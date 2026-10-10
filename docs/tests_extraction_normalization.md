# Test Design: Extraction and Normalization (Stages 1 and 2)

The tests are written with `pytest`. Run them from the project root with:

```
python -m pytest
```

Every test below exists in the repository. The test names are the function names. The sample resumes used as fixtures are in `data/resumes/`.

## 1. Sample resumes

| File | Scenario | Expected profile result (planned for the pipeline tests) |
|---|---|---|
| `resume_full_stack_developer_1.txt` | Complete resume with all the labeled fields | Accepted: Full Stack Developer |
| `resume_full_stack_developer_2.txt` | Simple fragment from the assignment (Wednesday Addams) | Accepted: Full Stack Developer |
| `resume_machine_learning_engineer_1.txt` | Simple fragment from the assignment (Mary Jane Watson) | Accepted: Machine Learning Engineer |
| `resume_devops_engineer_1.txt` | DevOps resume with experience bullets | Accepted: DevOps Engineer |
| `resume_data_engineer_1.txt` | Data engineering resume with a master degree | Accepted: Data Engineer |
| `resume_multi_profile_1.txt` | Skills of two profiles in one resume | Accepted: Full Stack Developer and Machine Learning Engineer |
| `resume_no_profile_1.txt` | Graphic designer, no technical skills of the supported profiles | No profile accepted |

## 2. Stage 1: extraction (`tests/extraction/test_resume_extractor.py`)

| ID | Test | Scenario | Input | Expected result |
|---|---|---|---|---|
| E-01 | `test_extract_name_returns_first_line_name` | Name on the first line | `Mary Jane Watson` followed by a header | `"Mary Jane Watson"` |
| E-02 | `test_extract_name_returns_none_when_first_line_is_not_a_name` | First line is not a name | `technical skills:` and a skill line | `None` |
| E-03 | `test_extract_contacts_finds_email_phone_and_links` | Contact data with country code | Full stack resume 1 | One e-mail, phone `+57 300 123 4567`, one GitHub link |
| E-04 | `test_extract_contacts_finds_phone_without_country_code` | Phone without country code | DevOps resume | `310 555 1234` |
| E-05 | `test_extract_skills_from_full_stack_fragment` | Raw spellings of the assignment | Full stack resume 2 | languages `JS`; frameworks `React.js`, `NodeJS`; databases `Postgres`; tools `Git` |
| E-06 | `test_extract_skills_from_machine_learning_fragment` | Machine learning skills | ML resume | `Python`; `Pandas`, `NumPy`, `Scikit-learn`, `TensorFlow`; `SQL`; `Git` |
| E-07 | `test_extract_skills_from_devops_resume` | Tools found in the text and in bullets | DevOps resume | `Jenkins`, `Docker`, `Kubernetes`, `AWS`, `Terraform`, `Linux`, `Git` in order of appearance |
| E-08 | `test_extract_skills_from_data_engineering_resume` | Data engineering skills | Data engineer resume | `Python`; `Spark`, `Airflow`; `Snowflake`, `SQL` |
| E-09 | `test_extract_skills_does_not_match_inside_other_words` | Skill inside another word | `PostgreSQL and NoSQL, using Projects` | databases `["PostgreSQL"]`, no languages |
| E-10 | `test_extract_experience_from_sentence` | Simple experience sentence | Full stack resume 2 | `ExperienceRecord(3, "developing web applications")` |
| E-11 | `test_extract_experience_sentence_without_description_uses_default` | Sentence without text after it | `4 years of experience.` | `ExperienceRecord(4, "professional experience")` |
| E-12 | `test_extract_experience_from_header_with_highlights` | Structured experience | Full stack resume 1 | Role, organization, 3 years and 4 highlights |
| E-13 | `test_extract_several_experiences_keeps_highlights_separated` | Two experiences | Two headers with one bullet each | Years `[2, 1]` and each bullet under its own experience |
| E-14 | `test_extract_location_role_and_summary` | Labeled fields | Full stack resume 1 | Location, current role and the two-line summary joined in one string |
| E-15 | `test_extract_education` | Education line | Data engineer resume | `["Master in Data Science - Universidad Icesi"]` |
| E-16 | `test_extract_handles_windows_line_endings` | `\r\n` line endings | Full stack resume 1 with `\r\n` | Same name and location as with `\n` |
| E-17 | `test_extract_full_resume_fills_every_field` | Complete result | Full stack resume 1 | Name, education, languages, frameworks, databases and tools |
| E-18 | `test_extract_unrecognizable_text_returns_empty_result` | Nothing recognizable | `???` and `123` | Empty `ExtractionResult` and no name |
| E-19 | `test_extract_resume_without_technical_skills_returns_no_skills` | Resume outside the supported profiles | No-profile resume | Name and role found, no skills |
| E-20 | `test_extract_skills_from_multi_profile_resume` | Skills of two profiles | Multi-profile resume | `JavaScript`, `Python`, `JS`; `React`, `Node.js`, `Pandas`, `TensorFlow`, `ReactJS`; `PostgreSQL`; `Git` |

## 3. Stage 2: transducers (`tests/normalization/test_transducer_builder.py`)

| ID | Test | Scenario | Input | Expected result |
|---|---|---|---|---|
| T-01 | `test_translate_word_returns_canonical_name_for_each_variant` | Every variant is translated | `javascript`, `js` | `JAVASCRIPT` |
| T-02 | `test_translate_word_outputs_canonical_name_once_when_a_variant_is_a_prefix_of_another` | A variant is a prefix of another one | `react`, `reactjs` | `REACT` once, never twice |
| T-03 | `test_translate_word_returns_none_for_unknown_word` | Word outside the language | `github`, `gi`, empty text with variant `git` | `None` |
| T-04 | `test_build_transducer_creates_one_final_state_per_variant` | Accepting states | Three variants of `NODE_JS` | 3 final states and 1 initial state |
| T-05 | `test_build_transducer_creates_one_state_per_character_plus_initial_state` | Number of states | `sql`, `psql` | `1 + 3 + 4` states |
| T-06 | `test_build_transducer_alphabets_match_variants_and_canonical_name` | Alphabets | `git`, `g` | Input alphabet `{g, i, t}` and output alphabet `{GIT}` |

## 4. Stage 2: normalizer (`tests/normalization/test_normalizer.py`)

| ID | Test | Scenario | Input | Expected result |
|---|---|---|---|---|
| N-01 | `test_normalize_returns_canonical_name` (20 cases) | Spellings of the assignment and extra ones | `JS`, `Javascript`, `React.js`, `ReactJS`, `NodeJS`, `Node.js`, `Postgres`, `PostgreSQL`, `pandas`, `sklearn`, `scikit learn`, `Scikit-learn`, `Tensor Flow`, `TensorFlow`, `Py Torch`, `PyTorch`, `k8s`, `Google Cloud Platform`, `GitLab CI/CD`, `Apache Spark` | `JAVASCRIPT`, `JAVASCRIPT`, `REACT`, `REACT`, `NODE_JS`, `NODE_JS`, `POSTGRESQL`, `POSTGRESQL`, `PANDAS`, `SCIKIT_LEARN`, `SCIKIT_LEARN`, `SCIKIT_LEARN`, `TENSORFLOW`, `TENSORFLOW`, `PYTORCH`, `PYTORCH`, `KUBERNETES`, `GCP`, `GITLAB_CI`, `SPARK` |
| N-02 | `test_normalize_ignores_case_and_extra_spaces` | Case and spaces | `"  SCIKIT    LEARN "` | `SCIKIT_LEARN` |
| N-03 | `test_normalize_returns_none_for_unknown_skill` | Unknown skill and empty text | `Photoshop`, empty text | `None` |
| N-04 | `test_normalize_all_removes_unknown_skills_and_duplicates_keeping_order` | List with noise | `Git`, `NodeJS`, `Photoshop`, `Node.js`, `JS`, `git` | `GIT`, `NODE_JS`, `JAVASCRIPT` |
| N-05 | `test_every_variant_in_the_catalog_maps_to_its_canonical_name` | Whole catalog | Every variant | Its canonical name |
| N-06 | `test_no_variant_belongs_to_two_canonical_names` | Ambiguity in the catalog | Whole catalog | No repeated variant |
| N-07 | `test_catalog_covers_every_qualification_of_every_profile` | Coverage of the profiles | Four profiles | Every qualification has an entry in the catalog |
| N-08 | `test_normalize_all_on_extracted_skills_of_the_full_stack_fragment` | Stage 1 plus Stage 2 | Assignment fragment | `JAVASCRIPT`, `REACT`, `NODE_JS`, `POSTGRESQL`, `GIT` |

## 5. Stage 2: sorter (`tests/normalization/test_qualification_sorter.py`)

| ID | Test | Scenario | Input | Expected result |
|---|---|---|---|---|
| S-01 | `test_sort_qualifications_follows_the_category_order_of_the_profile` | Unordered input | `GIT`, `NODE_JS`, `JAVASCRIPT`, `POSTGRESQL`, `REACT` with Full Stack | `JAVASCRIPT`, `REACT`, `NODE_JS`, `POSTGRESQL`, `GIT` |
| S-02 | `test_sort_qualifications_skips_categories_without_a_match` | Missing categories | `GIT`, `PYTHON` with Machine Learning | `PYTHON`, `GIT` |
| S-03 | `test_sort_qualifications_discards_qualifications_outside_the_profile` | Foreign qualifications | `DOCKER`, `GIT`, `PYTHON` with Full Stack | `GIT` |
| S-04 | `test_sort_qualifications_keeps_one_qualification_per_category_by_priority` | Several options in one category | Eight qualifications with Machine Learning | `PYTHON`, `PANDAS`, `SCIKIT_LEARN`, `SQL`, `GIT` |
| S-05 | `test_sort_qualifications_returns_empty_list_for_empty_input` | Empty input | Empty list with Data Engineer | Empty list |
| S-06 | `test_sort_qualifications_depends_on_the_selected_profile` | Same input, two profiles | `PANDAS`, `PYTHON`, `GIT`, `SQL` | Machine Learning: `PYTHON`, `PANDAS`, `SQL`, `GIT`; Data Engineer: `PYTHON`, `SQL`, `PANDAS`, `GIT` |

## 6. Coverage summary

| Area | Tests |
|---|---|
| Stage 1 extraction | 20 |
| Transducer builder | 6 |
| Normalizer (the first one has 20 parametrized cases) | 8 test functions |
| Sorter | 6 |

Pipeline tests that use the sample resumes of section 1 are designed in the pipeline documentation once the full flow is integrated.
