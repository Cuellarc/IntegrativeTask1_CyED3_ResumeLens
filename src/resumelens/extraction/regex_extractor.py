import re

from resumelens.extraction.patterns import (
    CURRENT_ROLE_PATTERN,
    DATABASE_PATTERN,
    EDUCATION_PATTERN,
    EMAIL_PATTERN,
    EXPERIENCE_HEADER_PATTERN,
    EXPERIENCE_SENTENCE_PATTERN,
    FRAMEWORK_PATTERN,
    HIGHLIGHT_PATTERN,
    LANGUAGE_PATTERN,
    LINK_PATTERN,
    LOCATION_PATTERN,
    NAME_PATTERN,
    PHONE_PATTERN,
    SUMMARY_PATTERN,
    TOOL_PATTERN,
)
from resumelens.models import ExperienceRecord, ExtractionResult

DEFAULT_DESCRIPTION = "professional experience"


class ResumeExtractor:
    # runs every regular expression over the resume text and groups the results
    def extract(self, text: str) -> ExtractionResult:
        text = text.replace("\r\n", "\n")
        emails, phones, links = self.extract_contacts(text)
        return ExtractionResult(
            full_name=self.extract_name(text),
            emails=emails,
            phones=phones,
            links=links,
            location=self.extract_labeled_value(text, LOCATION_PATTERN),
            current_role=self.extract_labeled_value(text, CURRENT_ROLE_PATTERN),
            summary=self.extract_summary(text),
            education=self.extract_education(text),
            experiences=self.extract_experiences(text),
            languages=self.extract_matches(text, LANGUAGE_PATTERN),
            frameworks=self.extract_matches(text, FRAMEWORK_PATTERN),
            databases=self.extract_matches(text, DATABASE_PATTERN),
            tools=self.extract_matches(text, TOOL_PATTERN),
        )

    def extract_name(self, text: str) -> str | None:
        for line in text.splitlines():
            line = line.strip()
            if line:
                return line if re.fullmatch(NAME_PATTERN, line) else None
        return None

    def extract_contacts(self, text: str) -> tuple[list[str], list[str], list[str]]:
        emails = self.extract_matches(text, EMAIL_PATTERN)
        phones = self.extract_matches(text, PHONE_PATTERN)
        links = self.extract_matches(text, LINK_PATTERN)
        return emails, phones, links

    def extract_education(self, text: str) -> list[str]:
        return [match.group(1) for match in re.finditer(EDUCATION_PATTERN, text)]

    def extract_experiences(self, text: str) -> list[ExperienceRecord]:
        experiences = []
        current = None
        for line in text.splitlines():
            highlight = re.fullmatch(HIGHLIGHT_PATTERN, line)
            if highlight and current is not None:
                current.highlights.append(highlight.group(1))
                continue
            header = re.fullmatch(EXPERIENCE_HEADER_PATTERN, line)
            if header:
                role = header.group("role").strip()
                current = ExperienceRecord(
                    years=int(header.group("years")),
                    description=role,
                    role=role,
                    organization=header.group("organization").strip(),
                )
                experiences.append(current)
            elif line.strip():
                current = None
        if experiences:
            return experiences
        return self.extract_sentence_experiences(text)

    def extract_sentence_experiences(self, text: str) -> list[ExperienceRecord]:
        experiences = []
        for match in re.finditer(EXPERIENCE_SENTENCE_PATTERN, text):
            description = match.group("description").strip() or DEFAULT_DESCRIPTION
            experiences.append(ExperienceRecord(int(match.group("years")), description))
        return experiences

    def extract_labeled_value(self, text: str, pattern: str) -> str | None:
        match = re.search(pattern, text)
        return match.group(1) if match else None

    def extract_summary(self, text: str) -> str | None:
        match = re.search(SUMMARY_PATTERN, text)
        return " ".join(match.group(1).split()) if match else None

    def extract_matches(self, text: str, pattern: str) -> list[str]:
        matches = []
        for match in re.finditer(pattern, text):
            value = match.group(0).strip().rstrip(".,;:")
            if value.lower() not in [item.lower() for item in matches]:
                matches.append(value)
        return matches
