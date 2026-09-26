from __future__ import annotations

import ctypes
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from desktop_modern import ModernDashboard


THEMES = {
    "Темний — військовий": {
        "BG": "#0b1110", "PANEL": "#111a17", "CARD": "#16221d", "CARD_2": "#1b2a23",
        "LINE": "#2b4035", "TEXT": "#eef5f0", "MUTED": "#9aada1", "ACCENT": "#66d39a",
        "ACCENT_2": "#3ea76f", "WARN": "#e6b85c", "DANGER": "#df746d", "ENTRY": "#0f1714",
        "HEADING": "#203129", "SELECT": "#24563e",
    },
    "Графітовий — командний": {
        "BG": "#0d1016", "PANEL": "#151a23", "CARD": "#1c222e", "CARD_2": "#252d3a",
        "LINE": "#343e4e", "TEXT": "#f1f4f8", "MUTED": "#9ba7b7", "ACCENT": "#70a7ff",
        "ACCENT_2": "#477fcb", "WARN": "#e3b45f", "DANGER": "#e06f75", "ENTRY": "#111620",
        "HEADING": "#273242", "SELECT": "#2c5688",
    },
    "Світлий — офісний": {
        "BG": "#eef2f0", "PANEL": "#f7f9f8", "CARD": "#ffffff", "CARD_2": "#edf3ef",
        "LINE": "#d5ded9", "TEXT": "#18231e", "MUTED": "#64736b", "ACCENT": "#217a4b",
        "ACCENT_2": "#2e9660", "WARN": "#a86e12", "DANGER": "#b84f49", "ENTRY": "#ffffff",
        "HEADING": "#e1e9e4", "SELECT": "#cce7d8",
    },
}


class ReleaseDashboard(ModernDashboard):
    """Фінальна оболонка 1.0.1: сучасний UI, теми, локальні ресурси, мова та додатки."""

    def __init__(self) -> None:
        self.theme_name = "Темний — військовий"
        super().__init__()
        self._install_release_controls()
        self._apply_theme(self.theme_name)

    def _resource(self, *parts: str) -> Path:
        base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        return base.joinpath(*parts)

    def _install_release_controls(self) -> None:
        bar = ttk.Frame(self.shell, style="Card.TFrame")
        bar.pack(fill="x", padx=22, pady=(0, 8))

        ttk.Label(bar, text="Тема оформлення", style="CardTitle.TLabel").pack(side="left", padx=(14, 8), pady=9)
        self.theme = ttk.Combobox(bar, values=list(THEMES), state="readonly", width=27)
        self.theme.set(self.theme_name)
        self.theme.pack(side="left", pady=6)
        self.theme.bind("<<ComboboxSelected>>", self._theme_changed)

        ttk.Label(bar, text="Мова інтерфейсу", style="CardTitle.TLabel").pack(side="left", padx=(24, 8), pady=9)
        self.language = ttk.Combobox(bar, values=["Українська", "Російська"], state="readonly", width=16)
        self.language.set("Українська")
        self.language.pack(side="left", pady=6)
        self.language.bind("<<ComboboxSelected>>", self._language_changed)
        ttk.Label(bar, text="Можна змінити тему у будь-який момент", style="Muted.TLabel").pack(side="right", padx=14)

    def _theme_changed(self, _event=None) -> None:
        self.theme_name = self.theme.get()
        self._apply_theme(self.theme_name)
        self.refresh_analytics()

    def _apply_theme(self, name: str) -> None:
        colors = THEMES.get(name, THEMES["Темний — військовий"])
        for key, value in colors.items():
            setattr(self, key, value)

        self.configure(bg=self.BG)
        s = self.style
        s.configure("Shell.TFrame", background=self.BG)
        s.configure("Panel.TFrame", background=self.PANEL)
        s.configure("Card.TFrame", background=self.CARD)
        s.configure("TLabel", background=self.PANEL, foreground=self.TEXT)
        s.configure("Title.TLabel", background=self.BG, foreground=self.TEXT)
        s.configure("Hero.TLabel", background=self.BG, foreground=self.ACCENT)
        s.configure("Muted.TLabel", background=self.PANEL, foreground=self.MUTED)
        s.configure("CardTitle.TLabel", background=self.CARD, foreground=self.TEXT)
        s.configure("Kpi.TLabel", background=self.CARD, foreground=self.TEXT)
        s.configure("KpiSmall.TLabel", background=self.CARD, foreground=self.MUTED)
        s.configure("Accent.TButton", foreground="#07100c" if name != "Світлий — офісний" else "#ffffff", background=self.ACCENT)
        s.map("Accent.TButton", background=[("active", self.ACCENT_2)])
        s.configure("Treeview", background=self.ENTRY, fieldbackground=self.ENTRY, foreground=self.TEXT)
        s.configure("Treeview.Heading", background=self.HEADING, foreground=self.TEXT)
        s.map("Treeview", background=[("selected", self.SELECT)], foreground=[("selected", self.TEXT)])
        s.configure("TNotebook", background=self.BG)
        s.configure("Modern.TNotebook", background=self.BG)
        s.configure("TNotebook.Tab", background=self.CARD, foreground=self.MUTED)
        s.map("TNotebook.Tab", background=[("selected", self.ACCENT_2)], foreground=[("selected", "#ffffff")])
        s.configure("TEntry", fieldbackground=self.ENTRY, foreground=self.TEXT, insertcolor=self.TEXT)
        s.configure("TCombobox", fieldbackground=self.ENTRY, foreground=self.TEXT)
        s.configure("TLabelframe", background=self.CARD, foreground=self.TEXT)
        s.configure("TLabelframe.Label", background=self.CARD, foreground=self.ACCENT)

        for canvas_name in ("month_canvas", "category_canvas", "resp_canvas"):
            canvas = getattr(self, canvas_name, None)
            if canvas is not None:
                canvas.configure(bg=self.CARD)

        if hasattr(self, "theme"):
            self.theme.configure(style="TCombobox")
        self.update_idletasks()

    def _language_changed(self, _event=None) -> None:
        if self.language.get() != "Російська":
            return
        win = tk.Toplevel(self)
        win.title("Мова інтерфейсу")
        win.geometry("520x500")
        win.configure(bg=self.BG)
        win.transient(self)
        win.grab_set()
        ttk.Label(win, text="Ти що москать?", style="Title.TLabel").pack(pady=(22, 10))
        image = self._resource("assets", "moskal.png")
        if image.exists():
            try:
                photo = tk.PhotoImage(file=str(image))
                label = ttk.Label(win, image=photo)
                label.image = photo
                label.pack(fill="both", expand=True, padx=20, pady=10)
            except tk.TclError:
                ttk.Label(win, text="Зображення не вдалося відкрити.").pack(pady=20)
        else:
            ttk.Label(win, text="Зображення не знайдено у збірці.").pack(pady=20)
        ttk.Label(win, text="Мова інтерфейсу залишається українською.", style="Muted.TLabel").pack(pady=8)
        self.after(3500, lambda: (win.grab_release(), win.destroy()) if win.winfo_exists() else None)
        self.language.set("Українська")

    def _play_sound(self) -> None:
        sound = self._resource("sounds", "opiat-rabota.mp3")
        if not sound.exists() or not sys.platform.startswith("win"):
            return
        try:
            alias = "vom_dashboard_sound"
            mci = ctypes.windll.winmm.mciSendStringW
            mci(f'open "{sound}" type mpegvideo alias {alias}', None, 0, 0)
            mci(f"play {alias}", None, 0, 0)
            self.after(3500, lambda: mci(f"close {alias}", None, 0, 0))
        except Exception:
            pass

    def add_order_dialog(self):
        self._play_sound()
        return super().add_order_dialog()

    def add_attachments_selected(self):
        row = self.selected()
        if not row:
            messagebox.showinfo("Додатки", "Оберіть розпорядження.")
            return
        paths = filedialog.askopenfilenames(title="Оберіть необов'язкові додатки до розпорядження")
        errors = []
        for raw in paths:
            try:
                self.service.add_attachment(row["id"], Path(raw))
            except Exception as exc:
                errors.append(str(exc))
        if errors:
            messagebox.showerror("Додатки", "Не всі додатки вдалося зберегти:\n\n" + "\n".join(errors))
        elif paths:
            messagebox.showinfo("Додатки", f"Додано файлів: {len(paths)}")


def main() -> None:
    app = ReleaseDashboard()
    app.mainloop()


if __name__ == "__main__":
    main()
