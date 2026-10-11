from pathlib import Path

from textx import metamodel_from_file
from textx.exceptions import TextXError

from resumelens.errors import InvalidProfileError


_GRAMMAR_PATH = Path(__file__).with_name("candidate_profile.tx")
_METAMODEL = metamodel_from_file(str(_GRAMMAR_PATH))


# Parses and validates candidate profile DSL text.
def parse_dsl(text: str) -> object:
    try:
        return _METAMODEL.model_from_str(text)
    except TextXError as error:
        raise InvalidProfileError(str(error)) from error


def parse_dsl_file(path: str) -> object:
    try:
        return _METAMODEL.model_from_file(path)
    except TextXError as error:
        raise InvalidProfileError(str(error)) from error