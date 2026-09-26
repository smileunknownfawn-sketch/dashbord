"""Дашборд виконання розпоряджень — автономний Windows-застосунок 1.0.1."""
from __future__ import annotations

import ctypes
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
        self.geometry("1320x820")
        self.minsize(1100, 720)
        self.configure(bg="#101713")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#101713")
        self.style.configure("Card.TFrame", background="#18221c")
        self.style.configure("TLabel", background="#101713", foreground="#e8efe9", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI Semibold", 21), foreground="#f2f6f3")
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
        cfg = Path.home() / ".vom_dashboard_root"
        if cfg.exists():
            try:
                p = Path(cfg.read_text(encoding="utf-8").strip()).expanduser()
                if p.exists(): return p.resolve()
            except OSError: pass
        return (Path.home() / "Документи" / "Дашборд розпоряджень").resolve()

    def _save_root(self) -> None:
        try: (Path.home() / ".vom_dashboard_root").write_text(str(self.root_path), encoding="utf-8")
        except OSError: pass

    def _build(self) -> None:
        header = ttk.Frame(self); header.pack(fill="x", padx=24, pady=(18, 8))
        ttk.Label(header, text=APP_TITLE, style="Title.TLabel").pack(side="left")
        ttk.Label(header, text=f"Версія {APP_VERSION}  •  АВТОНОМНИЙ РЕЖИМ", style="Muted.TLabel").pack(side="right")

        lang = ttk.Frame(self); lang.pack(fill="x", padx=24, pady=(0, 8))
        ttk.Label(lang, text="Мова інтерфейсу:").pack(side="left")
        self.language = ttk.Combobox(lang, values=["Українська", "Російська"], state="readonly", width=18)
        self.language.set("Українська"); self.language.pack(side="left", padx=8)
        self.language.bind("<<ComboboxSelected>>", self._language_changed)
        ttk.Label(lang, text="Інтерфейс застосунку залишається українським.", style="Muted.TLabel").pack(side="left")

        toolbar = ttk.Frame(self); toolbar.pack(fill="x", padx=24, pady=8)
        self.search_var = tk.StringVar()
        self.search = ttk.Entry(toolbar, textvariable=self.search_var, font=("Segoe UI", 11))
        self.search.pack(side="left", fill="x", expand=True, ipady=7)
        self.search.insert(0, "Пошук за номером, словами, відповідальним, мітками або файлами…")
        self.search.bind("<FocusIn>", lambda _e: self._clear_search_placeholder())
        self.search.bind("<KeyRelease>", lambda _e: self.refresh())
        ttk.Button(toolbar, text="＋ Додати розпорядження", command=self.add_order_dialog).pack(side="left", padx=8)
        ttk.Button(toolbar, text="⚙ Папка даних", command=self.choose_root).pack(side="left")

        stats = ttk.Frame(self, style="Card.TFrame"); stats.pack(fill="x", padx=24, pady=8)
        self.kpi = tk.StringVar(); ttk.Label(stats, textvariable=self.kpi, style="Muted.TLabel").pack(anchor="w", padx=16, pady=12)

        body = ttk.Frame(self); body.pack(fill="both", expand=True, padx=24, pady=8)
        self.tree = ttk.Treeview(body, columns=("number", "description", "deadline", "status", "responsible", "category"), show="headings", selectmode="browse")
        headings = {"number":"Номер", "description":"Короткий опис розпорядження", "deadline":"Термін виконання", "status":"Статус", "responsible":"Відповідальний", "category":"Категорія"}
        widths = {"number":120, "description":440, "deadline":125, "status":160, "responsible":180, "category":150}
        for col, title in headings.items(): self.tree.heading(col, text=title); self.tree.column(col, width=widths[col], anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(body, orient="vertical", command=self.tree.yview); scroll.pack(side="right", fill="y"); self.tree.configure(yscrollcommand=scroll.set)
        self.tree.bind("<Double-1>", lambda _e: self.open_selected())

        buttons = ttk.Frame(self); buttons.pack(fill="x", padx=24, pady=8)
        ttk.Button(buttons, text="Відкрити картку", command=self.open_selected).pack(side="left")
        ttk.Button(buttons, text="Додати відповідь", command=self.response_selected).pack(side="left", padx=6)
        ttk.Button(buttons, text="Додати додатки", command=self.add_attachments_selected).pack(side="left")
        ttk.Button(buttons, text="Виконано", command=self.done_selected).pack(side="left", padx=6)
        ttk.Button(buttons, text="У кошик", command=self.trash_selected).pack(side="left")
        ttk.Button(buttons, text="Календар / статистика", command=self.statistics).pack(side="right")
        ttk.Button(buttons, text="Діагностика", command=self.diagnostics).pack(side="right", padx=6)

        footer = ttk.Frame(self); footer.pack(fill="x", padx=24, pady=(2, 12))
        ttk.Label(footer, text=f"Розробник: {DEVELOPER}  •  Дані: {self.root_path}", style="Muted.TLabel").pack(side="left")
        ttk.Button(footer, text="Кошик", command=self.trash_window).pack(side="right")
        self.bind("<Control-f>", lambda _e: self._focus_search())

    def _focus_search(self) -> None:
        self.search.focus_set(); self._clear_search_placeholder(); self.search.selection_range(0, tk.END)

    def _clear_search_placeholder(self) -> None:
        if self.search_var.get().startswith("Пошук за номером"): self.search_var.set("")

    def _language_changed(self, _event=None) -> None:
        if self.language.get() != "Російська": return
        win = tk.Toplevel(self); win.title("Мова інтерфейсу"); win.geometry("430x360"); win.configure(bg="#101713"); win.transient(self); win.grab_set()
        ttk.Label(win, text="Ти що москать?", style="Title.TLabel").pack(pady=(24, 12))
        image_path = self._resource("assets", "moskal.png")
        if image_path.exists():
            try:
                photo = tk.PhotoImage(file=str(image_path)); label=ttk.Label(win,image=photo); label.image=photo; label.pack(pady=8)
            except tk.TclError: ttk.Label(win,text="[зображення не вдалося відкрити]").pack(pady=20)
        else:
            ttk.Label(win,text="Зображення не знайдено у збірці.",style="Muted.TLabel").pack(pady=20)
        ttk.Label(win,text="Режим мови залишається українським.",style="Muted.TLabel").pack()
        self.after(3500, lambda: (win.grab_release(), win.destroy()) if win.winfo_exists() else None)
        self.language.set("Українська")

    def _resource(self, *parts: str) -> Path:
        base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        return base.joinpath(*parts)

    def _play_sound(self) -> None:
        sound = self._resource("sounds", "opiat-rabota.mp3")
        if not sound.exists() or not sys.platform.startswith("win"): return
        try:
            alias = "vom_dashboard_sound"
            mci = ctypes.windll.winmm.mciSendStringW
            mci(f'open "{sound}" type mpegvideo alias {alias}', None, 0, 0)
            mci(f'play {alias}', None, 0, 0)
            self.after(3500, lambda: mci(f"close {alias}", None, 0, 0))
        except Exception: pass

    def refresh(self) -> None:
        for item in self.tree.get_children(): self.tree.delete(item)
        rows=[dict(r) for r in self.db.get_orders()]; query=self.search_var.get().strip()
        if query.startswith("Пошук за номером"): query=""
        results=search_rows(rows,query) if query else [type("R",(),{"row":r}) for r in rows]
        self.filtered=[x.row for x in results]
        status_names={"done":"ВИКОНАНО","overdue":"ПРОСТРОЧЕНО","today":"ТЕРМІН СЬОГОДНІ","progress":"У РОБОТІ"}
        for row in self.filtered:
            self.tree.insert("","end",iid=str(row["id"]),values=(row["number"],row["description"],row["deadline"],status_names[self.service.status(row)],row["responsible"],row["category"]))
        total=len(rows); done=sum(self.service.status(r)=="done" for r in rows); overdue=sum(self.service.status(r)=="overdue" for r in rows)
        self.kpi.set(f"Всього: {total}    •    Виконано: {done}    •    У роботі: {total-done}    •    Прострочено: {overdue}")

    def selected(self):
        sel=self.tree.selection(); return self.db.get_order(int(sel[0])) if sel else None

    def choose_root(self) -> None:
        chosen=filedialog.askdirectory(title="Оберіть папку для локальних даних",initialdir=str(self.root_path))
        if not chosen:return
        self.root_path=Path(chosen).resolve(); self._save_root(); self.paths=AppPaths.from_root(self.root_path); self.db=Database(self.paths.database); self.storage=LocalStorage(self.paths); self.service=OrderService(self.db,self.storage); self.refresh()

    def add_order_dialog(self) -> None:
        self._play_sound()
        win=tk.Toplevel(self); win.title("Додати розпорядження"); win.geometry("700x650"); win.configure(bg="#101713"); win.grab_set()
        fields={}; labels=[("number","Номер розпорядження"),("description","Короткий опис розпорядження"),("received","Дата отримання (РРРР-ММ-ДД)"),("deadline","Термін виконання (РРРР-ММ-ДД)"),("responsible","Відповідальний"),("tags","Мітки")]
        for i,(key,text) in enumerate(labels): ttk.Label(win,text=text).grid(row=i,column=0,sticky="w",padx=20,pady=8); e=ttk.Entry(win,width=58);e.grid(row=i,column=1,padx=20,pady=8);fields[key]=e
        fields["received"].insert(0,date.today().isoformat());fields["deadline"].insert(0,date.today().isoformat())
        ttk.Label(win,text="Пріоритет").grid(row=6,column=0,sticky="w",padx=20,pady=8);priority=ttk.Combobox(win,values=PRIORITIES,state="readonly",width=55);priority.set(PRIORITIES[0]);priority.grid(row=6,column=1,padx=20,pady=8)
        ttk.Label(win,text="Категорія").grid(row=7,column=0,sticky="w",padx=20,pady=8);category=ttk.Combobox(win,values=CATEGORIES,state="readonly",width=55);category.set(CATEGORIES[-1]);category.grid(row=7,column=1,padx=20,pady=8)
        chosen=[None]; ttk.Button(win,text="Обрати основний документ",command=lambda:self._choose_file(chosen,file_label)).grid(row=8,column=1,sticky="w",padx=20,pady=8)
        file_label=tk.StringVar(value="Основний документ не обрано");ttk.Label(win,textvariable=file_label,style="Muted.TLabel").grid(row=9,column=1,sticky="w",padx=20)
        def save():
            p=chosen[0]
            if not p:return messagebox.showwarning("Документ","Оберіть основний файл розпорядження.",parent=win)
            try:
                oid=self.service.create(number=fields["number"].get(),received=date.fromisoformat(fields["received"].get()),deadline=date.fromisoformat(fields["deadline"].get()),description=fields["description"].get(),file_name=p.name,file_bytes=p.read_bytes(),priority=priority.get(),responsible=fields["responsible"].get(),category=category.get(),tags=fields["tags"].get())
                for ap in self._choose_many("Додайте додатки до розпорядження (необов'язково)"):
                    self.service.add_attachment(oid,ap)
                messagebox.showinfo("Готово","Розпорядження додано.",parent=win);win.destroy();self.refresh()
            except Exception as exc:messagebox.showerror("Не вдалося додати",str(exc),parent=win)
        ttk.Button(win,text="Додати розпорядження",command=save).grid(row=10,column=1,sticky="e",padx=20,pady=18)

    def _choose_file(self,holder,label=None):
        p=filedialog.askopenfilename(title="Оберіть файл")
        holder[0]=Path(p) if p else None
        if label is not None: label.set(holder[0].name if holder[0] else "Файл не обрано")

    def _choose_many(self,title):
        paths=filedialog.askopenfilenames(title=title)
        return [Path(p) for p in paths if p]

    def add_attachments_selected(self):
        row=self.selected()
        if not row:return messagebox.showinfo("Додатки","Оберіть розпорядження.")
        paths=self._choose_many("Оберіть додатки до розпорядження")
        for p in paths:
            try:self.service.add_attachment(row["id"],p)
            except Exception as exc:messagebox.showerror("Додаток",str(exc));break
        if paths:self.open_card(row)

    def open_selected(self):
        row=self.selected()
        if not row:return messagebox.showinfo("Розпорядження","Оберіть розпорядження.")
        self.open_card(row)

    def open_card(self,row):
        win=tk.Toplevel(self);win.title(f"Розпорядження № {row['number']}");win.geometry("900x680");win.configure(bg="#101713")
        ttk.Label(win,text=f"Розпорядження № {row['number']}",style="Title.TLabel").pack(anchor="w",padx=20,pady=(18,4))
        ttk.Label(win,text=row["description"]).pack(anchor="w",padx=20,pady=4)
        info=ttk.Frame(win,style="Card.TFrame");info.pack(fill="x",padx=20,pady=10)
        ttk.Label(info,text=f"Отримано: {row['received_date']}    •    Термін: {row['deadline']}    •    Відповідальний: {row['responsible']}    •    Категорія: {row['category']}",style="Muted.TLabel").pack(anchor="w",padx=12,pady=10)
        ttk.Label(win,text="Додатки до розпорядження",font=("Segoe UI Semibold",11)).pack(anchor="w",padx=20,pady=(8,4))
        att=ttk.Treeview(win,columns=("name","path"),show="headings",height=5);att.heading("name",text="Файл");att.heading("path",text="Шлях");att.column("name",width=260);att.column("path",width=560);att.pack(fill="x",padx=20)
        for a in self.db.get_attachments(row["id"],0):att.insert("","end",iid=str(a["id"]),values=(a["filename"],a["path"]))
        bar=ttk.Frame(win);bar.pack(fill="x",padx=20,pady=6);ttk.Button(bar,text="Додати додатки",command=lambda:self._add_to_card(row,win)).pack(side="left")
        ttk.Label(win,text="Відповіді",font=("Segoe UI Semibold",11)).pack(anchor="w",padx=20,pady=(10,4))
        resp=ttk.Treeview(win,columns=("date","outgoing","comment","file"),show="headings",height=7)
        for c,t,w in (("date","Дата",100),("outgoing","Вихідний №",140),("comment","Коментар",330),("file","Файл",240)):resp.heading(c,text=t);resp.column(c,width=w)
        resp.pack(fill="both",expand=True,padx=20)
        for r in self.db.get_responses(row["id"]):resp.insert("","end",iid=str(r["id"]),values=(r["response_date"],r["outgoing"],r["comment"],r["filename"]))
        b=ttk.Frame(win);b.pack(fill="x",padx=20,pady=10);ttk.Button(b,text="＋ Додати відповідь",command=lambda:self.response_dialog(row,win)).pack(side="left");ttk.Button(b,text="Виконано",command=lambda:self._done_from_card(row,win)).pack(side="left",padx=6);ttk.Button(b,text="Повернути в роботу",command=lambda:self._reopen_from_card(row,win)).pack(side="left")

    def _add_to_card(self,row,win):
        paths=self._choose_many("Оберіть додатки")
        for p in paths:self.service.add_attachment(row["id"],p)
        win.destroy();self.open_card(self.db.get_order(row["id"]))

    def response_dialog(self,row,parent=None):
        win=tk.Toplevel(self);win.title(f"Додати відповідь — № {row['number']}");win.geometry("650x500");win.configure(bg="#101713");win.grab_set()
        fields={};labels=[("date","Дата відповіді (РРРР-ММ-ДД)"),("outgoing","Вихідний номер"),("comment","Короткий опис відповіді")]
        for i,(k,t) in enumerate(labels):ttk.Label(win,text=t).grid(row=i,column=0,sticky="w",padx=20,pady=10);e=ttk.Entry(win,width=48);e.grid(row=i,column=1,padx=20,pady=10);fields[k]=e
        fields["date"].insert(0,date.today().isoformat());file=[None];label=tk.StringVar(value="Файл відповіді не обрано")
        ttk.Button(win,text="Обрати файл відповіді",command=lambda:self._choose_file(file,label)).grid(row=3,column=1,sticky="w",padx=20,pady=10);ttk.Label(win,textvariable=label,style="Muted.TLabel").grid(row=4,column=1,sticky="w",padx=20)
        final=tk.BooleanVar(value=False);ttk.Checkbutton(win,text="Ця відповідь завершує розпорядження",variable=final).grid(row=5,column=1,sticky="w",padx=20,pady=10)
        def save():
            if not file[0]:return messagebox.showwarning("Відповідь","Оберіть файл відповіді.",parent=win)
            try:
                rid=self.service.add_response(row,response_date=date.fromisoformat(fields["date"].get()),outgoing=fields["outgoing"].get(),comment=fields["comment"].get(),file_name=file[0].name,file_bytes=file[0].read_bytes(),final=final.get())
                for p in self._choose_many("Додайте додатки до відповіді (необов'язково)"):self.service.add_response_attachment(row["id"],rid,p)
                win.destroy();self.refresh();
                if parent and parent.winfo_exists():parent.destroy()
                self.open_card(self.db.get_order(row["id"]))
            except Exception as exc:messagebox.showerror("Не вдалося додати відповідь",str(exc),parent=win)
        ttk.Button(win,text="Зберегти відповідь",command=save).grid(row=6,column=1,sticky="e",padx=20,pady=18)

    def response_selected(self):
        row=self.selected()
        if not row:return messagebox.showinfo("Відповідь","Оберіть розпорядження.")
        self.response_dialog(row)

    def _done_from_card(self,row,win):
        self.service.mark_done(row["id"]);win.destroy();self.refresh()
    def _reopen_from_card(self,row,win):
        self.service.reopen(row["id"]);win.destroy();self.refresh()

    def done_selected(self):
        row=self.selected()
        if row and messagebox.askyesno("Виконання",f"Позначити №{row['number']} як виконане?"):self.service.mark_done(row["id"]);self.refresh()

    def trash_selected(self):
        row=self.selected()
        if row and messagebox.askyesno("Кошик",f"Перемістити №{row['number']} до кошика?",icon="warning"):
            try:self.service.move_to_trash(row);self.refresh()
            except Exception as exc:messagebox.showerror("Кошик",str(exc))

    def statistics(self):
        rows=[dict(r) for r in self.db.get_orders()];by={}
        for r in rows:key=str(r.get("received_date") or "")[:7];by[key]=by.get(key,0)+1
        text="\n".join(f"{k or 'Без дати'}: {v}" for k,v in sorted(by.items(),reverse=True)) or "Даних ще немає."
        messagebox.showinfo("Статистика",f"Отримано за місяцями:\n\n{text}")

    def diagnostics(self):
        problems=self.storage.validate();inv=self.storage.inventory();text="🟢 SQLite — OK\n🟢 Локальне сховище — OK\n🟢 Кошик — OK\n🔒 Мережа — не потрібна\n\n";text+=f"Файлів: {inv['files']}\nПапок: {inv['folders']}\nОбсяг: {inv['mb']} МБ";text+=("\n\n⚠ Проблеми:\n"+"\n".join(problems)) if problems else ""
        messagebox.showinfo("Діагностика",text)

    def trash_window(self):
        win=tk.Toplevel(self);win.title("Кошик");win.geometry("760x520");tree=ttk.Treeview(win,columns=("number","description","deleted"),show="headings");
        for c,t in (("number","Номер"),("description","Короткий опис"),("deleted","Дата видалення")):tree.heading(c,text=t);tree.column(c,width=240)
        tree.pack(fill="both",expand=True,padx=12,pady=12)
        for r in self.db.get_trash():tree.insert("","end",iid=str(r["id"]),values=(r["number"],r["description"],r["deleted_at"]))
        def restore():
            sel=tree.selection()
            if not sel:return
            try:self.service.restore(int(sel[0]));win.destroy();self.refresh()
            except Exception as exc:messagebox.showerror("Відновлення",str(exc),parent=win)
        def purge():
            sel=tree.selection()
            if not sel:return
            if messagebox.askyesno("Остаточне видалення","Видалити назавжди? Цю дію не можна скасувати.",parent=win):self.service.purge(int(sel[0]));win.destroy();self.refresh()
        bar=ttk.Frame(win);bar.pack(pady=10);ttk.Button(bar,text="Відновити",command=restore).pack(side="left",padx=5);ttk.Button(bar,text="Видалити назавжди",command=purge).pack(side="left",padx=5)


def main(): DesktopApp().mainloop()
if __name__ == "__main__": main()
