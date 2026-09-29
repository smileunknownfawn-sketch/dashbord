from __future__ import annotations

import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk

try:
    from PIL import Image, ImageTk, ImageOps
except Exception:
    Image = None
    ImageTk = None
    ImageOps = None

from desktop_release import ReleaseDashboard


class FullReleaseDashboard(ReleaseDashboard):
    """Release UI with automatic, uncropped language-image preview."""

    def __init__(self) -> None:
        self.language = "Українська"
        self._language_photo = None
        self._language_source_image = None
        super().__init__()
        self.withdraw()
        self.after(80, self._show_language_gate)

    @property
    def _language_settings_file(self) -> Path:
        return Path(self.root_path) / "налаштування_інтерфейсу.json"

    def _load_saved_language(self) -> str:
        try:
            if self._language_settings_file.exists():
                data = json.loads(self._language_settings_file.read_text(encoding="utf-8"))
                value = data.get("language", "Українська")
                return value if value in {"Українська", "Русский"} else "Українська"
        except Exception:
            pass
        return "Українська"

    def _save_language(self) -> None:
        try:
            data = {}
            if self._language_settings_file.exists():
                data = json.loads(self._language_settings_file.read_text(encoding="utf-8"))
            data["language"] = self.language
            self._language_settings_file.parent.mkdir(parents=True, exist_ok=True)
            self._language_settings_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def _language_image_path(self) -> Path:
        for p in (
            self._resource("assets", "moskal.png"),
            self._resource("assets", "language-russian.jpg"),
            self._resource("language-russian.jpg"),
        ):
            if p.exists():
                return p
        return Path()

    def _show_language_gate(self) -> None:
        self.language = self._load_saved_language()
        win = tk.Toplevel(self)
        win.title("Мова / Язык")
        win.geometry("1280x860")
        win.minsize(1050, 720)
        win.resizable(True, True)
        win.transient(self)
        win.grab_set()
        win.configure(bg="#0b1110")

        outer = tk.Frame(win, bg="#0b1110")
        outer.pack(fill="both", expand=True)
        tk.Label(outer, text="ОБЕРІТЬ МОВУ / ВЫБЕРИТЕ ЯЗЫК", bg="#0b1110", fg="#eef5f0",
                 font=("Segoe UI Variable", 26, "bold")).pack(pady=(22, 8))
        tk.Label(outer, text="Мова інтерфейсу / Язык интерфейса", bg="#0b1110", fg="#9aada1",
                 font=("Segoe UI Variable", 12)).pack(pady=(0, 12))

        choice = tk.StringVar(value=self.language)
        selector = ttk.Frame(outer)
        selector.pack(pady=8)
        ttk.Radiobutton(selector, text="Українська", value="Українська", variable=choice).pack(side="left", padx=24)
        ttk.Radiobutton(selector, text="Русский", value="Русский", variable=choice).pack(side="left", padx=24)

        image_frame = tk.Frame(outer, bg="#050806", highlightthickness=1, highlightbackground="#2b4035")
        image_frame.pack(fill="both", expand=True, padx=22, pady=14)
        image_label = tk.Label(image_frame, bg="#050806", fg="#9aada1", bd=0)
        image_label.pack(fill="both", expand=True, padx=6, pady=6)

        def render_image(_event=None):
            image_label.configure(image="", text="")
            self._language_photo = None
            self._language_source_image = None
            if choice.get() != "Русский":
                image_label.configure(text="Українська мова\n\nЛокальний автономний режим",
                                      font=("Segoe UI Variable", 22, "bold"), fg="#66d39a")
                return
            path = self._language_image_path()
            if Image is None or ImageTk is None or ImageOps is None or not path.exists():
                image_label.configure(text="Не вдалося завантажити зображення мови",
                                      font=("Segoe UI Variable", 16), fg="#df746d")
                return
            try:
                self._language_source_image = Image.open(path).convert("RGB")
                w = max(200, image_label.winfo_width() - 12)
                h = max(200, image_label.winfo_height() - 12)
                fitted = ImageOps.contain(self._language_source_image, (w, h), Image.Resampling.LANCZOS)
                canvas = Image.new("RGB", (w, h), "#050806")
                canvas.paste(fitted, ((w - fitted.width) // 2, (h - fitted.height) // 2))
                self._language_photo = ImageTk.PhotoImage(canvas)
                image_label.configure(image=self._language_photo)
            except Exception:
                image_label.configure(text="Не вдалося відкрити зображення",
                                      font=("Segoe UI Variable", 16), fg="#df746d")

        image_label.bind("<Configure>", render_image)
        choice.trace_add("write", lambda *_: render_image())
        win.after(120, render_image)

        def accept() -> None:
            self.language = choice.get()
            self._save_language()
            win.grab_release()
            win.destroy()
            self.deiconify()
            self.lift()
            self.focus_force()

        ttk.Button(outer, text="Продовжити", command=accept).pack(pady=(0, 20), ipadx=35, ipady=7)
        win.protocol("WM_DELETE_WINDOW", accept)


def main() -> None:
    from desktop_max import MaxUXDashboard
    MaxUXDashboard().mainloop()


if __name__ == "__main__":
    main()
