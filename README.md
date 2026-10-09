# ResumeLens: Formal Language-Based Resume Screening

Integrative Task 1 - Computación y Estructuras Discretas III (CyED3), 2026-2
Universidad Icesi - Departamento de CSI

## Team

**Team name:** ParSeros

| Member | Student code |
|---|---|
| Juan Esteban Cuéllar | A00402548 |
| Juan Pablo Sinisterra | - |

**Course group:** 3 (Professor Andrés)

## About the project

Recruitment processes require reviewing many résumés to check whether candidates satisfy the qualifications expected for a professional profile. Résumés contain similar kinds of information (education, experience, technical skills, contact data), but they are written in very different ways. The same qualification can appear under several names: `JavaScript`, `Javascript` and `JS` are the same language, and `Scikit-learn`, `sklearn` and `scikit learn` are the same library.

**ResumeLens** is an application that processes textual résumés and determines whether the qualifications explicitly found in them satisfy a formally defined qualification pattern for a professional profile. It does not rank candidates and it does not make hiring decisions.

## Supported professional profiles

The four profiles are processed by the same general solution, not by independent implementations.

| Profile | Origin |
|---|---|
| Full Stack Developer | Predefined |
| Machine Learning Engineer | Predefined |
| DevOps Engineer | Chosen by the team (software engineering) |
| Data Engineer | Chosen by the team (AI/data) |

## Formal models

ResumeLens is organized in four stages, each one based on a formal language model:

| Stage | Goal | Formal model | Library |
|---|---|---|---|
| 1. Extraction | Extract candidate data and possible qualifications from résumé text | Regular expressions | `re` |
| 2. Normalization | Transform equivalent spellings into one canonical form (for example `JS` and `Javascript` into `JAVASCRIPT`) | Finite-state transducers | `pyformlang` |
| 3. Classification | Recognize whether the normalized qualifications satisfy the pattern of each profile | Finite automata | `pyformlang` |
| 4. Candidate profile language | Define and validate a structured representation of the candidate, and generate an HTML visualization | Context-free grammar | `textX` |

## Documentation

The design documents (module design, formalization and test cases) are placed in the [docs/](docs/) directory and are written in Markdown.

## Project status

The project is under development. Usage instructions will be added to this file as each component is implemented.
