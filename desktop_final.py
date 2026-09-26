"""Дашборд розпоряджень 1.0.1 — автономний Windows desktop UI."""
from __future__ import annotations

import os
import sys
import subprocess
from datetime import date, datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from core.config import APP_TITLE, APP_VERSION, DEVELOPER, AppPaths, CATEGORIES, PRIORITIES
from core.database import Database
from core.orders import OrderService
from core.search_service import search_rows
from core.storage import LocalStorage
from core.backup import BackupService


STATUS_UA = {"done": "ВИКОНАНО", "overdue": "ПРОСТРОЧЕНО", "today": "ТЕРМІН СЬОГОДНІ", "progress": "У РОБОТІ"}


class DesktopDashboard(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_TITLE} — версія {APP_VERSION}")
        self.geometry("1380x820")
        self.minsize(1100, 700)
        self.configure(bg="#0e1511")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#0e1511")
        self.style.configure("Card.TFrame", background="#18231c")
        self.style.configure("TLabel", background="#0e1511", foreground="#eaf1eb", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI Semibold", 22), foreground="#f5f8f5")
        self.style.configure("Muted.TLabel", foreground="#9cab9f", font=("Segoe UI", 9))
        self.style.configure("TButton", font=("Segoe UI Semibold", 10), padding=(12, 8))
        self.style.configure("Treeview", background="#121a15", fieldbackground="#121a15", foreground="#e8eee9", rowheight=34, font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading", background="#26372c", foreground="#f0f5f1", font=("Segoe UI Semibold", 9))
        self.style.map("Treeview", background=[("selected", "#31583d")])
        self.root_path = self._load_root()
        self._open_services()
        self._build_ui()
        self.refresh()

    def _open_services(self) -> None:
        self.paths = AppPaths.from_root(self.root_path)
        self.paths.ensure()
        self.db = Database(self.paths.database)
        self.storage = LocalStorage(self.paths)
        self.service = OrderService(self.db, self.storage)
        self.backup = BackupService(self.paths, self.db)

    def _load_root(self) -> Path:
        cfg = Path.home() / ".vom_dashboard_root"
        try:
            if cfg.exists():
                p = Path(cfg.read_text(encoding="utf-8").strip()).expanduser()
                if p.exists(): return p.resolve()
        except OSError:
            pass
        return (Path.home() / "Документи" / "Дашборд розпоряджень").resolve()

    def _save_root(self) -> None:
        (Path.home() / ".vom_dashboard_root").write_text(str(self.root_path), encoding="utf-8")

    def _build_ui(self) -> None:
        header = ttk.Frame(self); header.pack(fill="x", padx=24, pady=(20, 8))
        ttk.Label(header, text=APP_TITLE, style="Title.TLabel").pack(side="left")
        ttk.Label(header, text=f"Версія {APP_VERSION}  •  🟢 АВТОНОМНИЙ РЕЖИМ", style="Muted.TLabel").pack(side="right")

        tools = ttk.Frame(self); tools.pack(fill="x", padx=24, pady=8)
        self.search_var = tk.StringVar()
        self.search = ttk.Entry(tools, textvariable=self.search_var, font=("Segoe UI", 11))
        self.search.pack(side="left", fill="x", expand=True, ipady=8)
        self.search.insert(0, "Пошук за номером, словами, відповідальним, мітками або файлами…")
        self.search.bind("<FocusIn>", self._clear_placeholder)
        self.search.bind("<KeyRelease>", lambda _e: self.refresh())
        ttk.Button(tools, text="＋ Додати розпорядження", command=self.add_order_dialog).pack(side="left", padx=8)
        ttk.Button(tools, text="⚙ Папка даних", command=self.choose_root).pack(side="left")
        ttk.Button(tools, text="💾 Резервна копія", command=self.create_backup).pack(side="left", padx=8)

        kpi = ttk.Frame(self, style="Card.TFrame"); kpi.pack(fill="x", padx=24, pady=8)
        self.kpi_var = tk.StringVar(); ttk.Label(kpi, textvariable=self.kpi_var, style="Muted.TLabel").pack(anchor="w", padx=16, pady=12)

        body = ttk.Frame(self); body.pack(fill="both", expand=True, padx=24, pady=8)
        cols = ("number", "description", "deadline", "status", "responsible", "category")
        self.tree = ttk.Treeview(body, columns=cols, show="headings")
        titles = {"number":"Номер", "description":"Короткий опис", "deadline":"Термін виконання", "status":"Статус", "responsible":"Відповідальний", "category":"Категорія"}
        widths = {"number":120,"description":470,"deadline":125,"status":160,"responsible":190,"category":160}
        for c in cols: self.tree.heading(c, text=titles[c]); self.tree.column(c, width=widths[c], anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        bar=ttk.Scrollbar(body, orient="vertical", command=self.tree.yview); bar.pack(side="right", fill="y"); self.tree.configure(yscrollcommand=bar.set)
        self.tree.bind("<Double-1>", lambda _e: self.open_card())

        actions=ttk.Frame(self); actions.pack(fill="x", padx=24, pady=8)
        for text, cmd in (("Відкрити",self.open_card),("＋ Відповідь",self.response_selected),("✓ Виконано",self.done_selected),("↶ Повернути в роботу",self.reopen_selected),("🗑 У кошик",self.trash_selected)):
            ttk.Button(actions,text=text,command=cmd).pack(side="left", padx=(0,6))
        ttk.Button(actions,text="Календар / статистика",command=self.statistics).pack(side="right")
        ttk.Button(actions,text="Діагностика",command=self.diagnostics).pack(side="right", padx=6)
        ttk.Button(actions,text="Кошик",command=self.trash_window).pack(side="right")

        footer=ttk.Frame(self); footer.pack(fill="x", padx=24, pady=(2,12))
        ttk.Label(footer,text=f"Розробник: {DEVELOPER}  •  Дані: {self.root_path}",style="Muted.TLabel").pack(side="left")
        ttk.Label(footer,text="Локальна база • Мережа не потрібна",style="Muted.TLabel").pack(side="right")
        self.bind("<Control-f>", lambda _e: self._focus_search())

    def _focus_search(self):
        self._clear_placeholder(); self.search.focus_set(); self.search.selection_range(0, tk.END)

    def _clear_placeholder(self, _event=None):
        if self.search_var.get().startswith("Пошук за номером"): self.search_var.set("")

    def refresh(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        rows=[dict(r) for r in self.db.get_orders()]
        query=self.search_var.get().strip()
        if query.startswith("Пошук за номером"): query=""
        results=search_rows(rows,query) if query else [type("R",(),{"row":r}) for r in rows]
        for result in results:
            r=result.row; status=STATUS_UA[self.service.status(r)]
            self.tree.insert("","end",iid=str(r["id"]),values=(r["number"],r["description"],r["deadline"],status,r["responsible"],r["category"]))
        total=len(rows); done=sum(self.service.status(r)=="done" for r in rows); overdue=sum(self.service.status(r)=="overdue" for r in rows)
        self.kpi_var.set(f"Всього: {total}   •   Виконано: {done}   •   У роботі: {total-done}   •   Прострочено: {overdue}")

    def selected(self):
        sel=self.tree.selection(); return self.db.get_order(int(sel[0])) if sel else None

    def choose_root(self):
        chosen=filedialog.askdirectory(title="Оберіть папку для локальних даних",initialdir=str(self.root_path))
        if chosen:
            self.root_path=Path(chosen).resolve(); self._save_root(); self._open_services(); self.refresh()

    def _entry(self,parent,label,row,default="",width=52):
        ttk.Label(parent,text=label).grid(row=row,column=0,sticky="w",padx=16,pady=7)
        e=ttk.Entry(parent,width=width); e.grid(row=row,column=1,sticky="ew",padx=16,pady=7); e.insert(0,default); return e

    def add_order_dialog(self):
        win=tk.Toplevel(self); win.title("Додати розпорядження"); win.geometry("720x620"); win.grab_set(); win.configure(bg="#0e1511")
        win.columnconfigure(1,weight=1); fields={}
        fields["number"]=self._entry(win,"Номер розпорядження",0)
        fields["description"]=self._entry(win,"Короткий опис",1)
        fields["received"]=self._entry(win,"Дата отримання (РРРР-ММ-ДД)",2,date.today().isoformat())
        fields["deadline"]=self._entry(win,"Термін виконання (РРРР-ММ-ДД)",3,date.today().isoformat())
        fields["responsible"]=self._entry(win,"Відповідальний",4)
        fields["tags"]=self._entry(win,"Мітки",5)
        ttk.Label(win,text="Пріоритет").grid(row=6,column=0,sticky="w",padx=16,pady=7); priority=ttk.Combobox(win,values=PRIORITIES,state="readonly"); priority.set(PRIORITIES[0]); priority.grid(row=6,column=1,sticky="ew",padx=16)
        ttk.Label(win,text="Категорія").grid(row=7,column=0,sticky="w",padx=16,pady=7); category=ttk.Combobox(win,values=CATEGORIES,state="readonly"); category.set(CATEGORIES[-1]); category.grid(row=7,column=1,sticky="ew",padx=16)
        chosen=[None]; file_text=tk.StringVar(value="Файл не обрано")
        ttk.Button(win,text="Обрати документ",command=lambda:self._pick(chosen,file_text)).grid(row=8,column=1,sticky="w",padx=16,pady=8); ttk.Label(win,textvariable=file_text,style="Muted.TLabel").grid(row=9,column=1,sticky="w",padx=16)
        def save():
            p=chosen[0]
            try:
                if not p: raise ValueError("Оберіть файл розпорядження")
                self.service.create(number=fields["number"].get(),received=date.fromisoformat(fields["received"].get()),deadline=date.fromisoformat(fields["deadline"].get()),description=fields["description"].get(),file_name=p.name,file_bytes=p.read_bytes(),priority=priority.get(),responsible=fields["responsible"].get(),category=category.get(),tags=fields["tags"].get())
                win.destroy(); self.refresh(); messagebox.showinfo("Готово","Розпорядження успішно додано.")
            except Exception as exc: messagebox.showerror("Помилка","Не вдалося додати розпорядження.\n\n"+str(exc),parent=win)
        ttk.Button(win,text="Додати розпорядження",command=save).grid(row=10,column=1,sticky="e",padx=16,pady=18)

    def _pick(self,holder,label):
        p=filedialog.askopenfilename(title="Оберіть документ"); holder[0]=Path(p) if p else None; label.set(holder[0].name if holder[0] else "Файл не обрано")

    def open_card(self):
        row=self.selected()
        if not row: return messagebox.showinfo("Розпорядження","Оберіть розпорядження.")
        win=tk.Toplevel(self); win.title(f"Розпорядження № {row['number']}"); win.geometry("900x700"); win.configure(bg="#0e1511")
        ttk.Label(win,text=f"Розпорядження № {row['number']}",style="Title.TLabel").pack(anchor="w",padx=22,pady=(18,4))
        ttk.Label(win,text=f"{STATUS_UA[self.service.status(row)]}  •  {row['priority']}  •  {self.service.remaining(row['deadline'])}",style="Muted.TLabel").pack(anchor="w",padx=22,pady=(0,14))
        info=ttk.Frame(win,style="Card.TFrame"); info.pack(fill="x",padx=22,pady=6)
        details=[("Короткий опис",row["description"]),("Дата отримання",row["received_date"]),("Термін виконання",row["deadline"]),("Відповідальний",row["responsible"]),("Категорія",row["category"]),("Мітки",row["tags"]),("Вихідний номер",row["completion_outgoing"] or "—")]
        for i,(k,v) in enumerate(details): ttk.Label(info,text=f"{k}: ",font=("Segoe UI Semibold",10)).grid(row=i,column=0,sticky="w",padx=14,pady=5); ttk.Label(info,text=v).grid(row=i,column=1,sticky="w",padx=14,pady=5)
        ttk.Label(win,text="Відповіді",style="Title.TLabel").pack(anchor="w",padx=22,pady=(18,6))
        resp=ttk.Treeview(win,columns=("date","outgoing","comment","file"),show="headings",height=7)
        for c,t,w in (("date","Дата",110),("outgoing","Вихідний номер",150),("comment","Зміст відповіді",400),("file","Файл",190)):resp.heading(c,text=t);resp.column(c,width=w)
        resp.pack(fill="x",padx=22)
        for r in self.db.get_responses(row["id"]): resp.insert("","end",values=(r["response_date"],r["outgoing"] or "—",r["comment"] or "—",r["filename"]))
        buttons=ttk.Frame(win);buttons.pack(fill="x",padx=22,pady=16)
        ttk.Button(buttons,text="＋ Додати відповідь",command=lambda:self.response_dialog(row,win)).pack(side="left")
        ttk.Button(buttons,text="Відкрити оригінал",command=lambda:self.open_path(row["path"])).pack(side="left",padx=7)
        ttk.Button(buttons,text="Виконано",command=lambda:(self.service.mark_done(row["id"]),win.destroy(),self.refresh())).pack(side="right")

    def response_selected(self):
        row=self.selected()
        if row:self.response_dialog(row,self)
        else:messagebox.showinfo("Відповідь","Оберіть розпорядження.")

    def response_dialog(self,row,parent):
        win=tk.Toplevel(self);win.title(f"Відповідь на № {row['number']}");win.geometry("720x560");win.grab_set();win.columnconfigure(1,weight=1)
        f={"date":self._entry(win,"Дата відповіді (РРРР-ММ-ДД)",0,date.today().isoformat()),"outgoing":self._entry(win,"Вихідний номер",1),"comment":self._entry(win,"Зміст відповіді",2)}
        final=tk.BooleanVar(value=True);ttk.Checkbutton(win,text="Вважати розпорядження виконаним",variable=final).grid(row=3,column=1,sticky="w",padx=16,pady=8)
        holder=[None];label=tk.StringVar(value="Файл не обрано");ttk.Button(win,text="Обрати файл або архів",command=lambda:self._pick(holder,label)).grid(row=4,column=1,sticky="w",padx=16,pady=8);ttk.Label(win,textvariable=label,style="Muted.TLabel").grid(row=5,column=1,sticky="w",padx=16)
        def save():
            try:
                p=holder[0]
                if not p:raise ValueError("Оберіть файл відповіді або архів")
                self.service.add_response(row,response_date=date.fromisoformat(f["date"].get()),outgoing=f["outgoing"].get(),comment=f["comment"].get(),file_name=p.name,file_bytes=p.read_bytes(),final=final.get())
                win.destroy();self.refresh();messagebox.showinfo("Готово","Відповідь збережено у папці цього розпорядження.",parent=parent)
            except Exception as exc:messagebox.showerror("Помилка","Не вдалося зберегти відповідь.\n\n"+str(exc),parent=win)
        ttk.Button(win,text="Зберегти відповідь",command=save).grid(row=6,column=1,sticky="e",padx=16,pady=18)

    def open_path(self,relative):
        p=self.storage.safe(relative)
        if not p.exists():return messagebox.showwarning("Файл","Файл не знайдено у локальному сховищі.")
        try:
            if sys.platform.startswith("win"):os.startfile(str(p))
            elif sys.platform=="darwin":subprocess.run(["open",str(p)],check=False)
            else:subprocess.run(["xdg-open",str(p)],check=False)
        except Exception as exc:messagebox.showerror("Файл",str(exc))

    def done_selected(self):
        row=self.selected()
        if row and messagebox.askyesno("Виконання",f"Позначити №{row['number']} як виконане?"):self.service.mark_done(row["id"]);self.refresh()

    def reopen_selected(self):
        row=self.selected()
        if row and messagebox.askyesno("Повернення",f"Повернути №{row['number']} у роботу?"):self.service.reopen(row["id"]);self.refresh()

    def trash_selected(self):
        row=self.selected()
        if row and messagebox.askyesno("Кошик",f"Перемістити №{row['number']} до кошика?",icon="warning"):
            try:self.service.move_to_trash(row);self.refresh()
            except Exception as exc:messagebox.showerror("Кошик",str(exc))

    def create_backup(self):
        try:
            p=self.backup.create(True);messagebox.showinfo("Резервна копія",f"Копію створено:\n{p}")
        except Exception as exc:messagebox.showerror("Резервна копія",str(exc))

    def statistics(self):
        rows=[dict(r) for r in self.db.get_orders()];months={}
        for r in rows:months[str(r.get("received_date") or "Без дати")[:7]]=months.get(str(r.get("received_date") or "Без дати")[:7],0)+1
        text="\n".join(f"{k}: {v}" for k,v in sorted(months.items(),reverse=True)) or "Даних немає."
        messagebox.showinfo("Статистика",f"Отримано за місяцями:\n\n{text}")

    def diagnostics(self):
        inv=self.storage.inventory(); problems=self.storage.validate();text=f"SQLite — OK\nЛокальне сховище — OK\nМережа — не потрібна\nФайлів: {inv['files']}\nПапок: {inv['folders']}\nОбсяг: {inv['mb']} МБ"
        if problems:text+="\n\nПроблеми:\n"+"\n".join(problems)
        messagebox.showinfo("Діагностика",text)

    def trash_window(self):
        win=tk.Toplevel(self);win.title("Кошик");win.geometry("800x520");tree=ttk.Treeview(win,columns=("number","description","deleted"),show="headings")
        for c,t in (("number","Номер"),("description","Короткий опис"),("deleted","Дата видалення")):tree.heading(c,text=t);tree.column(c,width=250)
        tree.pack(fill="both",expand=True,padx=12,pady=12)
        for r in self.db.get_trash():tree.insert("","end",iid=str(r["id"]),values=(r["number"],r["description"],r["deleted_at"]))
        def restore():
            s=tree.selection()
            if s:
                try:self.service.restore(int(s[0]));win.destroy();self.refresh()
                except Exception as exc:messagebox.showerror("Відновлення",str(exc),parent=win)
        def purge():
            s=tree.selection()
            if s and messagebox.askyesno("Остаточне видалення","Видалити документ і всі його файли назавжди?",icon="warning"):
                self.service.purge(int(s[0]));win.destroy();self.refresh()
        ttk.Button(win,text="Відновити",command=restore).pack(side="left",padx=20,pady=10);ttk.Button(win,text="Видалити назавжди",command=purge).pack(side="right",padx=20,pady=10)


def main():
    DesktopDashboard().mainloop()

if __name__ == "__main__":main()
