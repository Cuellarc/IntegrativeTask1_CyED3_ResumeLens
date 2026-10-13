import tkinter as tk

import pytest

from resumelens.ui.app import ResumeLensApp


@pytest.fixture
def app():
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available")
    root.withdraw()
    yield ResumeLensApp(root)
    root.destroy()


def test_analyze_shows_the_accepted_profile_and_enables_the_report_button(app):
    app.resume_input.insert("1.0", "Wednesday Addams\nTechnical Skills:\nGit, NodeJS, JS, Postgres, React.js.\n")
    app.analyze()
    result = app.result_output.get("1.0", tk.END)
    assert "Wednesday Addams" in result
    assert "Full Stack Developer: ACCEPTED" in result
    assert "Machine Learning Engineer: REJECTED" in result
    assert str(app.report_button.cget("state")) == "normal"


def test_clear_empties_both_panels_and_disables_the_report_button(app):
    app.resume_input.insert("1.0", "Ana Perez\nTechnical Skills:\nGit.\n")
    app.analyze()
    app.clear()
    assert app.resume_input.get("1.0", tk.END).strip() == ""
    assert app.result_output.get("1.0", tk.END).strip() == ""
    assert str(app.report_button.cget("state")) == "disabled"
