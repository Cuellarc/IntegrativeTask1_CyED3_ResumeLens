from resumelens.normalization.transducer_builder import build_transducer, translate_word


def test_translate_word_returns_canonical_name_for_each_variant():
    transducer = build_transducer("JAVASCRIPT", ["javascript", "js"])
    assert translate_word(transducer, "javascript") == "JAVASCRIPT"
    assert translate_word(transducer, "js") == "JAVASCRIPT"


def test_translate_word_outputs_canonical_name_once_when_a_variant_is_a_prefix_of_another():
    transducer = build_transducer("REACT", ["react", "reactjs"])
    assert translate_word(transducer, "react") == "REACT"
    assert list(transducer.translate(list("reactjs"))) == [["REACT"]]


def test_translate_word_returns_none_for_unknown_word():
    transducer = build_transducer("GIT", ["git"])
    assert translate_word(transducer, "github") is None
    assert translate_word(transducer, "gi") is None
    assert translate_word(transducer, "") is None


def test_build_transducer_creates_one_final_state_per_variant():
    transducer = build_transducer("NODE_JS", ["nodejs", "node.js", "node"])
    assert len(transducer.final_states) == 3
    assert len(transducer.start_states) == 1


def test_build_transducer_creates_one_state_per_character_plus_initial_state():
    transducer = build_transducer("SQL", ["sql", "psql"])
    assert len(transducer.states) == 1 + len("sql") + len("psql")


def test_build_transducer_alphabets_match_variants_and_canonical_name():
    transducer = build_transducer("GIT", ["git", "g"])
    assert set(transducer.input_symbols) == {"g", "i", "t"}
    assert set(transducer.output_symbols) == {"GIT"}
