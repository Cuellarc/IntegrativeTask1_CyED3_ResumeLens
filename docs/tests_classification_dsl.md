# Classification and DSL Test Design

This document describes the main test scenarios for stages 3 and 4 of ResumeLens.

## Classification Test Cases

| ID | Scenario | Input | Expected Result |
|---|---|---|---|
| CL-01 | Valid Full Stack pattern | `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT` | Accepted |
| CL-02 | Valid Machine Learning pattern using TensorFlow | `PYTHON, PANDAS, TENSORFLOW, POSTGRESQL, GIT` | Accepted |
| CL-03 | Valid Machine Learning pattern using Scikit-learn | `PYTHON, PANDAS, SCIKIT_LEARN, SQL, GIT` | Accepted |
| CL-04 | Incomplete Machine Learning pattern | `PYTHON, PANDAS, GIT` | Rejected |
| CL-05 | Full Stack qualifications in incorrect order | `GIT, JAVASCRIPT, REACT, NODE_JS, POSTGRESQL` | Rejected |
| CL-06 | Valid DevOps pattern | `LINUX, DOCKER, JENKINS, AWS, TERRAFORM, GIT` | Accepted |
| CL-07 | Valid Data Engineer pattern | `PYTHON, SQL, SPARK, AIRFLOW, SNOWFLAKE, GIT` | Accepted |
| CL-08 | Empty qualification sequence | Empty list | Rejected |
| CL-09 | Qualification from another profile | Unsupported symbol in the sequence | Rejected |
| CL-10 | DFA state count | Profile with N categories | DFA contains N + 1 states |
| CL-11 | DFA final states | Any supported profile | Exactly one accepting state |
| CL-12 | Unknown profile classification | `UNKNOWN_PROFILE` | `UnknownProfileError` |

## DSL Parser Test Cases

| ID | Scenario | Input | Expected Result |
|---|---|---|---|
| DSL-01 | Valid Full Stack candidate | `valid_full_stack.rlp` | Accepted |
| DSL-02 | Valid Machine Learning candidate | `valid_machine_learning.rlp` | Accepted |
| DSL-03 | Valid DevOps candidate | `valid_devops.rlp` | Accepted |
| DSL-04 | Valid Data Engineer candidate | `valid_data_engineer.rlp` | Accepted |
| DSL-05 | Candidate without accepted profile | `valid_no_classification.rlp` | Accepted |
| DSL-06 | Candidate without email and phone | `valid_no_contact_details.rlp` | Accepted |
| DSL-07 | Invalid email | `invalid_email.rlp` | `InvalidProfileError` |
| DSL-08 | Negative experience years | `invalid_negative_years.rlp` | `InvalidProfileError` |
| DSL-09 | Lowercase qualification | `invalid_lowercase_skill.rlp` | `InvalidProfileError` |
| DSL-10 | Unknown professional profile | `invalid_unknown_profile.rlp` | `InvalidProfileError` |
| DSL-11 | Missing closing brace | `invalid_missing_brace.rlp` | `InvalidProfileError` |
| DSL-12 | Missing candidate name | `invalid_missing_name.rlp` | `InvalidProfileError` |

## DSL Writer Test Cases

| ID | Scenario | Expected Result |
|---|---|---|
| WR-01 | Candidate has accepted and rejected classifications | Only accepted profiles are written |
| WR-02 | Optional fields are absent | Missing fields are omitted from the DSL |
| WR-03 | Candidate contains double quotes | Double quotes are replaced by single quotes |
| WR-04 | Text contains line breaks | Line breaks are converted to spaces |
| WR-05 | Generated DSL is parsed again | Parser accepts the writer output |

## HTML Renderer Test Cases

| ID | Scenario | Expected Result |
|---|---|---|
| HTML-01 | Complete candidate model | Candidate name and expected report sections are displayed |
| HTML-02 | Candidate contains experience information | Role, organization, description and highlights are displayed |
| HTML-03 | Candidate contains normalized skills | Each skill is rendered using the `skill` class |
| HTML-04 | Candidate has an accepted profile | Profile name and `ACCEPTED` are displayed |
| HTML-05 | Optional information is absent | Corresponding optional sections are omitted |
| HTML-06 | Candidate has no accepted classification | `No matching profile` is displayed |
| HTML-07 | HTML report is saved | File is created at the requested path with UTF-8 encoding |

## Testing Strategy

Unit tests are implemented with pytest.

Classification tests construct the profile automata directly and evaluate accepted and rejected qualification sequences.

DSL tests construct `CandidateData` objects directly or use `.rlp` samples. They do not depend on the extraction or normalization stages, allowing stages 3 and 4 to be tested independently.

Valid and invalid DSL samples are used to verify both positive and negative scenarios. Negative tests confirm that lexical and syntactic errors are converted into `InvalidProfileError`.

The HTML tests validate relevant output content instead of depending on a browser. File generation is tested using pytest temporary directories.