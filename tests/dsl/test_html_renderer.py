from resumelens.dsl.dsl_parser import parse_dsl
from resumelens.dsl.html_renderer import render_html, save_html


def _full_candidate_model() -> object:
    return parse_dsl(
        '''
        candidate "Wednesday Addams" {
            contact {
                email: "wednesday.addams@example.com"
                phone: "+57 300 123 4567"
                link: "https://github.com/wednesday"
            }

            location: "Nevermore Academy, Jericho"
            role: "Web Application Developer"
            summary: "Detail-oriented developer."

            education {
                "Bachelor in Computer Science"
            }

            experience {
                3 years "Developing web applications."
                role "Web Application Developer"
                organization "Nevermore Academy Projects" {
                    "Implemented backend services using Node.js."
                    "Stored structured information using PostgreSQL."
                }
            }

            skills {
                JAVASCRIPT,
                REACT,
                NODE_JS,
                POSTGRESQL,
                GIT
            }

            classification {
                FULL_STACK_DEVELOPER: ACCEPTED [
                    JAVASCRIPT,
                    REACT,
                    NODE_JS,
                    POSTGRESQL,
                    GIT
                ]
            }
        }
        '''
    )


def test_renderer_contains_candidate_sections() -> None:
    html = render_html(_full_candidate_model())

    assert "Wednesday Addams" in html
    assert "Personal Information" in html
    assert "Profile Summary" in html
    assert "Education" in html
    assert "Experience" in html
    assert "Normalized Technical Skills" in html
    assert "Qualification Evaluation" in html


def test_renderer_contains_experience_skills_and_classification() -> None:
    html = render_html(_full_candidate_model())

    assert "Web Application Developer" in html
    assert "Nevermore Academy Projects" in html
    assert "Implemented backend services using Node.js." in html

    assert "JAVASCRIPT" in html
    assert "REACT" in html
    assert "NODE_JS" in html
    assert "POSTGRESQL" in html
    assert "GIT" in html

    assert "Full Stack Developer" in html
    assert "ACCEPTED" in html

    assert 'class="metadata"' in html
    assert 'class="skill"' in html
    assert 'class="evaluation"' in html
    assert 'class="accepted"' in html


def test_renderer_omits_missing_optional_sections() -> None:
    model = parse_dsl(
        '''
        candidate "Minimal Candidate" {
            skills {
                PYTHON
            }
        }
        '''
    )

    html = render_html(model)

    assert "Minimal Candidate" in html
    assert "Personal Information" not in html
    assert "Profile Summary" not in html
    assert "Education" not in html
    assert "Experience" not in html

    assert "Normalized Technical Skills" in html
    assert "Qualification Evaluation" in html
    assert "No matching profile" in html


def test_save_html_writes_file(tmp_path) -> None:
    html = render_html(_full_candidate_model())
    output_path = tmp_path / "reports" / "candidate.html"

    save_html(html, str(output_path))

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == html