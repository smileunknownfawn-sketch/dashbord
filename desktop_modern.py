from __future__ import annotations

import shutil
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from core.analytics import MONTHS_UA, distribution, metrics, monthly, response_rate, responsible_table
from core.config import APP_TITLE, APP_VERSION, DEVELOPER
from desktop_final import DesktopDashboard


class ModernDashboard(DesktopDashboard):
    """Сучасний робочий інтерфейс: документи, аналітика та інфографіка."""

    BG = "#0b1110"
    PANEL = "#111a17"
    CARD = "#16221d"
    CARD_2 = "#1b2a23"
    LINE = "#2b4035"
    TEXT = "#eef5f0"
    MUTED = "#9aada1"
    ACCENT = "#66d39a"
    ACCENT_2 = "#3ea76f"
    WARN = "#e6b85c"
    DANGER = "#df746d"

    def __init__(self) -> None:
        super().__init__()

    def _build_ui(self) -> None:
        self.configure(bg=self.BG)
        self._configure_styles()

        self.shell = ttk.Frame(self, style="Shell.TFrame")
        self.shell.pack(fill="both", expand=True)

        self._build_header()
        self._build_workspace_bar()

        self.tabs = ttk.Notebook(self.shell, style="Modern.TNotebook")
        self.tabs.pack(fill="both", expand=True, padx=22, pady=(4, 14))

        self.orders_tab = ttk.Frame(self.tabs, style="Panel.TFrame")
        self.analytics_tab = ttk.Frame(self.tabs, style="Panel.TFrame")
        self.tabs.add(self.orders_tab, text="  РОЗПОРЯДЖЕННЯ  ")
        self.tabs.add(self.analytics_tab, text="  АНАЛІТИКА  ")

        self._build_orders_tab()
        self._build_analytics_tab()
        self._build_footer()
        self.bind("<Control-f>", lambda _e: self._focus_search())

    def _configure_styles(self) -> None:
        s = self.style
        s.configure("Shell.TFrame", background=self.BG)
        s.configure("Panel.TFrame", background=self.PANEL)
        s.configure("Card.TFrame", background=self.CARD)
        s.configure("TLabel", background=self.PANEL, foreground=self.TEXT, font=("Segoe UI Variable", 10))
        s.configure("Title.TLabel", background=self.BG, foreground=self.TEXT, font=("Segoe UI Variable", 24, "bold"))
        s.configure("Hero.TLabel", background=self.BG, foreground=self.ACCENT, font=("Segoe UI Variable", 10, "bold"))
        s.configure("Muted.TLabel", background=self.PANEL, foreground=self.MUTED, font=("Segoe UI Variable", 9))
        s.configure("CardTitle.TLabel", background=self.CARD, foreground=self.TEXT, font=("Segoe UI Variable", 10, "bold"))
        s.configure("Kpi.TLabel", background=self.CARD, foreground=self.TEXT, font=("Segoe UI Variable", 21, "bold"))
        s.configure("KpiSmall.TLabel", background=self.CARD, foreground=self.MUTED, font=("Segoe UI Variable", 9))
        s.configure("TButton", font=("Segoe UI Variable", 10), padding=(13, 8))
        s.configure("Accent.TButton", font=("Segoe UI Variable", 10, "bold"), padding=(14, 9), foreground="#07100c", background=self.ACCENT)
        s.map("Accent.TButton", background=[("active", "#82e2ad")])
        s.configure("Treeview", background="#0f1714", fieldbackground="#0f1714", foreground=self.TEXT, rowheight=36, font=("Segoe UI Variable", 9), borderwidth=0)
        s.configure("Treeview.Heading", background="#203129", foreground=self.TEXT, font=("Segoe UI Variable", 9, "bold"), relief="flat")
        s.map("Treeview", background=[("selected", "#24563e")], foreground=[("selected", "#ffffff")])
        s.configure("TNotebook", background=self.BG, borderwidth=0)
        s.configure("Modern.TNotebook", background=self.BG, borderwidth=0, tabmargins=0)
        s.configure("TNotebook.Tab", background=self.CARD, foreground=self.MUTED, padding=(18, 10), font=("Segoe UI Variable", 9, "bold"))
        s.map("TNotebook.Tab", background=[("selected", self.ACCENT_2)], foreground=[("selected", "#ffffff")])
        s.configure("TEntry", fieldbackground="#0f1714", foreground=self.TEXT, insertcolor=self.TEXT, padding=9, borderwidth=0)
        s.configure("TCombobox", fieldbackground="#0f1714", foreground=self.TEXT, padding=7)
        s.configure("TLabelframe", background=self.CARD, foreground=self.TEXT)
        s.configure("TLabelframe.Label", background=self.CARD, foreground=self.ACCENT, font=("Segoe UI Variable", 9, "bold"))

    def _build_header(self) -> None:
        header = ttk.Frame(self.shell, style="Shell.TFrame")
        header.pack(fill="x", padx=24, pady=(18, 8))
        left = ttk.Frame(header, style="Shell.TFrame")
        left.pack(side="left")
        ttk.Label(left, text="СИСТЕМА КОНТРОЛЮ", style="Hero.TLabel").pack(anchor="w")
        ttk.Label(left, text=APP_TITLE, style="Title.TLabel").pack(anchor="w", pady=(2, 0))
        ttk.Label(left, text=f"Версія {APP_VERSION}  •  локальний автономний режим", style="Muted.TLabel").pack(anchor="w", pady=(2, 0))

        right = ttk.Frame(header, style="Shell.TFrame")
        right.pack(side="right", anchor="n")
        self.header_kpi = tk.StringVar(value="Готово до роботи")
        ttk.Label(right, textvariable=self.header_kpi, style="Hero.TLabel").pack(anchor="e")
        ttk.Label(right, text="Мережа не потрібна", style="Muted.TLabel").pack(anchor="e", pady=(4, 0))

    def _build_workspace_bar(self) -> None:
        bar = ttk.Frame(self.shell, style="Card.TFrame")
        bar.pack(fill="x", padx=22, pady=(0, 10))
        self.workspace_var = tk.StringVar(value=str(self.root_path))
        ttk.Label(bar, text="РОБОЧА ПАПКА", style="CardTitle.TLabel").pack(side="left", padx=(14, 6), pady=10)
        ttk.Label(bar, textvariable=self.workspace_var, style="Muted.TLabel").pack(side="left", fill="x", expand=True, pady=10)
        ttk.Button(bar, text="Змінити папку", command=self.choose_root).pack(side="right", padx=8, pady=6)
        ttk.Button(bar, text="Відкрити папку", command=self.open_workspace).pack(side="right", padx=(0, 8), pady=6)

    def _build_orders_tab(self) -> None:
        top = ttk.Frame(self.orders_tab, style="Panel.TFrame")
        top.pack(fill="x", padx=18, pady=(18, 10))
        self.search_var = tk.StringVar()
        self.search = ttk.Entry(top, textvariable=self.search_var, font=("Segoe UI Variable", 10))
        self.search.pack(side="left", fill="x", expand=True, ipady=5)
        self.search.insert(0, "Пошук за номером, словами, відповідальним, категорією або файлом…")
        self.search.bind("<FocusIn>", self._clear_placeholder)
        self.search.bind("<KeyRelease>", lambda _e: self.refresh())
        ttk.Button(top, text="＋ Додати", style="Accent.TButton", command=self.add_order_dialog).pack(side="left", padx=8)
        ttk.Button(top, text="Додатки", command=self.add_attachments_selected).pack(side="left")
        ttk.Button(top, text="💾 Резервна копія", command=self.create_backup).pack(side="left", padx=8)

        self.kpi_frame = ttk.Frame(self.orders_tab, style="Panel.TFrame")
        self.kpi_frame.pack(fill="x", padx=18, pady=4)
        self.kpi_var = tk.StringVar()
        self._kpi_card(self.kpi_frame, "Усього", "0", 0)
        self._kpi_card(self.kpi_frame, "Виконано", "0", 1)
        self._kpi_card(self.kpi_frame, "У роботі", "0", 2)
        self._kpi_card(self.kpi_frame, "Прострочено", "0", 3)

        body = ttk.Frame(self.orders_tab, style="Panel.TFrame")
        body.pack(fill="both", expand=True, padx=18, pady=(8, 4))
        cols = ("number", "description", "deadline", "status", "responsible", "category")
        self.tree = ttk.Treeview(body, columns=cols, show="headings")
        titles = {"number": "Номер", "description": "Короткий опис", "deadline": "Термін", "status": "Стан", "responsible": "Відповідальний", "category": "Категорія"}
        widths = {"number": 120, "description": 480, "deadline": 125, "status": 165, "responsible": 190, "category": 170}
        for col in cols:
            self.tree.heading(col, text=titles[col])
            self.tree.column(col, width=widths[col], anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(body, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.bind("<Double-1>", lambda _e: self.open_card())

        actions = ttk.Frame(self.orders_tab, style="Panel.TFrame")
        actions.pack(fill="x", padx=18, pady=(5, 14))
        for text, cmd in (("Відкрити", self.open_card), ("＋ Відповідь", self.response_selected), ("✓ Виконано", self.done_selected), ("↶ У роботу", self.reopen_selected), ("🗑 У кошик", self.trash_selected)):
            ttk.Button(actions, text=text, command=cmd).pack(side="left", padx=(0, 6))
        ttk.Button(actions, text="Кошик", command=self.trash_window).pack(side="right")
        ttk.Button(actions, text="Діагностика", command=self.diagnostics).pack(side="right", padx=6)

    def _kpi_card(self, parent, title: str, value: str, column: int) -> None:
        card = ttk.Frame(parent, style="Card.TFrame")
        card.grid(row=0, column=column, sticky="nsew", padx=5)
        parent.columnconfigure(column, weight=1)
        value_var = tk.StringVar(value=value)
        setattr(self, f"kpi_{column}", value_var)
        ttk.Label(card, text=title, style="KpiSmall.TLabel").pack(anchor="w", padx=14, pady=(12, 0))
        ttk.Label(card, textvariable=value_var, style="Kpi.TLabel").pack(anchor="w", padx=14, pady=(0, 12))

    def _build_analytics_tab(self) -> None:
        controls = ttk.Frame(self.analytics_tab, style="Panel.TFrame")
        controls.pack(fill="x", padx=18, pady=(18, 8))
        ttk.Label(controls, text="Аналітика за рік", style="CardTitle.TLabel").pack(side="left", padx=(12, 8))
        self.analytics_year = ttk.Combobox(controls, state="readonly", width=10)
        self.analytics_year.pack(side="left")
        self.analytics_year.bind("<<ComboboxSelected>>", lambda _e: self.refresh_analytics())
        ttk.Button(controls, text="Оновити", command=self.refresh_analytics).pack(side="left", padx=8)
        ttk.Button(controls, text="Згорнути / розгорнути графіки", command=self.toggle_charts).pack(side="right", padx=8)

        self.analytics_summary = tk.StringVar(value="")
        ttk.Label(self.analytics_tab, textvariable=self.analytics_summary, style="Muted.TLabel").pack(anchor="w", padx=30, pady=(0, 8))

        self.chart_area = ttk.Frame(self.analytics_tab, style="Panel.TFrame")
        self.chart_area.pack(fill="both", expand=True, padx=18, pady=5)
        self.chart_area.columnconfigure(0, weight=3)
        self.chart_area.columnconfigure(1, weight=2)
        self.chart_area.rowconfigure(0, weight=3)
        self.chart_area.rowconfigure(1, weight=2)

        self.month_canvas = tk.Canvas(self.chart_area, bg=self.CARD, highlightthickness=0)
        self.month_canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.category_canvas = tk.Canvas(self.chart_area, bg=self.CARD, highlightthickness=0)
        self.category_canvas.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.resp_canvas = tk.Canvas(self.chart_area, bg=self.CARD, highlightthickness=0)
        self.resp_canvas.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.charts_visible = True

    def _build_footer(self) -> None:
        footer = ttk.Frame(self.shell, style="Shell.TFrame")
        footer.pack(fill="x", padx=24, pady=(0, 10))
        ttk.Label(footer, text=f"Розробник: {DEVELOPER}", style="Muted.TLabel").pack(side="left")
        ttk.Label(footer, text="Дані зберігаються тільки у вибраній робочій папці", style="Muted.TLabel").pack(side="right")

    def _clear_placeholder(self, _event=None):
        if self.search_var.get().startswith("Пошук за номером"):
            self.search_var.set("")

    def _focus_search(self):
        self._clear_placeholder()
        self.search.focus_set()

    def refresh(self):
        super().refresh()
        if hasattr(self, "workspace_var"):
            self.workspace_var.set(str(self.root_path))
        if hasattr(self, "header_kpi"):
            rows = [dict(r) for r in self.db.get_orders()]
            m = metrics(rows, date.today())
            self.header_kpi.set(f"{m.total} розпоряджень  •  виконано {m.completion_rate}%")
            self.kpi_0.set(str(m.total)); self.kpi_1.set(str(m.completed)); self.kpi_2.set(str(m.active)); self.kpi_3.set(str(m.overdue))
            self._sync_years(rows)
            self.refresh_analytics()

    def _sync_years(self, rows):
        years = sorted({str(r.get("received_date", "") or "")[:4] for r in rows if str(r.get("received_date", ""))[:4].isdigit()}, reverse=True)
        current = str(date.today().year)
        if current not in years: years.insert(0, current)
        self.analytics_year["values"] = years
        if not self.analytics_year.get() or self.analytics_year.get() not in years:
            self.analytics_year.set(years[0])

    def refresh_analytics(self):
        if not hasattr(self, "month_canvas"):
            return
        rows = [dict(r) for r in self.db.get_orders()]
        try:
            year = int(self.analytics_year.get())
        except (TypeError, ValueError):
            year = date.today().year
        m = metrics(rows, date.today())
        self.analytics_summary.set(f"{year}: отримано {sum(x['отримано'] for x in monthly(rows, year))}  •  виконано {m.completed} загалом  •  прострочено {m.overdue}  •  частка виконання {m.completion_rate}%")
        if self.charts_visible:
            self._draw_month_chart(rows, year)
            self._draw_category_chart(rows)
            self._draw_responsible_chart(rows)

    def toggle_charts(self):
        self.charts_visible = not self.charts_visible
        if self.charts_visible:
            self.month_canvas.grid(); self.category_canvas.grid(); self.resp_canvas.grid(); self.refresh_analytics()
        else:
            self.month_canvas.grid_remove(); self.category_canvas.grid_remove(); self.resp_canvas.grid_remove()

    def _draw_month_chart(self, rows, year):
        c = self.month_canvas; c.delete("all")
        c.update_idletasks(); w=max(c.winfo_width(), 500); h=max(c.winfo_height(), 260)
        c.create_text(18, 18, anchor="w", text=f"Надходження та виконання — {year}", fill=self.TEXT, font=("Segoe UI Variable", 12, "bold"))
        data = monthly(rows, year); maximum=max([x["отримано"] for x in data] + [1]); left=42; bottom=h-36; chart_h=h-75; step=(w-70)/12
        for i, item in enumerate(data):
            x=left+i*step+step*0.18; bar_w=step*0.28
            val=item["отримано"]; bh=(val/maximum)*chart_h
            c.create_rectangle(x,bottom-bh,x+bar_w,bottom,fill=self.ACCENT,outline="")
            done=item["виконано"]; dh=(done/maximum)*chart_h
            c.create_rectangle(x+bar_w+3,bottom-dh,x+bar_w*2+3,bottom,fill=self.ACCENT_2,outline="")
            c.create_text(x+bar_w, bottom+14, text=MONTHS_UA[i][:3], fill=self.MUTED, font=("Segoe UI Variable",8))
        c.create_text(w-150, 18, anchor="w", text="■ отримано   ■ виконано", fill=self.MUTED, font=("Segoe UI Variable",8))

    def _draw_category_chart(self, rows):
        c=self.category_canvas; c.delete("all"); c.update_idletasks(); w=max(c.winfo_width(),350); h=max(c.winfo_height(),260)
        c.create_text(18,18,anchor="w",text="Розподіл за категоріями",fill=self.TEXT,font=("Segoe UI Variable",12,"bold"))
        data=distribution(rows,"category","Інше"); items=list(data.items())[:7]; total=max(sum(data.values()),1); y=55
        for name,value in items:
            width=max(2,(w-155)*value/total); c.create_text(18,y,anchor="w",text=name[:20],fill=self.MUTED,font=("Segoe UI Variable",8)); c.create_rectangle(125,y-7,125+width,y+7,fill=self.ACCENT_2,outline=""); c.create_text(130+width,y,anchor="w",text=str(value),fill=self.TEXT,font=("Segoe UI Variable",8,"bold")); y+=27

    def _draw_responsible_chart(self, rows):
        c=self.resp_canvas; c.delete("all"); c.update_idletasks(); w=max(c.winfo_width(),700); h=max(c.winfo_height(),180)
        c.create_text(18,16,anchor="w",text="Навантаження відповідальних",fill=self.TEXT,font=("Segoe UI Variable",12,"bold"))
        items=responsible_table(rows)[:8]; y=48
        for item in items:
            pct=float(item["відсоток"]); width=max(2,(w-300)*pct/100); name=str(item["відповідальний"])[:28]
            c.create_text(18,y,anchor="w",text=name,fill=self.MUTED,font=("Segoe UI Variable",8)); c.create_rectangle(190,y-6,190+width,y+6,fill=self.ACCENT,outline=""); c.create_text(min(w-10,200+width),y,anchor="w",text=f"{pct:.0f}%  |  {item['усього']}",fill=self.TEXT,font=("Segoe UI Variable",8,"bold")); y+=22

    def choose_root(self):
        chosen=filedialog.askdirectory(title="Оберіть папку, де зберігатимуться всі дані розпоряджень",initialdir=str(self.root_path))
        if not chosen: return
        new_root=Path(chosen).resolve()
        if new_root == self.root_path.resolve(): return
        if self._path_inside(new_root, self.root_path) or self._path_inside(self.root_path, new_root):
            messagebox.showerror("Папка даних","Не можна вибрати вкладену папку поточного сховища.")
            return
        has_data=any(self.root_path.iterdir()) if self.root_path.exists() else False
        if has_data and messagebox.askyesno("Перенести дані", "Перенести всю поточну ієрархію розпоряджень у нову папку?\n\nСтаре сховище не буде видалено."):
            try:
                self._copy_workspace(self.root_path, new_root)
            except Exception as exc:
                messagebox.showerror("Перенесення", f"Не вдалося перенести дані:\n\n{exc}")
                return
        self.root_path=new_root; self._save_root(); self._open_services(); self.refresh()
        messagebox.showinfo("Папку змінено", f"Усі нові файли зберігатимуться тут:\n\n{new_root}")

    @staticmethod
    def _path_inside(path: Path, parent: Path) -> bool:
        try:
            path.relative_to(parent.resolve()); return True
        except ValueError:
            return False

    @staticmethod
    def _copy_workspace(source: Path, destination: Path) -> None:
        destination.mkdir(parents=True, exist_ok=True)
        for item in source.iterdir():
            target=destination/item.name
            if item.is_dir(): shutil.copytree(item,target,dirs_exist_ok=True)
            else: shutil.copy2(item,target)

    def open_workspace(self):
        self.open_path(".")
