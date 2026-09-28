from __future__ import annotations

import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk

try:
    from PIL import Image, ImageTk
except Exception:
    Image = None
    ImageTk = None

from desktop_release import ReleaseDashboard


class FullReleaseDashboard(ReleaseDashboard):
    """Final release wrapper with a real language-selection gate and Russian-language image."""

    def __init__(self) -> None:
        self.language = "Українська"
        self._language_photo = None
        super().__init__()
        self.withdraw()
        self.after(50, self._show_language_gate)

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
            self._language_settings_file.write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    def _show_language_gate(self) -> None:
        self.language = self._load_saved_language()
        win = tk.Toplevel(self)
        win.title("Мова / Язык")
        win.geometry("760x620")
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()
        win.configure(bg="#0b1110")

        title = tk.Label(
            win,
            text="ОБЕРІТЬ МОВУ / ВЫБЕРИТЕ ЯЗЫК",
            bg="#0b1110",
            fg="#eef5f0",
            font=("Segoe UI", 20, "bold"),
        )
        title.pack(pady=(24, 12))

        subtitle = tk.Label(
            win,
            text="Мова інтерфейсу / Язык интерфейса",
            bg="#0b1110",
            fg="#9aada1",
            font=("Segoe UI", 10),
        )
        subtitle.pack(pady=(0, 16))

        choice = tk.StringVar(value=self.language)
        buttons = ttk.Frame(win)
        buttons.pack(pady=8)
        ttk.Radiobutton(buttons, text="Українська", value="Українська", variable=choice).pack(side="left", padx=18)
        ttk.Radiobutton(buttons, text="Русский", value="Русский", variable=choice).pack(side="left", padx=18)

        image_frame = tk.Frame(win, bg="#111a17", width=680, height=390, highlightthickness=1, highlightbackground="#2b4035")
        image_frame.pack(padx=24, pady=18, fill="both", expand=True)
        image_frame.pack_propagate(False)

        image_label = tk.Label(image_frame, bg="#111a17", fg="#9aada1", text="")
        image_label.pack(fill="both", expand=True, padx=8, pady=8)

        def show_language_image(*_args) -> None:
            image_label.configure(image="", text="")
            self._language_photo = None
            if choice.get() != "Русский":
                image_label.configure(text="Українська мова\n\nЛокальний автономний режим", font=("Segoe UI", 18, "bold"), fg="#66d39a")
                return
            image_path = self._resource("assets", "moskal.png")
            if not image_path.exists():
                image_path = self._resource("assets", "language-russian.jpg")
            if Image is not None and ImageTk is not None and image_path.exists():
                try:
                    img = Image.open(image_path).convert("RGB")
                    img.thumbnail((650, 360), Image.Resampling.LANCZOS)
                    self._language_photo = ImageTk.PhotoImage(img)
                    image_label.configure(image=self._language_photo, text="")
                    return
                except Exception:
                    pass
            image_label.configure(text="Зображення для російської мови недоступне", font=("Segoe UI", 14), fg="#df746d")

        choice.trace_add("write", show_language_image)
        show_language_image()

        def accept() -> None:
            self.language = choice.get()
            self._save_language()
            win.grab_release()
            win.destroy()
            self.deiconify()
            self.lift()
            self.focus_force()

        ttk.Button(win, text="Продовжити", command=accept).pack(pady=(0, 24), ipadx=20, ipady=5)
        win.protocol("WM_DELETE_WINDOW", accept)


def main() -> None:
    FullReleaseDashboard().mainloop()


if __name__ == "__main__":
    main()
