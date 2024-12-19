from loguru import logger

from analyzer.states import S, F
from analyzer.types import SemanticData


def analyze(input_str: str) -> SemanticData:
    state = S(input_str)
    while not isinstance(state, F):
        logger.debug(f"Current state: {state.__class__.__name__}. Position: {state.cur_pos}")
        state = state.analyze()
    final_state: F = state.analyze()
    logger.debug(f"Current state: {state.__class__.__name__}. Position: {state.cur_pos}")
    return final_state.semantic_data
