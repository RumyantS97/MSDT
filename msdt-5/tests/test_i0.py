import pytest

from analyzer import SemanticData
from analyzer.exceptions import SyntaxAnalyzeError
from analyzer.states import I0, C1
from analyzer.types import Identifier


def test_normal_collect():
    state = I0('E1<CD THEN B12 := - 81;', cur_pos=1,
               semantic_data=SemanticData([], [], current_identifier=Identifier(0, 'E')))
    new_state = state.analyze()
    assert isinstance(new_state, I0)
    assert new_state.semantic_data.current_identifier.value == 'E1'


def test_normal_transition():
    state = I0('E1<CD THEN B12 := - 81;', cur_pos=2,
               semantic_data=SemanticData([], [], current_identifier=Identifier(0, 'E1')))
    new_state = state.analyze()
    assert isinstance(new_state, C1)
    assert new_state.semantic_data.identifiers[0].value == 'E1'


def test_syntax_error():
    with pytest.raises(SyntaxAnalyzeError):
        state = I0('E1!=CD', cur_pos=2,
                   semantic_data=SemanticData([], [], current_identifier=Identifier(0, 'E1')))
        state.analyze()
