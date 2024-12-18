import math
import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import (
    LogisticRegression,
    Ridge,
)
from sklearn.metrics import auc, precision_recall_curve, roc_curve
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.feature_selection import RFE

import helper
import smote as st

np.set_printoptions(suppress=True,
                    formatter={
                        'all': lambda x: str(x) + ','
                    },
                    linewidth=9999)
should_have_failed = 0
success = 0


def preprocess_game_state(game_state: str, remove_fallen_opp: bool = False) -> tuple:
    """
    Parse and preprocess the game state string into structured data.
    """
    x, init_time, x, agent_info, x, opp, x, me, x, ball, x, kick_target, x, direct_features = game_state.split(
        ":")
    init_time = float(init_time)
    agent_type = int(agent_info.split()[1])
    ball = [float(x) for x in ball.split()]
    me = [float(x) for x in me.split()]
    kick_target = [float(x) for x in kick_target.split()]
    direct_features = direct_features.split()
    direct_features = [float(x) for x in direct_features]

    if len(opp) == 0:
        opp_array = []
    else:
        opp_array = [[float(x) for x in temp.split()]
                     for temp in opp.split(';')[:-1]]
    if remove_fallen_opp:
        opp_array = helper.remove_fallen_opponents(opp_array)
    return init_time, opp_array, me, ball, kick_target, agent_type, direct_features


def is_opponent_2far(
    game_state: tuple,
    threshold: float = 2.5,
    remove_fallen_opp: bool = False
) -> bool:
    """
    Check if the closest opponent to the ball is farther than a threshold.
    """
    opp_array, me, ball, kick_target, agent_type, direct_features = game_state
    closest_opp_dist, closest_opp_index = helper.find_closest_opponent_to_ball(
        opp_array, ball)
    return closest_opp_dist > threshold


def parse_game_state(
    game_state: tuple,
    n_features: int,
    skip_no_opp: bool = True,
    kick_type: list = [7],
    remove_fallen_opp: bool = False,
    use_direct_features: bool = True,
) -> tuple:
    """
    Parse the game state to extract features for classification.
    """
    init_time, opp_array, me, ball, kick_target, agent_type, direct_features = game_state

    if (len(opp_array) == 0 or kick_target[2] not in kick_type) and skip_no_opp:
        return np.zeros(n_features), False

    if use_direct_features:
        return np.abs(np.array(direct_features)), True

    closest_opp_dist, closest_opp_index = helper.find_closest_opponent_to_ball(
        opp_array, ball)
    opp_dist_2kick_line = helper.get_dist_2kick_line(
        kick_target, ball, opp_array[closest_opp_index])
    angle_between_opp_and_kick_dir = helper.ang_between3_pts(
        ball, kick_target, opp_array[closest_opp_index])
    num_opp_closer_than_dist = helper.opp_closer_than_dist(
        opp_array, ball, dist=2.0)
    ang_between_opp_and_ball = helper.ang_between3_pts(
        me, ball, opp_array[closest_opp_index])
    ang2_turn_opp = helper.angle2_turn(
        ball, (-15.0, 0.0), math.radians(opp_array[closest_opp_index][2]))
    angle2_turn_me = helper.angle2_turn(ball, kick_target, math.radians(me[2]))
    opp_ball_angle, opp_ball_dist = helper.find_target_angleand_dist(
        opp_array[closest_opp_index], ball)
    angle_between_me_and_ball = helper.ang_between3_pts(
        opp_array[closest_opp_index], me, ball)
    opp_fallen = opp_array[closest_opp_index][3]
    num_opp_within_kick_dir = helper.opp_within_kick_dir(
        opp_array, kick_target, ball, angle_thres=30)
    closest_opp_angle_from_me, closest_opp_dist_from_me = helper.find_target_angleand_dist(
        me, opp_array[closest_opp_index])
    dist_to_kick_pos_opp = helper.dist_to_kick_position(
        ball, (-15.0, 0.0), opp_array[closest_opp_index])
    oppdist, indices, n = helper.find_n_closest_opponent_to_ball(
        opp_array, ball)
    mean_opp_dist = np.mean(oppdist)
    max_opp_dist = np.max(oppdist)
    ball_angle, ball_dist = helper.find_target_angleand_dist(me, ball)
    angle_of_kick = helper.ang_between3_pts(me, ball, kick_target)
    ball_velocity = helper.norm(ball[2], ball[3])

    feature_array = np.array([closest_opp_dist, opp_dist_2kick_line, angle_between_opp_and_kick_dir, num_opp_closer_than_dist, ang_between_opp_and_ball, ang2_turn_opp,
                             angle2_turn_me, opp_ball_angle, opp_fallen, num_opp_within_kick_dir, closest_opp_angle_from_me, closest_opp_dist_from_me,
                             dist_to_kick_pos_opp, mean_opp_dist, max_opp_dist, ball_angle, ball_dist, angle_of_kick, ball_velocity, angle_between_me_and_ball])
    return feature_array, True


def parse_kick_success(
    game_state: tuple,
    ball_movement: str,
    ez_kick_success: bool = False,
    ball_travel_dist: float = 2.0,
) -> int:
    """
    Evaluate whether a kick was successful based on ball movement.
    """
    init_time, opp_array, me, ball, kick_target, agent_type, direct_features = game_state
    x, immed_after_kick, x, after_kick, x, kick_info = ball_movement.split(":")
    kick_mode = int(kick_info.split()[0])
    if (kick_mode != 2):
        return -1
    if ez_kick_success:
        return 1
    after_kick = [float(x) for x in after_kick.split()]
    immed_after_kick = [float(x) for x in immed_after_kick.split()]

    timeElapsed = after_kick[2] - immed_after_kick[4]
    target = (immed_after_kick[2], immed_after_kick[3])
    ball_before = (immed_after_kick[0], immed_after_kick[1])
    ball_after = (after_kick[0], after_kick[1])

    ball_before_dist = helper.get_dist_to(ball_before, target)
    ball_after_dist = helper.get_dist_to(ball_after, target)

    if ball_before_dist - ball_after_dist > ball_travel_dist:
        return 1
    else:
        return -1


def parse_kick_success_new(game_state: tuple, ball_movement, ez_kick_success: bool = False) -> int:
    def get_dribble_dist(time_elapsed: float) -> float:
        if time_elapsed < 1.5:
            dist = 0.0
        else:
            dist = 4.0/6.5 * (time_elapsed - 1.5)

        return dist

    init_time, opp_array, me, ball, kick_target, agent_type, direct_features = game_state
    x, immed_after_kick, x, after_kick, x, kick_info = ball_movement.split(":")
    kick_mode = int(kick_info.split()[0])
    if (kick_mode != 2):
        return -1
    if ez_kick_success:
        return 1
    after_kick = [float(x) for x in after_kick.split()]
    immed_after_kick = [float(x) for x in immed_after_kick.split()]

    time_elapsed = after_kick[2] - init_time
    target = (kick_target[0], kick_target[1])
    ball_before = (immed_after_kick[0], immed_after_kick[1])
    ball_after = (after_kick[0], after_kick[1])

    travel_dist = helper.get_dist_to(
        ball_before, target) - helper.get_dist_to(ball_after, target)

    if travel_dist > get_dribble_dist(time_elapsed):
        return 1
    else:
        return -1


def parse(
    file_name: str = "combined.txt",
    use_cache: bool = False,
    n_features: int = 20,
    ez_kick_success: bool = False,
    kick_type: list = [10],
    remove_fallen_opp: bool = False,
    ignore_self_failure: bool = False,
    use_direct_features: bool = True,
) -> tuple:
    """
    Parse and preprocess the dataset for training and testing.
    """

    features_file = f"cache/{file_name[:-4]}{n_features}_{
        ez_kick_success}_{kick_type}_features.npy"
    labels_file = f"cache/{file_name[:-4]
                           }{n_features}_{ez_kick_success}_{kick_type}_labels.npy"

    if use_cache and os.path.exists(features_file) and os.path.exists(labels_file):
        print("cached files exists, using cache!")
        features = np.load(features_file)
        labels = np.load(labels_file)
        return features, labels

    w = open(file_name)
    lines = w.readlines()
    features = np.empty((len(lines), n_features))
    labels = np.empty(len(lines), dtype=np.int)
    success_index = []
    for index, line in enumerate(lines):
        if index % 1000 == 0:
            print(f"parsed {index} samples")
        rawgame_state, ball_movement = line.rstrip().split("#")

        try:
            game_state = preprocess_game_state(
                rawgame_state, remove_fallen_opp=remove_fallen_opp)
            feature_array, success = parse_game_state(game_state, n_features, kick_type=kick_type,
                                                      remove_fallen_opp=remove_fallen_opp, use_direct_features=use_direct_features)
        except:
            success = False

        if success:
            features[index, :] = feature_array
            labels[index] = parse_kick_success_new(
                game_state, ball_movement, ez_kick_success=ez_kick_success)
            if ignore_self_failure:
                if labels[index] == 1 or not is_opponent_2far(game_state, remove_fallen_opp=remove_fallen_opp):
                    success_index.append(index)
            else:
                success_index.append(index)
        else:
            pass

    print(f"ignored {len(lines) - len(success_index)} lines.")
    features = features[success_index, :]
    labels = labels[success_index]
    print("saving processed features and labels to file...")
    np.save(features_file, features)
    np.save(labels_file, labels)
    return features, labels


def visualize(use_features: list = [0, 8], frac: float = 0.005) -> None:
    """
    Visualize data distribution using a scatter plot.
    """
    features, labels = parse(useCache=False)
    features = features[:, use_features]
    r = np.random.random(features.shape[0]) < frac
    features2 = features[r, :]
    labels2 = labels[r]
    plt.figure(figsize=(16, 16))
    plt.xlabel("feature #1")
    plt.ylabel("feature #2")
    cm = plt.cm.get_cmap('cool')
    sc = plt.scatter(x=features2[:, 0],
                     y=features2[:, 1],
                     s=60, c=labels2,
                     cmap=cm
                     )
    plt.draw()
    plt.savefig('scatter.png', bbox_inches='tight')
    plt.clf()


def batch_eval_accuracy(file_names=['type0_apollo3d.txt', 'type0_fc.txt', 'type1_apollo3d.txt',
                                    'type1_fc.txt', 'type2_apollo3d.txt', 'type2_fc.txt',
                                    'type3_apollo3d.txt', 'type3_fc.txt', 'type4_apollo3d.txt', 'type4_fc.txt'],
                        use_features=[4, 6, 8, 11, 0, 15, 17,], kick_type=[10]) -> None:
    """
    Evaluate model accuracy in batch.
    """

    accuracys = []
    for i, file_name in enumerate(file_names):
        try:
            accuracyRate = classify(file_name=file_name, use_features=use_features, equal_class_size=False,
                                    use_all=False, batch=True, useCache=True, kick_type=kick_type, draw=False)
            accuracys.append(round(accuracyRate, 3))
        except:
            accuracys.append(0.0)

    for i, file_name in enumerate(file_names):
        print(file_name[:-4] + ":", accuracys[i])


def balance_classes(new_features: np.ndarray, labels: np.ndarray) -> tuple:
    """
    Balance classes in the dataset using oversampling.
    """
    pos = new_features[labels == 1]
    pos_labels = labels[labels == 1]
    neg = new_features[labels == -1]
    neg_labels = labels[labels == -1]
    r = np.random.random(neg.shape[0]) < float(pos.shape[0])/neg.shape[0]
    neg = neg[r, :]
    neg_labels = neg_labels[r]
    new_features = np.concatenate((neg, pos))
    labels = np.concatenate((neg_labels, pos_labels))
    return new_features, labels


def smote(new_features: np.ndarray, labels: np.ndarray) -> tuple:
    """
    Apply SMOTE to generate synthetic data points.
    """
    percentage = 100*(float(len(labels) - np.sum(labels))/np.sum(labels))
    percentage = int(round(percentage, -2))
    safe, synthetic, danger = sm.borderline_smote(
        new_features, labels, 1, percentage, 5)
    num_new_features = synthetic.shape[0]

    new_features = np.concatenate((new_features, synthetic))
    labels = np.concatenate((labels, np.ones(num_new_features)))
    return new_features, labels


def classify(file_name: str = '4_14_type4_apollo3d.txt', useFrac: float = 1.0, train_fraction: float = 0.5, equal_class_size: bool = True,
             thres: float = 0.5, use_features: list = [0], use_all: bool = True, batch: bool = False, use_cache: bool = True,
             feature_select: bool = False, kick_type: list = [11], draw: bool = False, scale: bool = False, C: float = 1.0, B: float = 1.0, return_prob: bool = False) -> float:
    """Main function to classify data using different models."""
    features, labels = parse(file_name=file_name, use_cache=use_cache, ez_kick_success=False,
                             kick_type=kick_type, ignore_self_failure=False, use_direct_features=True,
                             n_features=8)
    num2_use = int(useFrac*len(features))
    features = features[:num2_use]
    labels = labels[:num2_use]
    if scale:
        features = StandardScaler().fit_transform(features)
    print(f"features mean: {features.mean(axis=0)}")
    print(f"features std: {features.std(axis=0)}")
    if not use_all:
        new_features = features[:, use_features]
    else:
        new_features = features

    if equal_class_size:
        new_features, labels = balance_classes(new_features, labels)

    print(f"we have {new_features.shape[0]} samples.")
    print(f"we have {np.sum(labels == 1)} positive labels")
    print(f"ratio: {float(np.sum(labels == -1)) / np.sum(labels == 1)}")
    print(f"using approximately {train_fraction * 100}% as training examples")

    r = np.random.random(new_features.shape[0]) < train_fraction
    r2 = np.invert(r)
    training_set = new_features[r, :]
    train_labels = labels[r]
    testing_set = new_features[r2, :]
    test_labels = labels[r2]

    if not equal_class_size:
        testing_set, test_labels = balance_classes(testing_set, test_labels)
        clf = LogisticRegression(
            C=C, class_weight='auto', intercept_scaling=B, penalty='l2')
    else:
        clf = LogisticRegression(C=C, intercept_scaling=B, penalty='l2')

    if feature_select:
        rfecv = RFE(estimator=clf, step=1,  n_features_to_select=8)
        rfecv.fit(new_features, labels)
        print(f"Optimal number of features: {rfecv.n_features_}")
        print(rfecv.ranking_)
        print(np.arange(20)[rfecv.support_])
        return

    clf.fit(training_set, train_labels)

    def my_predict(clf, x, thres=0.5):
        prob_array = clf.predict_proba(x)[:, 1]
        predict_labels = 1*(prob_array > thres)
        predict_labels = 2*predict_labels - 1
        return predict_labels, prob_array

    if return_prob:
        predict_labels, prob_array = my_predict(clf, testing_set, thres=thres)
    else:
        predict_labels = clf.predict(testing_set)

    suffix = "" if use_all else str(features)

    if draw and return_prob:
        area = draw_precision_recall_curve(
            file_name[:-4] + suffix, test_labels, prob_array)
        roc_auc = draw_roc_curve(
            file_name[:-4] + suffix, test_labels, prob_array)

    false_neg = false_pos = true_neg = true_pos = 0
    for i in range(len(predict_labels)):
        if predict_labels[i] == test_labels[i] == -1:
            true_neg += 1
        elif predict_labels[i] == test_labels[i] == 1:
            true_pos += 1
        elif predict_labels[i] == -1 and test_labels[i] == 1:
            false_neg += 1
        else:
            false_pos += 1
    good = true_neg + true_pos
    print(f"accuracy rate: {good / float(len(predict_labels))}, {good}")
    print(f"true negative rate: {true_neg / float(len(predict_labels))}, {true_neg}")
    print(f"true positive rate: {true_pos / float(len(predict_labels))}, {true_pos}")
    print(f"false negative rate: {false_neg / float(len(predict_labels))}, {false_neg}")
    print(f"false positive rate: {false_pos / float(len(predict_labels))}, {false_pos}")
    precision = true_pos/float(true_pos + false_pos)
    recall = true_pos/float(true_pos + false_neg)
    print(f"precision: {precision}")
    print(f"recall: {recall}")
    print(f"f1 score: {2 * (precision * recall) / (precision + recall)}")
    return good/float(len(predict_labels))


def draw_precision_recall_curve(file_name: str, test_labels: np.ndarray, prob_array: np.ndarray) -> None:
    """Draw the Precision-Recall curve."""
    precision, recall, thresholds = precision_recall_curve(
        test_labels, prob_array)
    area = auc(recall, precision)
    plt.clf()
    plt.plot(recall, precision, label='Precision-Recall curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.grid()
    plt.title('Precision-Recall: AUC=%0.2f' % area)
    plt.legend(loc="lower left")
    plt.savefig(f"{file_name}_precRecallCurve")


def draw_roc_curve(file_name: str, test_labels: np.ndarray, prob_array: np.ndarray) -> None:
    """Draw the ROC curve."""
    fpr, tpr, thresholds = roc_curve(test_labels, prob_array)
    roc_auc = auc(fpr, tpr)
    plt.clf()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.grid()
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.savefig(f"{file_name}_ROC")


def visualize_dribble_data(dribble: str = "type4_dribble.txt", kick: str = "type4_rc.txt") -> None:
    """Visualize dribble data."""
    def parse_kick_data(kick: str) -> np.array:
        w = open(kick)
        lines = w.readlines()
        my_list = []
        for index, line in enumerate(lines):
            if index % 1000 == 0:
                print(f"parsed {index} samples")
            game_state, ball_movement = line.rstrip().split("#")
            x, init_time, x, agent_info, x, opp, x, me, x, ball, x, kick_target, x, direct_features = game_state.split(":")
            init_time = float(init_time)
            x, immed_after_kick, x, after_kick, x, kick_info = ball_movement.split(":")
            kick_mode = int(kick_info.split()[0])
            if (kick_mode != 2):
                continue
            after_kick = [float(x) for x in after_kick.split()]
            immed_after_kick = [float(x) for x in immed_after_kick.split()]

            final_time = after_kick[2]
            target = (immed_after_kick[2], immed_after_kick[3])
            ball_before = (immed_after_kick[0], immed_after_kick[1])
            ball_after = (after_kick[0], after_kick[1])
            ball_before_dist = helper.get_dist_to(ball_before, target)
            ball_after_dist = helper.get_dist_to(ball_after, target)

            dist_traveled = ball_before_dist - ball_after_dist
            time_elapsed = final_time - init_time
            my_list.append([time_elapsed, dist_traveled])
        return np.array(my_list)

    plt.figure(figsize=(16, 12))
    mat = np.loadtxt(dribble)
    plt.scatter(mat[:, 0], mat[:, 1], alpha=0.3, c='g', label="dibble")
    plt.legend()
    plt.xlabel("time elapsed in seconds")
    plt.ylabel("distance ball traveled in meters")
    plt.grid()
    ax = plt.gca()
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 0.5))

    r = make_pipeline(PolynomialFeatures(9), Ridge(alpha=0.0001))

    r.fit(np.reshape(mat[:, 0], (-1, 1)), mat[:, 1])
    x = np.linspace(0, 12, 100)
    x = np.reshape(x, (-1, 1))
    y = r.predict(x)
    plt.plot(x, y, c='g', linewidth=3)

    plt.savefig("dibble_kick_compare.png", bbox_inches="tight")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        eval(sys.argv[1])()
    else:
        classify()
