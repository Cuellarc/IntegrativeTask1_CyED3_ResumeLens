from pathlib import Path

import pytest

from resumelens.dsl.dsl_parser import parse_dsl_file
from resumelens.errors import InvalidProfileError


_DATA_DIRECTORY = Path("data/profiles_dsl")


@pytest.mark.parametrize(
    "filename",
    [
        "valid_full_stack.rlp",
        "valid_machine_learning.rlp",
        "valid_devops.rlp",
        "valid_data_engineer.rlp",
        "valid_no_classification.rlp",
        "valid_no_contact_details.rlp",
    ],
)
def test_valid_profile_is_accepted(filename: str) -> None:
    model = parse_dsl_file(str(_DATA_DIRECTORY / filename))

    assert model.name


@pytest.mark.parametrize(
    "filename",
    [
        "invalid_email.rlp",
        "invalid_negative_years.rlp",
        "invalid_lowercase_skill.rlp",
        "invalid_unknown_profile.rlp",
        "invalid_missing_brace.rlp",
        "invalid_missing_name.rlp",
    ],
)
def test_invalid_profile_is_rejected(filename: str) -> None:
    with pytest.raises(InvalidProfileError):
        parse_dsl_file(str(_DATA_DIRECTORY / filename))