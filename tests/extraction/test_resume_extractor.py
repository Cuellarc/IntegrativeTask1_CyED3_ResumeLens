from pathlib import Path

from resumelens.extraction.regex_extractor import ResumeExtractor
from resumelens.models import ExperienceRecord

RESUMES_DIRECTORY = Path(__file__).resolve().parents[2] / "data" / "resumes"


def read_resume(file_name: str) -> str:
    return (RESUMES_DIRECTORY / file_name).read_text(encoding="utf-8")


def test_extract_name_returns_first_line_name():
    extractor = ResumeExtractor()
    assert extractor.extract_name("Mary Jane Watson\nTechnical Skills:") == "Mary Jane Watson"


def test_extract_name_returns_none_when_first_line_is_not_a_name():
    extractor = ResumeExtractor()
    assert extractor.extract_name("technical skills:\nPython") is None


def test_extract_contacts_finds_email_phone_and_links():
    text = read_resume("resume_full_stack_developer_1.txt")
    emails, phones, links = ResumeExtractor().extract_contacts(text)
    assert emails == ["wednesday.addams@example.com"]
    assert phones == ["+57 300 123 4567"]
    assert links == ["https://github.com/wednesday-addams"]


def test_extract_contacts_finds_phone_without_country_code():
    text = read_resume("resume_devops_engineer_1.txt")
    _, phones, _ = ResumeExtractor().extract_contacts(text)
    assert phones == ["310 555 1234"]


def test_extract_skills_from_full_stack_fragment():
    result = ResumeExtractor().extract(read_resume("resume_full_stack_developer_2.txt"))
    assert result.languages == ["JS"]
    assert result.frameworks == ["React.js", "NodeJS"]
    assert result.databases == ["Postgres"]
    assert result.tools == ["Git"]


def test_extract_skills_from_machine_learning_fragment():
    result = ResumeExtractor().extract(read_resume("resume_machine_learning_engineer_1.txt"))
    assert result.languages == ["Python"]
    assert result.frameworks == ["Pandas", "NumPy", "Scikit-learn", "TensorFlow"]
    assert result.databases == ["SQL"]
    assert result.tools == ["Git"]


def test_extract_skills_from_devops_resume():
    result = ResumeExtractor().extract(read_resume("resume_devops_engineer_1.txt"))
    assert result.tools == ["Jenkins", "Docker", "Kubernetes", "AWS", "Terraform", "Linux", "Git"]


def test_extract_skills_from_data_engineering_resume():
    result = ResumeExtractor().extract(read_resume("resume_data_engineer_1.txt"))
    assert result.languages == ["Python"]
    assert result.frameworks == ["Spark", "Airflow"]
    assert result.databases == ["Snowflake", "SQL"]


def test_extract_skills_does_not_match_inside_other_words():
    result = ResumeExtractor().extract("Experienced with PostgreSQL and NoSQL, using Projects daily")
    assert result.databases == ["PostgreSQL"]
    assert result.languages == []


def test_extract_experience_from_sentence():
    text = read_resume("resume_full_stack_developer_2.txt")
    experiences = ResumeExtractor().extract_experiences(text)
    assert experiences == [ExperienceRecord(3, "developing web applications")]


def test_extract_experience_sentence_without_description_uses_default():
    experiences = ResumeExtractor().extract_experiences("4 years of experience.")
    assert experiences == [ExperienceRecord(4, "professional experience")]


def test_extract_experience_from_header_with_highlights():
    text = read_resume("resume_full_stack_developer_1.txt")
    experiences = ResumeExtractor().extract_experiences(text)
    assert len(experiences) == 1
    assert experiences[0].years == 3
    assert experiences[0].role == "Web Application Developer"
    assert experiences[0].organization == "Nevermore Academy Projects"
    assert len(experiences[0].highlights) == 4
    assert experiences[0].highlights[1] == "Implemented backend services using Node.js."


def test_extract_several_experiences_keeps_highlights_separated():
    text = "Ana Perez\nExperience:\nDeveloper - Acme (2 years)\n- Built apis.\nAnalyst - Beta (1 year)\n- Made reports.\n"
    experiences = ResumeExtractor().extract_experiences(text)
    assert [record.years for record in experiences] == [2, 1]
    assert experiences[0].highlights == ["Built apis."]
    assert experiences[1].highlights == ["Made reports."]


def test_extract_location_role_and_summary():
    result = ResumeExtractor().extract(read_resume("resume_full_stack_developer_1.txt"))
    assert result.location == "Nevermore Academy, Jericho"
    assert result.current_role == "Student and independent investigator"
    assert result.summary == (
        "Detail-oriented developer with three years of experience developing web applications. "
        "Her work involves small tools that organize clues and investigation records."
    )


def test_extract_education():
    result = ResumeExtractor().extract(read_resume("resume_data_engineer_1.txt"))
    assert result.education == ["Master in Data Science - Universidad Icesi"]


def test_extract_handles_windows_line_endings():
    text = read_resume("resume_full_stack_developer_1.txt").replace("\n", "\r\n")
    result = ResumeExtractor().extract(text)
    assert result.full_name == "Wednesday Addams"
    assert result.location == "Nevermore Academy, Jericho"


def test_extract_full_resume_fills_every_field():
    result = ResumeExtractor().extract(read_resume("resume_full_stack_developer_1.txt"))
    assert result.full_name == "Wednesday Addams"
    assert result.education == ["Bachelor in Computer Science - Nevermore Academy"]
    assert result.languages == ["JS"]
    assert result.frameworks == ["Node.js", "React.js", "NodeJS"]
    assert result.databases == ["PostgreSQL", "Postgres"]
    assert result.tools == ["Git"]


def test_extract_unrecognizable_text_returns_empty_result():
    result = ResumeExtractor().extract("???\n123\n")
    assert result.full_name is None
    assert result.emails == []
    assert result.experiences == []
    assert result.languages == []
    assert result.frameworks == []
    assert result.databases == []
    assert result.tools == []


def test_extract_resume_without_technical_skills_returns_no_skills():
    result = ResumeExtractor().extract(read_resume("resume_no_profile_1.txt"))
    assert result.full_name == "Carlos Rivera"
    assert result.current_role == "Graphic Designer"
    assert result.languages == []
    assert result.tools == []


def test_extract_skills_from_multi_profile_resume():
    result = ResumeExtractor().extract(read_resume("resume_multi_profile_1.txt"))
    assert result.languages == ["JavaScript", "Python", "JS"]
    assert result.frameworks == ["React", "Node.js", "Pandas", "TensorFlow", "ReactJS"]
    assert result.databases == ["PostgreSQL"]
    assert result.tools == ["Git"]
