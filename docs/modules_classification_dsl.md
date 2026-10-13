# Classification and DSL Module Design

This document describes the modules implemented for stages 3 and 4 of ResumeLens.

## Classification Modules

| Module | Function or Class | Input | Output | Responsibility |
|---|---|---|---|---|
| `profile_automata.py` | `build_profile_automaton(profile)` | `Profile` | `DeterministicFiniteAutomaton` | Builds a DFA from the ordered qualification categories of a professional profile. |
| `profile_automata.py` | `accepts_pattern(automaton, qualifications)` | DFA and `list[str]` | `bool` | Determines whether an ordered qualification sequence is accepted by the DFA. |
| `profile_classifier.py` | `ProfileClassifier` | `list[Profile]` | Classifier instance | Creates and stores one DFA for every supported professional profile. |
| `profile_classifier.py` | `classify(profile_name, sorted_qualifications)` | Profile name and ordered qualifications | `ClassificationResult` | Evaluates the sequence using the corresponding profile automaton. |

## DSL Modules

| Module | Function or Component | Input | Output | Responsibility |
|---|---|---|---|---|
| `candidate_profile.tx` | Candidate profile grammar | DSL text | textX model definition | Defines the lexical and syntactic structure of the candidate profile language. |
| `dsl_writer.py` | `write_dsl(candidate)` | `CandidateData` | `str` | Converts structured candidate information into valid ResumeLens DSL text. |
| `dsl_parser.py` | `parse_dsl(text)` | DSL string | textX model | Parses and validates DSL text using the candidate profile grammar. |
| `dsl_parser.py` | `parse_dsl_file(path)` | File path | textX model | Loads and validates a candidate profile DSL file. |
| `html_renderer.py` | `render_html(model)` | Validated textX model | `str` | Generates the candidate HTML report. |
| `html_renderer.py` | `save_html(html, path)` | HTML string and output path | `None` | Creates the required directories and stores the report using UTF-8. |

## Stage 3 Data Flow

The classification stage receives normalized qualifications that have already been sorted according to the categories of a professional profile.

```text
Normalized qualifications
        |
        v
Profile categories
        |
        v
DFA construction
        |
        v
Pattern recognition
        |
        v
ClassificationResult