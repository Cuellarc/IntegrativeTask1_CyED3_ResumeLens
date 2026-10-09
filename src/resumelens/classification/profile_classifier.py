from pyformlang.finite_automaton import DeterministicFiniteAutomaton

from resumelens.classification.profile_automata import (
    accepts_pattern,
    build_profile_automaton,
)
from resumelens.errors import UnknownProfileError
from resumelens.models import ClassificationResult, Profile


class ProfileClassifier:
    def __init__(self, profiles: list[Profile]) -> None:
        self.automata: dict[str, DeterministicFiniteAutomaton] = {}

        for profile in profiles:
            self.automata[profile.name] = build_profile_automaton(profile)

    # Classifies an ordered qualification sequence for a profile.
    def classify(
        self,
        profile_name: str,
        sorted_qualifications: list[str],
    ) -> ClassificationResult:
        if profile_name not in self.automata:
            raise UnknownProfileError(profile_name)

        accepted = accepts_pattern(
            self.automata[profile_name],
            sorted_qualifications,
        )

        return ClassificationResult(
            profile_name=profile_name,
            accepted=accepted,
            qualifications=list(sorted_qualifications),
        )