from math import log
from typing import List, Tuple, Optional


def precision(serp: List[Tuple[int, int]]) -> List[float]:
    """
    Calculate precision at each rank in the SERP.
    """
    l = []
    nr_docs_retrieved = 0
    nr_relevant_docs_retrieved = 0
    for rank in serp:
        nr_docs_retrieved += 1
        nr_relevant_docs_retrieved += rank[1]
        l.append(nr_relevant_docs_retrieved / float(nr_docs_retrieved))
    return l


def recall(serp: List[Tuple[int, int]]) -> Optional[List[float]]:
    """
    Calculate recall at each rank in the SERP.
    """
    l = []
    nr_relevant_docs_retrieved = 0
    nr_relevant_docs = sum([rank[1] for rank in serp])
    if nr_relevant_docs == 0:
        return None
    for rank in serp:
        nr_relevant_docs_retrieved += rank[1]
        l.append(nr_relevant_docs_retrieved / float(nr_relevant_docs))
    return l


def interpolated_precision(
    serp: List[Tuple[int, int]], precisions: List[float] = []
) -> List[float]:
    """
    Calculate interpolated precision for the SERP.
    """
    l = []
    for r in range(0, len(serp)):
        l.append(max(precisions[r:]))
    return l


def avg_precision(
    serp: List[Tuple[int, int]], precisions: List[float] = []
) -> List[float]:
    """
    Calculate average precision at each rank.
    """
    avg_precisions = []
    for r in range(1, len(serp) + 1):
        avg_precisions.append(sum(precisions[:r]) / float(r))
    return avg_precisions


def precision_at_k(k: int, precisions: List[float]) -> Optional[float]:
    """
    Get precision at a specific rank k.
    """
    try:
        return precisions[k - 1]
    except IndexError:
        return None


def cumulative_gain(serp: List[Tuple[int, int]]) -> int:
    """
    Calculate the cumulative gain for the SERP.
    """
    return sum(rank[1] for rank in serp)


def discounted_cumulative_gain(serp: List[Tuple[int, int]]) -> float:
    """
    Calculate the discounted cumulative gain (DCG) for the SERP.
    """
    return sum([g / log(i + 2) for (i, g) in enumerate([
            rank[1] for rank in serp
        ])])


def ideal_discounted_cumulative_gain(serp: List[Tuple[int, int]]) -> float:
    """
    Calculate the ideal discounted cumulative gain (IDCG).
    """
    return sum(
        [
            g / log(i + 2)
            for (i, g) in enumerate(sorted([
                rank[1] for rank in serp
            ], reverse=True))
        ]
    )


def normalized_discounted_cumulative_gain(
        serp: List[Tuple[int, int]]
    ) -> float:
    """
    Calculate the normalized discounted cumulative gain (nDCG).
    """
    idcg = ideal_discounted_cumulative_gain(serp)
    return discounted_cumulative_gain(serp) / idcg if idcg != 0 else 0


def show_ranked_results_evaluation(serp: List[Tuple[int, int]]) -> None:
    """
    Display evaluation metrics for the ranked SERP.
    """
    precisions = precision(serp)
    recalls = recall(serp)
    interpolated_precisions = interpolated_precision(serp, precisions)
    print("RANK\tRELEVANT?\tPRECISION\tRECALL\t\tINTERPOLATED PRECISION")
    for s, p, r, i in zip(serp, precisions, recalls, interpolated_precisions):
        fs0 = str(s[0])
        fs1 = str(s[1])
        fp = str(round(p, 5)).ljust(7, "0")
        fr = str(round(r, 5)).ljust(7, "0")
        fi = str(round(i, 5)).ljust(7, "0")
        print(f"{fs0}\t{fs1}\t\t{fp}\t\t{fr}\t\t{fi}")
