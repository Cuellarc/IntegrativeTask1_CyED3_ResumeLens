from pyformlang.fst import FST


# builds a finite-state transducer with one path per variant that outputs the canonical name
def build_transducer(canonical: str, variants: list[str]) -> FST:
    transducer = FST()
    transducer.add_start_state("q0")
    for index, variant in enumerate(variants):
        previous_state = "q0"
        for position, character in enumerate(variant):
            state = f"v{index}_{position + 1}"
            is_last = position == len(variant) - 1
            output = [canonical] if is_last else []
            transducer.add_transition(previous_state, character, state, output)
            previous_state = state
        transducer.add_final_state(previous_state)
    return transducer


def translate_word(transducer: FST, word: str) -> str | None:
    for output in transducer.translate(list(word)):
        if output:
            return output[0]
    return None
