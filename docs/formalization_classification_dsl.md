# ResumeLens Formalization: Classification and Candidate Profile DSL

## 1. Qualification Pattern Recognition with Finite Automata

ResumeLens uses deterministic finite automata to determine whether a sequence of normalized qualifications satisfies the qualification pattern defined for a professional profile.

A single general construction is used for every profile. If a profile contains `N` ordered qualification categories, the corresponding automaton contains states `q0, q1, ..., qN`. State `q0` is the initial state and `qN` is the only accepting state.

For each category, every valid qualification produces a transition from the state associated with that category to the next state. Therefore, a candidate is accepted only when the input contains one valid qualification from every required category and follows the canonical category order.

The transition function is deterministic and partial. When no transition exists for a state-symbol pair, the sequence is rejected.

---

## 1.1 Full Stack Developer

### Formal Definition

The automaton is defined as:

**M_FS = (Q, Σ, δ, q0, F)**

where:

**Q**

```text
Q = {q0, q1, q2, q3, q4, q5}

---

## 2. Candidate Profile Domain-Specific Language

After the extraction, normalization, and classification stages, ResumeLens represents the processed candidate information using a domain-specific language.

The language is implemented with textX and describes the structured information of a candidate, including personal information, contact information, education, professional experience, normalized technical skills, and accepted professional profiles.

The DSL is designed to represent the result produced by ResumeLens rather than the original résumé text.

---

## 2.1 EBNF Grammar

The candidate profile language can be represented using the following EBNF notation:

```ebnf
CandidateProfile =
    "candidate", STRING, "{",
        [ Contact ],
        [ Location ],
        [ Role ],
        [ Summary ],
        [ Education ],
        { Experience },
        Skills,
        [ Classification ],
    "}";

Contact =
    "contact", "{",
        [ "email", ":", EMAIL ],
        [ "phone", ":", PHONE ],
        { "link", ":", STRING },
    "}";

Location =
    "location", ":", STRING;

Role =
    "role", ":", STRING;

Summary =
    "summary", ":", STRING;

Education =
    "education", "{",
        { STRING },
    "}";

Experience =
    "experience", "{",
        NON_NEGATIVE_INT, "years",
        STRING,
        [ "role", STRING ],
        [ "organization", STRING ],
        [ Highlights ],
    "}";

Highlights =
    "{",
        { STRING },
    "}";

Skills =
    "skills", "{",
        QUALIFICATION,
        { ",", QUALIFICATION },
    "}";

Classification =
    "classification", "{",
        { ClassificationEntry },
    "}";

ClassificationEntry =
    PROFILE_NAME,
    ":",
    "ACCEPTED",
    "[",
        QUALIFICATION,
        { ",", QUALIFICATION },
    "]";

PROFILE_NAME =
      "FULL_STACK_DEVELOPER"
    | "MACHINE_LEARNING_ENGINEER"
    | "DEVOPS_ENGINEER"
    | "DATA_ENGINEER";

STRING =
    '"', TEXT, '"';

TEXT =
    character sequence excluding double quotes and line breaks;

EMAIL =
    valid local-part,
    "@",
    valid domain,
    ".",
    alphabetic top-level domain;

PHONE =
    [ "+" ],
    digit,
    { digit | space | "(" | ")" | "-" },
    digit;

QUALIFICATION =
    uppercase letter,
    { uppercase letter | digit | "_" };

NON_NEGATIVE_INT =
    "0"
    | non-zero digit, { digit };