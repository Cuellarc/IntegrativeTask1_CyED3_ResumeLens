from pathlib import Path

from resumelens.classification.profile_classifier import ProfileClassifier
from resumelens.dsl.dsl_parser import parse_dsl
from resumelens.dsl.dsl_writer import write_dsl
from resumelens.dsl.html_renderer import render_html, save_html
from resumelens.extraction.regex_extractor import ResumeExtractor
from resumelens.models import CandidateData
from resumelens.normalization.normalizer import QualificationNormalizer
from resumelens.normalization.qualification_sorter import sort_qualifications
from resumelens.profiles import get_profiles

UNKNOWN_NAME = "Unknown"


class ResumeAnalyzer:
    def __init__(self) -> None:
        self.extractor = ResumeExtractor()
        self.normalizer = QualificationNormalizer()
        self.profiles = get_profiles()
        self.classifier = ProfileClassifier(self.profiles)

    # runs extraction, normalization, sorting and classification over a resume text
    def analyze(self, text: str) -> CandidateData:
        extraction = self.extractor.extract(text)
        raw_skills = (
            extraction.languages
            + extraction.frameworks
            + extraction.databases
            + extraction.tools
        )
        skills = self.normalizer.normalize_all(raw_skills)
        classifications = []
        for profile in self.profiles:
            sorted_skills = sort_qualifications(skills, profile)
            classifications.append(self.classifier.classify(profile.name, sorted_skills))
        return CandidateData(
            full_name=extraction.full_name or UNKNOWN_NAME,
            email=extraction.emails[0] if extraction.emails else None,
            phone=extraction.phones[0] if extraction.phones else None,
            links=extraction.links,
            education=extraction.education,
            experiences=extraction.experiences,
            skills=skills,
            classifications=classifications,
            location=extraction.location,
            current_role=extraction.current_role,
            summary=extraction.summary,
        )

    def generate_report(self, text: str, output_dir: str) -> str:
        candidate = self.analyze(text)
        model = parse_dsl(write_dsl(candidate))
        html = render_html(model)
        file_name = "".join(
            character if character.isalnum() else "_" for character in candidate.full_name
        ).strip("_").lower()
        path = str(Path(output_dir) / f"{file_name or 'candidate'}.html")
        save_html(html, path)
        return path
