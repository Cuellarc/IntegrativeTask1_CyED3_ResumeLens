from resumelens.normalization.qualification_sorter import sort_qualifications
from resumelens.profiles import (
    DATA_ENGINEER,
    FULL_STACK_DEVELOPER,
    MACHINE_LEARNING_ENGINEER,
    get_profile,
)


def test_sort_qualifications_follows_the_category_order_of_the_profile():
    profile = get_profile(FULL_STACK_DEVELOPER)
    unordered = ["GIT", "NODE_JS", "JAVASCRIPT", "POSTGRESQL", "REACT"]
    assert sort_qualifications(unordered, profile) == [
        "JAVASCRIPT",
        "REACT",
        "NODE_JS",
        "POSTGRESQL",
        "GIT",
    ]


def test_sort_qualifications_skips_categories_without_a_match():
    profile = get_profile(MACHINE_LEARNING_ENGINEER)
    assert sort_qualifications(["GIT", "PYTHON"], profile) == ["PYTHON", "GIT"]


def test_sort_qualifications_discards_qualifications_outside_the_profile():
    profile = get_profile(FULL_STACK_DEVELOPER)
    assert sort_qualifications(["DOCKER", "GIT", "PYTHON"], profile) == ["GIT"]


def test_sort_qualifications_keeps_one_qualification_per_category_by_priority():
    profile = get_profile(MACHINE_LEARNING_ENGINEER)
    candidate = ["NUMPY", "PANDAS", "PYTORCH", "SCIKIT_LEARN", "PYTHON", "SQL", "POSTGRESQL", "GIT"]
    assert sort_qualifications(candidate, profile) == [
        "PYTHON",
        "PANDAS",
        "SCIKIT_LEARN",
        "SQL",
        "GIT",
    ]


def test_sort_qualifications_returns_empty_list_for_empty_input():
    assert sort_qualifications([], get_profile(DATA_ENGINEER)) == []


def test_sort_qualifications_depends_on_the_selected_profile():
    candidate = ["PANDAS", "PYTHON", "GIT", "SQL"]
    machine_learning = sort_qualifications(candidate, get_profile(MACHINE_LEARNING_ENGINEER))
    data_engineer = sort_qualifications(candidate, get_profile(DATA_ENGINEER))
    assert machine_learning == ["PYTHON", "PANDAS", "SQL", "GIT"]
    assert data_engineer == ["PYTHON", "SQL", "PANDAS", "GIT"]
