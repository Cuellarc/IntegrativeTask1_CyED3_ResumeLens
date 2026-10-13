from pathlib import Path

import pytest

from resumelens.errors import InvalidProfileError
from resumelens.pipeline import ResumeAnalyzer
from resumelens.profiles import (
    DATA_ENGINEER,
    DEVOPS_ENGINEER,
    FULL_STACK_DEVELOPER,
    MACHINE_LEARNING_ENGINEER,
)

RESUMES_DIRECTORY = Path(__file__).resolve().parents[1] / "data" / "resumes"
analyzer = ResumeAnalyzer()


def read_resume(file_name: str) -> str:
    return (RESUMES_DIRECTORY / file_name).read_text(encoding="utf-8")


def accepted_profiles(file_name: str) -> list[str]:
    candidate = analyzer.analyze(read_resume(file_name))
    return [item.profile_name for item in candidate.classifications if item.accepted]


@pytest.mark.parametrize(
    "file_name, expected",
    [
        ("resume_full_stack_developer_1.txt", [FULL_STACK_DEVELOPER]),
        ("resume_full_stack_developer_2.txt", [FULL_STACK_DEVELOPER]),
        ("resume_machine_learning_engineer_1.txt", [MACHINE_LEARNING_ENGINEER]),
        ("resume_devops_engineer_1.txt", [DEVOPS_ENGINEER]),
        ("resume_data_engineer_1.txt", [DATA_ENGINEER]),
        ("resume_multi_profile_1.txt", [FULL_STACK_DEVELOPER, MACHINE_LEARNING_ENGINEER]),
        ("resume_no_profile_1.txt", []),
    ],
)
def test_analyze_accepts_the_expected_profiles(file_name, expected):
    assert accepted_profiles(file_name) == expected


def test_analyze_classifies_the_four_profiles_for_every_resume():
    candidate = analyzer.analyze(read_resume("resume_full_stack_developer_2.txt"))
    assert len(candidate.classifications) == 4


def test_analyze_returns_normalized_skills_and_sorted_sequence():
    candidate = analyzer.analyze(read_resume("resume_full_stack_developer_2.txt"))
    assert candidate.full_name == "Wednesday Addams"
    assert candidate.skills == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
    full_stack = candidate.classifications[0]
    assert full_stack.qualifications == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]


def test_analyze_does_not_depend_on_the_order_of_the_skills():
    first = analyzer.analyze("Ana Perez\nTechnical Skills:\nGit, NodeJS, JS, Postgres, React.js.\n")
    second = analyzer.analyze("Ana Perez\nTechnical Skills:\nJS, React.js, NodeJS, Postgres, Git.\n")
    assert first.classifications[0].qualifications == second.classifications[0].qualifications
    assert first.classifications[0].accepted


def test_analyze_uses_unknown_name_and_empty_data_for_unrecognizable_text():
    candidate = analyzer.analyze("???\n123\n")
    assert candidate.full_name == "Unknown"
    assert candidate.email is None
    assert candidate.skills == []
    assert not any(item.accepted for item in candidate.classifications)


def test_analyze_copies_contact_and_optional_fields():
    candidate = analyzer.analyze(read_resume("resume_full_stack_developer_1.txt"))
    assert candidate.email == "wednesday.addams@example.com"
    assert candidate.phone == "+57 300 123 4567"
    assert candidate.location == "Nevermore Academy, Jericho"
    assert candidate.experiences[0].role == "Web Application Developer"


def test_generate_report_creates_html_with_name_and_accepted_profile(tmp_path):
    path = analyzer.generate_report(read_resume("resume_full_stack_developer_1.txt"), str(tmp_path))
    html = Path(path).read_text(encoding="utf-8")
    assert Path(path).name == "wednesday_addams.html"
    assert "Wednesday Addams" in html
    assert "ACCEPTED" in html
    assert "JAVASCRIPT" in html


def test_generate_report_for_resume_without_accepted_profile_shows_no_matching_profile(tmp_path):
    text = "Ana Perez\nTechnical Skills:\nPython, Git.\n"
    path = analyzer.generate_report(text, str(tmp_path))
    assert "No matching profile" in Path(path).read_text(encoding="utf-8")


def test_generate_report_raises_invalid_profile_error_when_no_skill_is_recognized(tmp_path):
    with pytest.raises(InvalidProfileError):
        analyzer.generate_report(read_resume("resume_no_profile_1.txt"), str(tmp_path))


def test_generate_report_creates_missing_output_directory(tmp_path):
    output_dir = tmp_path / "nested" / "output"
    path = analyzer.generate_report(read_resume("resume_machine_learning_engineer_1.txt"), str(output_dir))
    assert Path(path).exists()
