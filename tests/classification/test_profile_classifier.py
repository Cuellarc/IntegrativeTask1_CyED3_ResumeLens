import pytest

from resumelens.classification.profile_classifier import ProfileClassifier
from resumelens.errors import UnknownProfileError
from resumelens.profiles import (
    DATA_ENGINEER,
    DEVOPS_ENGINEER,
    FULL_STACK_DEVELOPER,
    MACHINE_LEARNING_ENGINEER,
    get_profiles,
)


def test_classifier_accepts_full_stack_profile() -> None:
    classifier = ProfileClassifier(get_profiles())

    qualifications = [
        "JAVASCRIPT",
        "REACT",
        "NODE_JS",
        "POSTGRESQL",
        "GIT",
    ]

    result = classifier.classify(
        FULL_STACK_DEVELOPER,
        qualifications,
    )

    assert result.profile_name == FULL_STACK_DEVELOPER
    assert result.accepted
    assert result.qualifications == qualifications


def test_classifier_accepts_machine_learning_profile() -> None:
    classifier = ProfileClassifier(get_profiles())

    qualifications = [
        "PYTHON",
        "PANDAS",
        "SCIKIT_LEARN",
        "SQL",
        "GIT",
    ]

    result = classifier.classify(
        MACHINE_LEARNING_ENGINEER,
        qualifications,
    )

    assert result.accepted


def test_classifier_rejects_incomplete_profile() -> None:
    classifier = ProfileClassifier(get_profiles())

    result = classifier.classify(
        MACHINE_LEARNING_ENGINEER,
        ["PYTHON", "PANDAS", "GIT"],
    )

    assert not result.accepted


def test_classifier_accepts_devops_profile() -> None:
    classifier = ProfileClassifier(get_profiles())

    qualifications = [
        "LINUX",
        "DOCKER",
        "JENKINS",
        "AWS",
        "TERRAFORM",
        "GIT",
    ]

    result = classifier.classify(
        DEVOPS_ENGINEER,
        qualifications,
    )

    assert result.accepted


def test_classifier_accepts_data_engineer_profile() -> None:
    classifier = ProfileClassifier(get_profiles())

    qualifications = [
        "PYTHON",
        "SQL",
        "SPARK",
        "AIRFLOW",
        "SNOWFLAKE",
        "GIT",
    ]

    result = classifier.classify(
        DATA_ENGINEER,
        qualifications,
    )

    assert result.accepted


def test_classifier_rejects_empty_qualifications() -> None:
    classifier = ProfileClassifier(get_profiles())

    result = classifier.classify(
        FULL_STACK_DEVELOPER,
        [],
    )

    assert not result.accepted


def test_classifier_raises_for_unknown_profile() -> None:
    classifier = ProfileClassifier(get_profiles())

    with pytest.raises(UnknownProfileError):
        classifier.classify(
            "UNKNOWN_PROFILE",
            ["GIT"],
        )