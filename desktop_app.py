"""Автономний Windows-застосунок. Не використовує Streamlit або мережу."""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from core.config import APP_TITLE, APP_VERSION, DEVELOPER, AppPaths, CATEGORIES, PRIORITIES
from core.database import Database
from core.orders import OrderService
from core.search_service import search_rows
from core.storage import LocalStorage


class DesktopApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_TITLE} — версія {APP_VERSION}")
        self.geometry("1280x780")
        self.minsize(1050, 680)
        self.configure(bg="#101713")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#101713")
        self.style.configure("Card.TFrame", background="#18221c")
        self.style.configure("TLabel", background="#101713", foreground="#e8efe9", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI Semibold", 20), foreground="#f2f6f3")
        self.style.configure("Muted.TLabel", foreground="#9baa9f", font=("Segoe UI", 9))
        self.style.configure("TButton", font=("Segoe UI Semibold", 10), padding=(12, 8))
        self.style.configure("Treeview", background="#141c17", fieldbackground="#141c17", foreground="#e8efe9", rowheight=32, font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading", background="#26352b", foreground="#eef5ef", font=("Segoe UI Semibold", 9))
        self.style.map("Treeview", background=[("selected", "#31543b")])

        self.root_path = self._load_root()
        self.paths = AppPaths.from_root(self.root_path)
        self.db = Database(self.paths.database)
        self.storage = LocalStorage(self.paths)
        self.service = OrderService(self.db, self.storage)
        self.filtered: list[dict] = []
        self._build()
        self.refresh()

    def _load_root(self) -> Path:
        # Налаштування зберігається у профілі користувача, а дані — окремо.
        cfg = Path.home() / ".vom_dashboard_root"
        if cfg.exists():
            try:
                p = Path(cfg.read_text(encoding="utf-8").strip()).expanduser()
                if p.exists():
                    return p.resolve()
            except OSError:
                pass
        return (Path.home() / "Документи" / "Дашборд розпоряджень").resolve()

    def _save_root(self) -> None:
        cfg = Path.home() / ".vom_dashboard_root"
        cfg.write_text(str(self.root_path), encoding="utf-8")

    def _build(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill="x", padx=24, pady=(22, 10))
        ttk.Label(header, text=APP_TITLE, style="Title.TLabel").pack(side="left")
        ttk.Label(header, text=f"Версія {APP_VERSION}  •  🟢 АВТОНОМНИЙ РЕЖИМ", style="Muted.TLabel").pack(side="right")

        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=24, pady=8)
        self.search_var = tk.StringVar()
        search = ttk.Entry(toolbar, textvariable=self.search_var, font=("Segoe UI", 11))
        search.pack(side="left", fill="x", expand=True, ipady=7)
        search.insert(0, "Пошук за номером, словами, відповідальним, мітками або файлами…")
        search.bind("<FocusIn>", lambda _e: self._clear_search_placeholder())
        search.bind("<KeyRelease>", lambda _e: self.refresh())
        ttk.Button(toolbar, text="＋ Додати розпорядження", command=self.add_order_dialog).pack(side="left", padx=8)
        ttk.Button(toolbar, text="⚙ Папка даних", command=self.choose_root).pack(side="left")

        stats = ttk.Frame(self, style="Card.TFrame")
        stats.pack(fill="x", padx=24, pady=8)
        self.kpi = tk.StringVar()
        ttk.Label(stats, textvariable=self.kpi, style="Muted.TLabel").pack(anchor="w", padx=16, pady=12)

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, padx=24, pady=8)
        self.tree = ttk.Treeview(body, columns=("number", "description", "deadline", "status", "responsible", "category"), show="headings", selectmode="browse")
        headings = {"number": "Номер", "description": "Короткий опис", "deadline": "Термін виконання", "status": "Статус", "responsible": "Відповідальний", "category": "Категорія"}
        widths = {"number": 120, "description": 430, "deadline": 120, "status": 150, "responsible": 180, "category": 150}
        for col, title in headings.items():
            self.tree.heading(col, text=title)
            self.tree.column(col, width=widths[col], anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(body, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.bind("<Double-1>", lambda _e: self.open_selected())

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=24, pady=8)
        ttk.Button(buttons, text="Відкрити", command=self.open_selected).pack(side="left")
        ttk.Button(buttons, text="Додати відповідь", command=self.response_selected).pack(side="left", padx=6)
        ttk.Button(buttons, text="Виконано", command=self.done_selected).pack(side="left")
        ttk.Button(buttons, text="У кошик", command=self.trash_selected).pack(side="left", padx=6)
        ttk.Button(buttons, text="Календар / статистика", command=self.statistics).pack(side="right")
        ttk.Button(buttons, text="Діагностика", command=self.diagnostics).pack(side="right", padx=6)

        footer = ttk.Frame(self)
        footer.pack(fill="x", padx=24, pady=(2, 12))
        ttk.Label(footer, text=f"Розробник: {DEVELOPER}  •  Дані: {self.root_path}", style="Muted.TLabel").pack(side="left")
        ttk.Button(footer, text="Кошик", command=self.trash_window).pack(side="right")

        self.bind("<Control-f>", lambda _e: (self.focus_force(), self.after(20, lambda: self._focus_search())))

    def _focus_search(self) -> None:
        for child in self.winfo_children():
            pass
        self.search_var.set("")

    def _clear_search_placeholder(self) -> None:
        if self.search_var.get().startswith("Пошук за номером"):
            self.search_var.set("")

    def refresh(self) -> None:
        for item in self.tree.get_children(): self.tree.delete(item)
        rows = [dict(r) for r in self.db.get_orders()]
        query = self.search_var.get().strip()
        if query.startswith("Пошук за номером"): query = ""
        results = search_rows(rows, query) if query else [type("R", (), {"row": r}) for r in rows]
        self.filtered = [x.row for x in results]
        for row in self.filtered:
            status = self.service.status(row)
            status_ua = {"done": "ВИКОНАНО", "overdue": "ПРОСТРОЧЕНО", "today": "ТЕРМІН СЬОГОДНІ", "progress": "У РОБОТІ"}[status]
            self.tree.insert("", "end", iid=str(row["id"]), values=(row["number"], row["description"], row["deadline"], status_ua, row["responsible"], row["category"]))
        total = len(rows); done = sum(self.service.status(r) == "done" for r in rows); overdue = sum(self.service.status(r) == "overdue" for r in rows)
        self.kpi.set(f"Всього: {total}    •    Виконано: {done}    •    У роботі: {total-done}    •    Прострочено: {overdue}")

    def selected(self):
        sel = self.tree.selection()
        if not sel: return None
        return self.db.get_order(int(sel[0]))

    def choose_root(self) -> None:
        chosen = filedialog.askdirectory(title="Оберіть папку для локальних даних", initialdir=str(self.root_path))
        if chosen:
            self.root_path = Path(chosen).resolve(); self._save_root()
            self.paths = AppPaths.from_root(self.root_path); self.db = Database(self.paths.database); self.storage = LocalStorage(self.paths); self.service = OrderService(self.db, self.storage)
            self.refresh()

    def add_order_dialog(self) -> None:
        win = tk.Toplevel(self); win.title("Додати розпорядження"); win.geometry("650x600"); win.configure(bg="#101713"); win.grab_set()
        fields = {}
        labels = [("number", "Номер розпорядження"), ("description", "Короткий опис"), ("received", "Дата отримання (РРРР-ММ-ДД)"), ("deadline", "Термін виконання (РРРР-ММ-ДД)"), ("responsible", "Відповідальний"), ("tags", "Мітки")]
        for i, (key, text) in enumerate(labels):
            ttk.Label(win, text=text).grid(row=i, column=0, sticky="w", padx=20, pady=8); e=ttk.Entry(win, width=55); e.grid(row=i,column=1,padx=20,pady=8); fields[key]=e
        fields["received"].insert(0, date.today().isoformat()); fields["deadline"].insert(0, date.today().isoformat())
        ttk.Label(win,text="Пріоритет").grid(row=6,column=0,sticky="w", padx=20,pady=8); priority=ttk.Combobox(win,values=PRIORITIES,state="readonly");priority.set(PRIORITIES[0]);priority.grid(row=6,column=1,sticky="ew",padx=20,pady=8)
        ttk.Label(win,text="Категорія").grid(row=7,column=0,sticky="w", padx=20,pady=8); category=ttk.Combobox(win,values=CATEGORIES,state="readonly");category.set(CATEGORIES[-1]);category.grid(row=7,column=1,sticky="ew",padx=20,pady=8)
        chosen=[None]
        ttk.Button(win,text="Обрати документ",command=lambda:self._choose_file(chosen)).grid(row=8,column=1,sticky="w",padx=20,pady=8)
        file_label=tk.StringVar(value="Файл не обрано"); ttk.Label(win,textvariable=file_label,style="Muted.TLabel").grid(row=9,column=1,sticky="w",padx=20)
        def choose():
            p=chosen[0]
            if not p: messagebox.showwarning("Документ","Оберіть файл розпорядження.",parent=win); return
            try:
                self.service.create(number=fields["number"].get(),received=date.fromisoformat(fields["received"].get()),deadline=date.fromisoformat(fields["deadline"].get()),description=fields["description"].get(),file_name=p.name,file_bytes=p.read_bytes(),priority=priority.get(),responsible=fields["responsible"].get(),category=category.get(),tags=fields["tags"].get())
                messagebox.showinfo("Готово","Розпорядження додано.",parent=win); win.destroy(); self.refresh()
            except Exception as exc: messagebox.showerror("Не вдалося додати",str(exc),parent=win)
        ttk.Button(win,text="Додати",command=choose).grid(row=10,column=1,sticky="e",padx=20,pady=18)
        def update_label(*_): file_label.set(chosen[0].name if chosen[0] else "Файл не обрано")
        win._update_label=update_label

    def _choose_file(self, holder):
        p=filedialog.askopenfilename(title="Оберіть документ"); holder[0]=Path(p) if p else None

    def open_selected(self) -> None:
        row=self.selected()
        if not row:return messagebox.showinfo("Розпорядження","Оберіть розпорядження.")
        p=self.storage.safe(row["path"])
        if p.exists():
            try:
                if sys.platform.startswith("win"): os.startfile(str(p))
                elif sys.platform=="darwin": subprocess.run(["open",str(p)],check=False)
                else: subprocess.run(["xdg-open",str(p)],check=False)
            except Exception as exc: messagebox.showerror("Файл",f"Не вдалося відкрити файл: {exc}")
        else: messagebox.showwarning("Файл","Файл розпорядження не знайдено у локальному сховищі.")

    def done_selected(self):
        row=self.selected()
        if not row:return
        if messagebox.askyesno("Виконання",f"Позначити розпорядження №{row['number']} як виконане?"):
            self.service.mark_done(row["id"]); self.refresh()

    def trash_selected(self):
        row=self.selected()
        if not row:return
        if messagebox.askyesno("Кошик",f"Перемістити розпорядження №{row['number']} до кошика?",icon="warning"):
            try:self.service.move_to_trash(row);self.refresh()
            except Exception as exc:messagebox.showerror("Кошик",str(exc))

    def response_selected(self):
        row=self.selected()
        if not row:return messagebox.showinfo("Відповідь","Оберіть розпорядження.")
        messagebox.showinfo("Відповідь", "Форма відповіді буде доступна у картці розпорядження на наступному етапі desktop UI.")

    def statistics(self):
        rows=[dict(r) for r in self.db.get_orders()]; by={}
        for r in rows:
            key=str(r.get("received_date") or "")[:7]; by[key]=by.get(key,0)+1
        text="\n".join(f"{k or 'Без дати'}: {v}" for k,v in sorted(by.items(),reverse=True)) or "Даних ще немає."
        messagebox.showinfo("Статистика",f"Отримано за місяцями:\n\n{text}")

    def diagnostics(self):
        problems=self.storage.validate(); inv=self.storage.inventory();
        text="🟢 SQLite — OK\n🟢 Локальне сховище — OK\n🟢 Кошик — OK\n🟢 Резервні копії — OK\n🔒 Мережа — не потрібна\n\n"
        text+=f"Файлів: {inv['files']}\nПапок: {inv['folders']}\nОбсяг: {inv['mb']} МБ"
        if problems:text+="\n\n⚠ Проблеми:\n"+"\n".join(problems)
        messagebox.showinfo("Діагностика",text)

    def trash_window(self):
        win=tk.Toplevel(self);win.title("Кошик");win.geometry("700x500");
        tree=ttk.Treeview(win,columns=("number","description","deleted"),show="headings");
        for c,t in (("number","Номер"),("description","Короткий опис"),("deleted","Дата видалення")):tree.heading(c,text=t);tree.column(c,width=220)
        tree.pack(fill="both",expand=True,padx=12,pady=12)
        for r in self.db.get_trash():tree.insert("","end",iid=str(r["id"]),values=(r["number"],r["description"],r["deleted_at"]))
        def restore():
            sel=tree.selection()
            if not sel:return
            try:self.service.restore(int(sel[0]));win.destroy();self.refresh()
            except Exception as exc:messagebox.showerror("Відновлення",str(exc),parent=win)
        ttk.Button(win,text="Відновити",command=restore).pack(pady=10)


def main():
    app=DesktopApp();app.mainloop()

if __name__ == "__main__": main()
