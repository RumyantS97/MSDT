import pytest

from analyzer.exceptions import SyntaxAnalyzeError
from analyzer.states import S, G1


def test_normal():
    state = S('IF E1<CD THEN B12 := - 81;')
    assert isinstance(state.analyze(), G1)


def test_syntax_error():
    with pytest.raises(SyntaxAnalyzeError):
        state = S('syntax error')
        state.analyze()
