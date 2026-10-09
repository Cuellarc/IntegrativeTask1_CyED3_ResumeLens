from pyformlang.fst import FST

from resumelens.normalization.transducer_builder import build_transducer, translate_word
from resumelens.normalization.variants import QUALIFICATION_VARIANTS


class QualificationNormalizer:
    def __init__(self) -> None:
        self.transducers: dict[str, FST] = {
            canonical: build_transducer(canonical, variants)
            for canonical, variants in QUALIFICATION_VARIANTS.items()
        }

    # tries every transducer on the raw skill and returns its canonical name
    def normalize(self, raw: str) -> str | None:
        word = " ".join(raw.lower().split())
        for transducer in self.transducers.values():
            canonical = translate_word(transducer, word)
            if canonical:
                return canonical
        return None

    def normalize_all(self, raw_values: list[str]) -> list[str]:
        normalized = []
        for raw in raw_values:
            canonical = self.normalize(raw)
            if canonical is not None and canonical not in normalized:
                normalized.append(canonical)
        return normalized
