from __future__ import annotations

import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from desktop_release_v2 import FullReleaseDashboard


class MaxUXDashboard(FullReleaseDashboard):
    """Command dashboard with all frequent preferences directly on the main screen."""

    def __init__(self) -> None:
        self.ui_language = "Українська"
        super().__init__()
        self.after(120, self._install_main_quick_controls)

    @property
    def _quick_settings_file(self) -> Path:
        return Path(self.root_path) / "налаштування_інтерфейсу.json"

    def _read_quick_language(self) -> str:
        try:
            if self._quick_settings_file.exists():
                data = json.loads(self._quick_settings_file.read_text(encoding="utf-8"))
                return data.get("language", "Українська")
        except Exception:
            pass
        return "Українська"

    def _save_quick_language(self) -> None:
        try:
            data = {}
            if self._quick_settings_file.exists():
                data = json.loads(self._quick_settings_file.read_text(encoding="utf-8"))
            data["language"] = self.ui_language
            self._quick_settings_file.parent.mkdir(parents=True, exist_ok=True)
            self._quick_settings_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def _install_main_quick_controls(self) -> None:
        self.ui_language = self._read_quick_language()
        try:
            for child in list(self.shell.winfo_children()):
                labels = []
                for sub in child.winfo_children():
                    try:
                        text = sub.cget("text")
                        if text:
                            labels.append(str(text))
                    except Exception:
                        pass
                if "КЕРУВАННЯ" in labels:
                    child.destroy()
        except Exception:
            pass

        self.tabs.pack_forget()
        bar = ttk.Frame(self.shell, style="Card.TFrame")
        bar.pack(fill="x", padx=22, pady=(0, 8), before=self.tabs)

        ttk.Label(bar, text="ШВИДКІ НАЛАШТУВАННЯ", style="CardTitle.TLabel").pack(side="left", padx=(14, 10), pady=8)

        ttk.Label(bar, text="Мова", style="Muted.TLabel").pack(side="left", padx=(0, 4))
        self.language_combo = ttk.Combobox(bar, values=["Українська", "Русский"], state="readonly", width=13)
        self.language_combo.set(self.ui_language if self.ui_language in {"Українська", "Русский"} else "Українська")
        self.language_combo.pack(side="left", padx=(0, 12), pady=6)
        self.language_combo.bind("<<ComboboxSelected>>", lambda _e: self._quick_language_changed())

        ttk.Label(bar, text="Тема", style="Muted.TLabel").pack(side="left", padx=(0, 4))
        self.quick_theme = ttk.Combobox(bar, values=list(self.__class__.THEMES if hasattr(self.__class__, "THEMES") else []), state="readonly", width=20)
        try:
            from desktop_release import THEMES
            self.quick_theme["values"] = list(THEMES)
        except Exception:
            self.quick_theme["values"] = ["Темна військова", "Графітова командна", "Світла офісна"]
        self.quick_theme.set(self.theme_name)
        self.quick_theme.pack(side="left", padx=(0, 12), pady=6)
        self.quick_theme.bind("<<ComboboxSelected>>", lambda _e: self._quick_theme_changed())

        ttk.Label(bar, text="Текст", style="Muted.TLabel").pack(side="left", padx=(0, 4))
        self.quick_font = ttk.Combobox(bar, values=["90%", "100%", "110%", "120%", "130%", "140%"], state="readonly", width=8)
        self.quick_font.set(f"{round(self.font_scale * 100)}%")
        self.quick_font.pack(side="left", padx=(0, 10), pady=6)
        self.quick_font.bind("<<ComboboxSelected>>", lambda _e: self._quick_font_changed())

        self.quick_compact = tk.BooleanVar(value=self.compact_rows)
        ttk.Checkbutton(bar, text="Компактно", variable=self.quick_compact, command=self._quick_compact_changed).pack(side="left", padx=4)

        ttk.Button(bar, text="＋ Нове", style="Accent.TButton", command=self.add_order_dialog).pack(side="right", padx=(8, 6), pady=6)
        ttk.Button(bar, text="💾 Копія", command=self.create_backup).pack(side="right", padx=5, pady=6)
        ttk.Button(bar, text="📂 Дані", command=self.choose_root).pack(side="right", padx=5, pady=6)
        ttk.Button(bar, text="📊 Аналітика", command=self.open_statistics).pack(side="right", padx=5, pady=6)

        self.tabs.pack(fill="both", expand=True, padx=22, pady=(4, 14))
        self.bind("<Control-n>", lambda _e: self.add_order_dialog())
        self.bind("<Control-s>", lambda _e: self.create_backup())
        self.bind("<F11>", lambda _e: self._toggle_fullscreen())
        self.bind("<Escape>", lambda _e: self.attributes("-fullscreen", False))

    def _quick_language_changed(self) -> None:
        self.ui_language = self.language_combo.get()
        self._save_quick_language()
        self._save_language()

    def _quick_theme_changed(self) -> None:
        self.theme_name = self.quick_theme.get()
        self._apply_theme()

    def _quick_font_changed(self) -> None:
        self.font_scale = int(self.quick_font.get().rstrip("%")) / 100
        self._apply_theme()

    def _quick_compact_changed(self) -> None:
        self.compact_rows = bool(self.quick_compact.get())
        self._apply_theme()

    def _toggle_fullscreen(self) -> None:
        self.attributes("-fullscreen", not bool(self.attributes("-fullscreen")))


def main() -> None:
    MaxUXDashboard().mainloop()


if __name__ == "__main__":
    main()
