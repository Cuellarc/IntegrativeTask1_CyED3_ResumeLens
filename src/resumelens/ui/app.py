import ctypes
import sys
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from resumelens.errors import ResumeLensError
from resumelens.pipeline import ResumeAnalyzer
from resumelens.profiles import get_profile

OUTPUT_DIRECTORY = "output"

BACKGROUND = "#1e1e1e"
PANEL = "#252526"
BUTTON = "#3c3c3c"
BUTTON_ACTIVE = "#505050"
TEXT = "#ffffff"
DISABLED_TEXT = "#808080"


class ResumeLensApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.analyzer = ResumeAnalyzer()
        self.report_path: str | None = None
        self.root.title("ResumeLens")
        self.root.geometry("980x620")
        self.root.configure(bg=BACKGROUND)
        self.apply_theme()
        self.build_layout()
        self.darken_title_bar()

    def darken_title_bar(self) -> None:
        if sys.platform != "win32":
            return
        try:
            self.root.update_idletasks()
            handle = ctypes.windll.user32.GetParent(self.root.winfo_id())
            for attribute, value in ((20, 1), (35, 0x001E1E1E), (36, 0x00FFFFFF)):
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    handle, attribute, ctypes.byref(ctypes.c_int(value)), ctypes.sizeof(ctypes.c_int)
                )
        except (AttributeError, OSError):
            return

    def apply_theme(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background=BACKGROUND)
        style.configure("TLabel", background=BACKGROUND, foreground=TEXT)
        style.configure(
            "TButton",
            background=BUTTON,
            foreground=TEXT,
            bordercolor=BUTTON,
            lightcolor=BUTTON,
            darkcolor=BUTTON,
            padding=6,
        )
        style.map(
            "TButton",
            background=[("active", BUTTON_ACTIVE), ("disabled", BACKGROUND)],
            foreground=[("disabled", DISABLED_TEXT)],
        )

    def create_text(self, parent: ttk.Frame, **options) -> tk.Text:
        return tk.Text(
            parent,
            wrap=tk.WORD,
            width=50,
            bg=PANEL,
            fg=TEXT,
            insertbackground=TEXT,
            selectbackground=BUTTON_ACTIVE,
            relief=tk.FLAT,
            padx=8,
            pady=8,
            **options,
        )

    def build_layout(self) -> None:
        left = ttk.Frame(self.root, padding=10)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right = ttk.Frame(self.root, padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(left, text="Resume text").pack(anchor=tk.W)
        self.resume_input = self.create_text(left)
        self.resume_input.pack(fill=tk.BOTH, expand=True)

        buttons = ttk.Frame(left)
        buttons.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(buttons, text="Load file", command=self.load_file).pack(side=tk.LEFT)
        ttk.Button(buttons, text="Analyze", command=self.analyze).pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons, text="Clear", command=self.clear).pack(side=tk.LEFT)

        ttk.Label(right, text="Result").pack(anchor=tk.W)
        self.result_output = self.create_text(right, state=tk.DISABLED)
        self.result_output.pack(fill=tk.BOTH, expand=True)
        self.report_button = ttk.Button(
            right, text="Generate and open HTML report", command=self.open_report, state=tk.DISABLED
        )
        self.report_button.pack(fill=tk.X, pady=(8, 0))

    def load_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            self.resume_input.delete("1.0", tk.END)
            self.resume_input.insert("1.0", Path(path).read_text(encoding="utf-8"))

    def clear(self) -> None:
        self.resume_input.delete("1.0", tk.END)
        self.show_result("")
        self.report_button.config(state=tk.DISABLED)

    def show_result(self, text: str) -> None:
        self.result_output.config(state=tk.NORMAL)
        self.result_output.delete("1.0", tk.END)
        self.result_output.insert("1.0", text)
        self.result_output.config(state=tk.DISABLED)

    def analyze(self) -> None:
        text = self.resume_input.get("1.0", tk.END)
        if not text.strip():
            messagebox.showwarning("ResumeLens", "Paste or load a resume first.")
            return
        candidate = self.analyzer.analyze(text)
        lines = [f"Candidate: {candidate.full_name}", ""]
        lines.append("Normalized qualifications:")
        lines.append(", ".join(candidate.skills) if candidate.skills else "none recognized")
        lines.append("")
        lines.append("Profile evaluation:")
        for item in candidate.classifications:
            status = "ACCEPTED" if item.accepted else "REJECTED"
            display_name = get_profile(item.profile_name).display_name
            sequence = ", ".join(item.qualifications) if item.qualifications else "empty sequence"
            lines.append(f"- {display_name}: {status}")
            lines.append(f"  sequence: {sequence}")
        self.show_result("\n".join(lines))
        self.report_button.config(state=tk.NORMAL)

    def open_report(self) -> None:
        text = self.resume_input.get("1.0", tk.END)
        try:
            self.report_path = self.analyzer.generate_report(text, OUTPUT_DIRECTORY)
        except ResumeLensError as error:
            messagebox.showerror("ResumeLens", f"The report could not be generated:\n{error}")
            return
        webbrowser.open(Path(self.report_path).resolve().as_uri())


def run() -> None:
    root = tk.Tk()
    ResumeLensApp(root)
    root.mainloop()
