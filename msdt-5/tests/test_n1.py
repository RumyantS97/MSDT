import pytest

from analyzer import SemanticData
from analyzer.exceptions import SyntaxAnalyzeError, SemanticAnalyzeError
from analyzer.states import N1, G3
from analyzer.types import Constant


def test_normal_collect():
    state = N1('10 THEN B12 := - 81;', cur_pos=1,
               semantic_data=SemanticData([], [], current_constant=Constant(0, '1')))
    new_state = state.analyze()
    assert isinstance(new_state, N1)
    assert new_state.semantic_data.current_constant.value == 10


def test_normal_transition():
    state = N1('10 THEN B12 := - 81;', cur_pos=2,
               semantic_data=SemanticData([], [], current_constant=Constant(0, '10')))
    new_state = state.analyze()
    assert isinstance(new_state, G3)
    assert new_state.semantic_data.constants[0].value == 10


def test_syntax_error():
    with pytest.raises(SyntaxAnalyzeError):
        state = N1('10A', cur_pos=2,
                   semantic_data=SemanticData([], [], current_constant=Constant(0, '10')))
        state.analyze()


def test_semantic_error():
    with pytest.raises(SemanticAnalyzeError):
        state = N1('100000 THEN', cur_pos=6,
                   semantic_data=SemanticData([], [], current_constant=Constant(0, '100000')))
        state.analyze()
