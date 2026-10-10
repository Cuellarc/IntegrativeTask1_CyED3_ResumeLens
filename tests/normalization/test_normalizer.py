import pytest

from resumelens.extraction.regex_extractor import ResumeExtractor
from resumelens.normalization.normalizer import QualificationNormalizer
from resumelens.normalization.variants import QUALIFICATION_VARIANTS
from resumelens.profiles import get_profiles

normalizer = QualificationNormalizer()


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("JS", "JAVASCRIPT"),
        ("Javascript", "JAVASCRIPT"),
        ("React.js", "REACT"),
        ("ReactJS", "REACT"),
        ("NodeJS", "NODE_JS"),
        ("Node.js", "NODE_JS"),
        ("Postgres", "POSTGRESQL"),
        ("PostgreSQL", "POSTGRESQL"),
        ("pandas", "PANDAS"),
        ("sklearn", "SCIKIT_LEARN"),
        ("scikit learn", "SCIKIT_LEARN"),
        ("Scikit-learn", "SCIKIT_LEARN"),
        ("Tensor Flow", "TENSORFLOW"),
        ("TensorFlow", "TENSORFLOW"),
        ("Py Torch", "PYTORCH"),
        ("PyTorch", "PYTORCH"),
        ("k8s", "KUBERNETES"),
        ("Google Cloud Platform", "GCP"),
        ("GitLab CI/CD", "GITLAB_CI"),
        ("Apache Spark", "SPARK"),
    ],
)
def test_normalize_returns_canonical_name(raw, expected):
    assert normalizer.normalize(raw) == expected


def test_normalize_ignores_case_and_extra_spaces():
    assert normalizer.normalize("  SCIKIT    LEARN ") == "SCIKIT_LEARN"


def test_normalize_returns_none_for_unknown_skill():
    assert normalizer.normalize("Photoshop") is None
    assert normalizer.normalize("") is None


def test_normalize_all_removes_unknown_skills_and_duplicates_keeping_order():
    raw_values = ["Git", "NodeJS", "Photoshop", "Node.js", "JS", "git"]
    assert normalizer.normalize_all(raw_values) == ["GIT", "NODE_JS", "JAVASCRIPT"]


def test_every_variant_in_the_catalog_maps_to_its_canonical_name():
    for canonical, variants in QUALIFICATION_VARIANTS.items():
        for variant in variants:
            assert normalizer.normalize(variant) == canonical


def test_no_variant_belongs_to_two_canonical_names():
    variants = [variant for values in QUALIFICATION_VARIANTS.values() for variant in values]
    assert len(variants) == len(set(variants))


def test_catalog_covers_every_qualification_of_every_profile():
    for profile in get_profiles():
        for category in profile.categories:
            for qualification in category.qualifications:
                assert qualification in QUALIFICATION_VARIANTS


def test_normalize_all_on_extracted_skills_of_the_full_stack_fragment():
    text = "Wednesday Addams\n3 years of experience developing web applications.\nTechnical Skills:\nJS, React.js, NodeJS, Postgres, Git.\n"
    result = ResumeExtractor().extract(text)
    raw_values = result.languages + result.frameworks + result.databases + result.tools
    assert normalizer.normalize_all(raw_values) == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
