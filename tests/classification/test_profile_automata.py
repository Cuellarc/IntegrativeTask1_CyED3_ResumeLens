from resumelens.classification.profile_automata import (
    accepts_pattern,
    build_profile_automaton,
)
from resumelens.profiles import (
    DATA_ENGINEER,
    DEVOPS_ENGINEER,
    FULL_STACK_DEVELOPER,
    MACHINE_LEARNING_ENGINEER,
    get_profile,
)


def test_full_stack_pattern_is_accepted() -> None:
    profile = get_profile(FULL_STACK_DEVELOPER)
    automaton = build_profile_automaton(profile)

    qualifications = [
        "JAVASCRIPT",
        "REACT",
        "NODE_JS",
        "POSTGRESQL",
        "GIT",
    ]

    assert accepts_pattern(automaton, qualifications)


def test_machine_learning_tensorflow_pattern_is_accepted() -> None:
    profile = get_profile(MACHINE_LEARNING_ENGINEER)
    automaton = build_profile_automaton(profile)

    qualifications = [
        "PYTHON",
        "PANDAS",
        "TENSORFLOW",
        "POSTGRESQL",
        "GIT",
    ]

    assert accepts_pattern(automaton, qualifications)


def test_machine_learning_scikit_learn_pattern_is_accepted() -> None:
    profile = get_profile(MACHINE_LEARNING_ENGINEER)
    automaton = build_profile_automaton(profile)

    qualifications = [
        "PYTHON",
        "PANDAS",
        "SCIKIT_LEARN",
        "SQL",
        "GIT",
    ]

    assert accepts_pattern(automaton, qualifications)


def test_incomplete_machine_learning_pattern_is_rejected() -> None:
    profile = get_profile(MACHINE_LEARNING_ENGINEER)
    automaton = build_profile_automaton(profile)

    qualifications = ["PYTHON", "PANDAS", "GIT"]

    assert not accepts_pattern(automaton, qualifications)


def test_wrong_order_full_stack_pattern_is_rejected() -> None:
    profile = get_profile(FULL_STACK_DEVELOPER)
    automaton = build_profile_automaton(profile)

    qualifications = [
        "GIT",
        "JAVASCRIPT",
        "REACT",
        "NODE_JS",
        "POSTGRESQL",
    ]

    assert not accepts_pattern(automaton, qualifications)


def test_devops_pattern_is_accepted() -> None:
    profile = get_profile(DEVOPS_ENGINEER)
    automaton = build_profile_automaton(profile)

    qualifications = [
        "LINUX",
        "DOCKER",
        "JENKINS",
        "AWS",
        "TERRAFORM",
        "GIT",
    ]

    assert accepts_pattern(automaton, qualifications)


def test_data_engineer_pattern_is_accepted() -> None:
    profile = get_profile(DATA_ENGINEER)
    automaton = build_profile_automaton(profile)

    qualifications = [
        "PYTHON",
        "SQL",
        "SPARK",
        "AIRFLOW",
        "SNOWFLAKE",
        "GIT",
    ]

    assert accepts_pattern(automaton, qualifications)


def test_empty_pattern_is_rejected() -> None:
    profile = get_profile(FULL_STACK_DEVELOPER)
    automaton = build_profile_automaton(profile)

    assert not accepts_pattern(automaton, [])


def test_foreign_symbol_is_rejected() -> None:
    profile = get_profile(FULL_STACK_DEVELOPER)
    automaton = build_profile_automaton(profile)

    qualifications = [
        "PYTHON",
        "REACT",
        "NODE_JS",
        "POSTGRESQL",
        "GIT",
    ]

    assert not accepts_pattern(automaton, qualifications)


def test_automaton_has_one_state_per_category_plus_start() -> None:
    profile = get_profile(FULL_STACK_DEVELOPER)
    automaton = build_profile_automaton(profile)

    assert len(automaton.states) == len(profile.categories) + 1


def test_automaton_has_one_final_state() -> None:
    profile = get_profile(FULL_STACK_DEVELOPER)
    automaton = build_profile_automaton(profile)

    assert len(automaton.final_states) == 1