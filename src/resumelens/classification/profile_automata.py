from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol

from resumelens.models import Profile


# Builds a DFA that requires one qualification from each profile category.
def build_profile_automaton(profile: Profile) -> DeterministicFiniteAutomaton:
    automaton = DeterministicFiniteAutomaton()
    states = [State(f"q{index}") for index in range(len(profile.categories) + 1)]

    automaton.add_start_state(states[0])
    automaton.add_final_state(states[-1])

    for index, category in enumerate(profile.categories):
        for qualification in category.qualifications:
            automaton.add_transition(
                states[index],
                Symbol(qualification),
                states[index + 1],
            )

    return automaton


def accepts_pattern(
    automaton: DeterministicFiniteAutomaton,
    qualifications: list[str],
) -> bool:
    symbols = [Symbol(qualification) for qualification in qualifications]
    return automaton.accepts(symbols)