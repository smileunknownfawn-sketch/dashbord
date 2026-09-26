from __future__ import annotations

import ctypes
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from desktop_final import DesktopDashboard


class ReleaseDashboard(DesktopDashboard):
    """Фінальна оболонка 1.0.1: локальні ресурси, мова та додатки."""

    def __init__(self) -> None:
        super().__init__()
        self._install_release_controls()

    def _resource(self, *parts: str) -> Path:
        base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        return base.joinpath(*parts)

    def _install_release_controls(self) -> None:
        children = self.winfo_children()
        anchor = children[1] if len(children) > 1 else None
        bar = ttk.Frame(self)
        if anchor is not None:
            bar.pack(fill="x", padx=24, pady=(0, 6), before=anchor)
        else:
            bar.pack(fill="x", padx=24, pady=(0, 6))
        ttk.Label(bar, text="Мова інтерфейсу:").pack(side="left")
        self.language = ttk.Combobox(bar, values=["Українська", "Російська"], state="readonly", width=18)
        self.language.set("Українська")
        self.language.pack(side="left", padx=8)
        self.language.bind("<<ComboboxSelected>>", self._language_changed)
        ttk.Label(bar, text="Інтерфейс застосунку — українською", style="Muted.TLabel").pack(side="left")

    def _language_changed(self, _event=None) -> None:
        if self.language.get() != "Російська":
            return
        win = tk.Toplevel(self)
        win.title("Мова інтерфейсу")
        win.geometry("520x500")
        win.configure(bg="#0e1511")
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
        paths = filedialog.askopenfilenames(title="Оберіть додатки до розпорядження")
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
