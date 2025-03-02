import streamlit as st
from typing import Dict


def initialise_states(states=Dict[str, bool], initialise: bool = False) -> None:
    """
    Initialises session states.

    Parameters:
        states (Dict[str, bool]): The session states to initialise.

    Returns:
        None
    """

    # Clear states from previous sessions
    states_old = list(st.session_state.keys())
    for state in states_old:
        st.session_state.pop(state)

    # Initialise new states
    for state, value in states.items():
        if state not in st.session_state:
            st.session_state[state] = value

    return None
