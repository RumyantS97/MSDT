import pytest
from unittest.mock import patch
from rankedresultseval import (
    precision,
    recall,
    interpolated_precision,
    avg_precision,
    precision_at_k,
    cumulative_gain,
    discounted_cumulative_gain,
    ideal_discounted_cumulative_gain,
    normalized_discounted_cumulative_gain,
)


@pytest.mark.parametrize(
    "serp, expected",
    [
        ([(1, 1), (2, 0), (3, 1)], [1.0, 0.5, 0.6666666666666666]),
        ([(1, 0), (2, 0), (3, 0)], [0.0, 0.0, 0.0]),
    ],
)
def test_precision(serp, expected):
    assert precision(serp) == expected


@pytest.mark.parametrize(
    "serp, expected",
    [
        ([(1, 1), (2, 0), (3, 1)], [0.5, 0.5, 1.0]),
        ([(1, 0), (2, 0), (3, 0)], None),
    ],
)
def test_recall(serp, expected):
    assert recall(serp) == expected


@pytest.mark.parametrize(
    "serp, precisions, expected",
    [
        (
            [(1, 1), (2, 0), (3, 1)],
            [1.0, 0.5, 0.6666666666666666],
            [1.0, 0.6666666666666666, 0.6666666666666666],
        ),
        ([(1, 0), (2, 0), (3, 0)], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
    ],
)
def test_interpolated_precision(serp, precisions, expected):
    assert interpolated_precision(serp, precisions) == expected


@pytest.mark.parametrize(
    "serp, precisions, expected",
    [
        (
            [(1, 1), (2, 0), (3, 1)],
            [1.0, 0.5, 0.6666666666666666],
            [1.0, 0.75, 0.7222222222222222],
        ),
    ],
)
def test_avg_precision(serp, precisions, expected):
    assert avg_precision(serp, precisions) == expected


@pytest.mark.parametrize(
    "k, precisions, expected",
    [
        (1, [1.0, 0.5, 0.6666666666666666], 1.0),
        (2, [1.0, 0.5, 0.6666666666666666], 0.5),
        (4, [1.0, 0.5, 0.6666666666666666], None),
    ],
)
def test_precision_at_k(k, precisions, expected):
    assert precision_at_k(k, precisions) == expected


def test_cumulative_gain():
    serp = [(1, 1), (2, 0), (3, 1)]
    assert cumulative_gain(serp) == 2


@pytest.mark.parametrize(
    "serp, expected",
    [
        ([(1, 1), (2, 0), (3, 1)], 1.5),
    ],
)
def test_discounted_cumulative_gain(serp, expected):
    assert discounted_cumulative_gain(serp) == pytest.approx(expected, rel=1e-5)


@pytest.mark.parametrize(
    "serp, expected",
    [
        ([(1, 1), (2, 0), (3, 1)], 1.6309297535714575),
    ],
)
def test_ideal_discounted_cumulative_gain(serp, expected):
    assert ideal_discounted_cumulative_gain(serp) == pytest.approx(expected, rel=1e-5)


@pytest.mark.parametrize(
    "serp, expected",
    [
        ([(1, 1), (2, 0), (3, 1)], 0.9197207891481876),
    ],
)
def test_normalized_discounted_cumulative_gain(serp, expected):
    assert normalized_discounted_cumulative_gain(serp) == pytest.approx(
        expected, rel=1e-5
    )
