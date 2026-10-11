from resumelens.dsl.dsl_parser import parse_dsl
from resumelens.dsl.dsl_writer import write_dsl
from resumelens.models import (
    CandidateData,
    ClassificationResult,
    ExperienceRecord,
)


def _build_candidate() -> CandidateData:
    return CandidateData(
        full_name="Wednesday Addams",
        email="wednesday@example.com",
        phone="+57 300 123 4567",
        links=["https://github.com/wednesday"],
        education=["Bachelor in Computer Science"],
        experiences=[
            ExperienceRecord(
                years=3,
                description="Developing web applications.",
                role="Web Application Developer",
                organization="Nevermore Academy Projects",
                highlights=[
                    "Implemented backend services using Node.js.",
                ],
            )
        ],
        skills=[
            "JAVASCRIPT",
            "REACT",
            "NODE_JS",
            "POSTGRESQL",
            "GIT",
        ],
        classifications=[
            ClassificationResult(
                profile_name="FULL_STACK_DEVELOPER",
                accepted=True,
                qualifications=[
                    "JAVASCRIPT",
                    "REACT",
                    "NODE_JS",
                    "POSTGRESQL",
                    "GIT",
                ],
            ),
            ClassificationResult(
                profile_name="DEVOPS_ENGINEER",
                accepted=False,
                qualifications=["GIT"],
            ),
        ],
        location="Nevermore Academy, Jericho",
        current_role="Web Application Developer",
        summary="Detail-oriented developer.",
    )


def test_writer_includes_only_accepted_profiles() -> None:
    dsl = write_dsl(_build_candidate())

    assert "FULL_STACK_DEVELOPER: ACCEPTED" in dsl
    assert "DEVOPS_ENGINEER" not in dsl


def test_writer_output_can_be_parsed() -> None:
    dsl = write_dsl(_build_candidate())

    model = parse_dsl(dsl)

    assert model.name == "Wednesday Addams"


def test_writer_omits_missing_optional_fields() -> None:
    candidate = CandidateData(
        full_name="Test Candidate",
        email=None,
        phone=None,
        links=[],
        education=[],
        experiences=[],
        skills=["PYTHON"],
        classifications=[],
    )

    dsl = write_dsl(candidate)

    assert "contact {" not in dsl
    assert "location:" not in dsl
    assert "role:" not in dsl
    assert "summary:" not in dsl
    assert "classification {" not in dsl

    parse_dsl(dsl)


def test_writer_sanitizes_quotes_and_newlines() -> None:
    candidate = CandidateData(
        full_name='John "Test" Doe',
        email=None,
        phone=None,
        links=[],
        education=[],
        experiences=[],
        skills=["PYTHON"],
        classifications=[],
        summary="First line\nSecond line",
    )

    dsl = write_dsl(candidate)

    assert 'John \'Test\' Doe' in dsl
    assert "First line Second line" in dsl

    parse_dsl(dsl)