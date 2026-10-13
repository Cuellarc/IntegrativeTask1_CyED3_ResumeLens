# ResumeLens: Formal Language-Based Resume Screening

Integrative Task 1 - Computación y Estructuras Discretas III (CyED3), 2026-2
Universidad Icesi - Departamento de CSI

## Team: **ParSeros**

| Member | Student code |
|---|---|
| Juan Esteban Cuéllar | A00402548 |
| Juan Pablo Sinisterra | A00402333 |

**Course group:** 3 (Professor Andrés)

## About the project

Recruitment processes require reviewing many résumés to check whether candidates satisfy the qualifications expected for a professional profile. Résumés contain similar kinds of information (education, experience, technical skills, contact data), but they are written in very different ways. The same qualification can appear under several names: `JavaScript`, `Javascript` and `JS` are the same language, and `Scikit-learn`, `sklearn` and `scikit learn` are the same library.

**ResumeLens** is an application that processes textual résumés and determines whether the qualifications explicitly found in them satisfy a formally defined qualification pattern for a professional profile. It does not rank candidates and it does not make hiring decisions.

## Supported professional profiles

The four profiles are processed by the same general solution, not by independent implementations. A profile is defined as data (an ordered list of categories, each one with its accepted qualifications) in `src/resumelens/profiles.py`.

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

## Development environment

- **Language:** Python 3.11 or newer (developed with Python 3.12)
- **IDE:** Visual Studio Code
- **Libraries:** `pyformlang`, `textX`, `pytest` (listed in `requirements.txt`)
- **Version control:** Git and GitHub, with one branch per feature merged into `main` through pull requests

## Installation

From the project root:

```
python -m venv .venv
```

Activate the virtual environment (Windows PowerShell: `.venv\Scripts\Activate.ps1`, Linux or macOS: `source .venv/bin/activate`) and install the dependencies:

```
pip install -r requirements.txt
```

## Running the tests

```
python -m pytest
```

`pytest.ini` already adds `src` to the Python path, so no further configuration is needed.

## Running the application

From the project root, with the virtual environment active:

```
python main.py
```

A window opens with two panels. Paste a résumé (or use **Load file**, for example one from `data/resumes/`) and press **Analyze**. The right panel shows the candidate name, the normalized qualifications and, for each of the four profiles, whether the sorted sequence is `ACCEPTED` or `REJECTED`. **Generate and open HTML report** validates the candidate with the DSL grammar and opens the HTML visualization in the browser. The file is saved in `output/`.

A résumé in which no qualification is recognized cannot produce a report, because the candidate profile grammar requires at least one skill. The analysis panel still shows the result.

## Using the stages from Python

```python
from resumelens.pipeline import ResumeAnalyzer

analyzer = ResumeAnalyzer()
candidate = analyzer.analyze(open("data/resumes/resume_full_stack_developer_2.txt").read())
print(candidate.skills)
print([item.profile_name for item in candidate.classifications if item.accepted])
path = analyzer.generate_report(open("data/resumes/resume_full_stack_developer_2.txt").read(), "output")
```

Run it with `src` on the Python path (Windows PowerShell: `$env:PYTHONPATH = "src"`, Linux or macOS: `export PYTHONPATH=src`). For the assignment example (`Git, NodeJS, JS, Postgres, React.js`), Stage 1 returns the strings as written, Stage 2 rewrites them into canonical names and the sorting puts them in the order of the profile, which gives `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT`. Because of the sorting, the result does not depend on the order written by the candidate.

## Accepted résumé format

The extractor reads plain text. The simple format from the assignment works, and these optional labeled fields are also recognized:

```
Wednesday Addams
Location: Nevermore Academy, Jericho
Current role: Student and independent investigator
Email: wednesday.addams@example.com
Phone: +57 300 123 4567
GitHub: https://github.com/wednesday-addams

Summary:
Detail-oriented developer with three years of experience developing web applications.

Education:
Bachelor in Computer Science - Nevermore Academy

Experience:
Web Application Developer - Nevermore Academy Projects (3 years)
- Developed web applications for organizing investigation notes.
- Implemented backend services using Node.js.

Technical Skills:
JS, React.js, NodeJS, Postgres, Git.
```

Sample résumés for every profile are in [data/resumes/](data/resumes/).

## Project structure

```
main.py                  starts the user interface
src/resumelens/
|-- models.py            data structures shared by all stages
|-- profiles.py          the four profiles, defined as data
|-- errors.py            project exceptions
|-- pipeline.py          ResumeAnalyzer: runs the four stages in order
|-- extraction/          Stage 1: regular expressions
|-- normalization/       Stage 2: transducers, spelling catalog and sorting
|-- classification/      Stage 3: finite automata
|-- dsl/                 Stage 4: candidate profile grammar (textX) and HTML
`-- ui/                  Tkinter user interface
tests/                   tests of each stage, the pipeline and the interface
data/resumes/            sample résumés
data/profiles_dsl/       valid and invalid candidate profile samples
docs/                    design documents
```

## Documentation

The design documents are in the [docs/](docs/) directory, written in Markdown:

| Document | Content |
|---|---|
| [architecture.md](docs/architecture.md) | Components, data flow and design decisions |
| [modules_extraction_normalization.md](docs/modules_extraction_normalization.md) | Modules of Stages 1 and 2 with inputs and outputs |
| [formalization_extraction_normalization.md](docs/formalization_extraction_normalization.md) | Regular expressions and transducers (7-tuples and diagrams) |
| [tests_extraction_normalization.md](docs/tests_extraction_normalization.md) | Test cases of Stages 1 and 2 |
| [literature_review.md](docs/literature_review.md) | Literature review |
| [transducer_catalog.md](docs/transducer_catalog.md) | Complete 7-tuple and diagram of each of the 41 transducers |
| [ResumeLens-Poster.pdf](poster/ResumeLens-Poster.pdf) | Research poster |

## Project status

| Stage | Status |
|---|---|
| 1. Extraction | Implemented and tested |
| 2. Normalization | Implemented and tested |
| 3. Classification | Implemented and tested |
| 4. Candidate profile language and HTML | Implemented and tested |
| Pipeline and user interface | Implemented and tested |
