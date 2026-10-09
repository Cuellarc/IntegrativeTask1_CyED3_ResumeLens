from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProfileCategory:
    name: str
    qualifications: tuple[str, ...]


@dataclass(frozen=True)
class Profile:
    name: str
    display_name: str
    categories: tuple[ProfileCategory, ...]


@dataclass
class ExperienceRecord:
    years: int
    description: str
    role: str | None = None
    organization: str | None = None
    highlights: list[str] = field(default_factory=list)


@dataclass
class ExtractionResult:
    full_name: str | None = None
    emails: list[str] = field(default_factory=list)
    phones: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    location: str | None = None
    current_role: str | None = None
    summary: str | None = None
    education: list[str] = field(default_factory=list)
    experiences: list[ExperienceRecord] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    databases: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)


@dataclass
class ClassificationResult:
    profile_name: str
    accepted: bool
    qualifications: list[str]


@dataclass
class CandidateData:
    full_name: str
    email: str | None
    phone: str | None
    links: list[str]
    education: list[str]
    experiences: list[ExperienceRecord]
    skills: list[str]
    classifications: list[ClassificationResult]
    location: str | None = None
    current_role: str | None = None
    summary: str | None = None
