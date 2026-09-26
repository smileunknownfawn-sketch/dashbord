from __future__ import annotations

import ctypes
import json
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from desktop_modern import ModernDashboard

THEMES = {
    "Темна військова": {"BG":"#0b1110","PANEL":"#111a17","CARD":"#16221d","TEXT":"#eef5f0","MUTED":"#9aada1","ACCENT":"#66d39a","ACCENT_2":"#3ea76f","ENTRY":"#0f1714","HEADING":"#203129","SELECT":"#24563e"},
    "Графітова командна": {"BG":"#0d1016","PANEL":"#151a23","CARD":"#1c222e","TEXT":"#f1f4f8","MUTED":"#9ba7b7","ACCENT":"#70a7ff","ACCENT_2":"#477fcb","ENTRY":"#111620","HEADING":"#273242","SELECT":"#2c5688"},
    "Світла офісна": {"BG":"#eef2f0","PANEL":"#f7f9f8","CARD":"#ffffff","TEXT":"#18231e","MUTED":"#64736b","ACCENT":"#217a4b","ACCENT_2":"#2e9660","ENTRY":"#ffffff","HEADING":"#e1e9e4","SELECT":"#cce7d8"},
}

class ReleaseDashboard(ModernDashboard):
    """Фінальна оболонка 1.0.1: теми, налаштування, DPI та локальні ресурси."""
    def __init__(self) -> None:
        self.theme_name = "Темна військова"
        self.font_scale = 1.0
        self.compact_rows = False
        self._enable_windows_dpi()
        super().__init__()
        self._load_ui_settings()
        self._install_release_controls()
        self._apply_theme()

    def _enable_windows_dpi(self) -> None:
        if not sys.platform.startswith("win"): return
        try: ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try: ctypes.windll.user32.SetProcessDPIAware()
            except Exception: pass

    @property
    def _settings_file(self) -> Path: return Path(self.root_path) / "налаштування_інтерфейсу.json"

    def _load_ui_settings(self) -> None:
        try:
            if self._settings_file.exists():
                data=json.loads(self._settings_file.read_text(encoding="utf-8"))
                self.theme_name=data.get("theme",self.theme_name); self.font_scale=float(data.get("font_scale",1.0)); self.compact_rows=bool(data.get("compact_rows",False))
        except Exception: pass
        if self.theme_name not in THEMES: self.theme_name="Темна військова"
        self.font_scale=min(1.35,max(0.85,self.font_scale))

    def _save_ui_settings(self) -> None:
        try:
            self._settings_file.parent.mkdir(parents=True,exist_ok=True)
            self._settings_file.write_text(json.dumps({"theme":self.theme_name,"font_scale":self.font_scale,"compact_rows":self.compact_rows},ensure_ascii=False,indent=2),encoding="utf-8")
        except Exception: pass

    def _install_release_controls(self) -> None:
        bar=ttk.Frame(self.shell,style="Card.TFrame"); bar.pack(fill="x",padx=22,pady=(0,8))
        ttk.Label(bar,text="ОФОРМЛЕННЯ",style="CardTitle.TLabel").pack(side="left",padx=(14,8),pady=8)
        self.theme_combo=ttk.Combobox(bar,values=list(THEMES),state="readonly",width=24); self.theme_combo.set(self.theme_name); self.theme_combo.pack(side="left",pady=6); self.theme_combo.bind("<<ComboboxSelected>>",lambda _e:self._theme_selected())
        ttk.Button(bar,text="⚙ Налаштування",command=self.open_settings).pack(side="right",padx=8,pady=6)
        ttk.Label(bar,text="Тема • масштаб шрифту • щільність таблиці",style="Muted.TLabel").pack(side="right",padx=6)

    def _apply_theme(self) -> None:
        c=THEMES[self.theme_name]; self.BG=c["BG"]; self.PANEL=c["PANEL"]; self.CARD=c["CARD"]; self.TEXT=c["TEXT"]; self.MUTED=c["MUTED"]; self.ACCENT=c["ACCENT"]; self.ACCENT_2=c["ACCENT_2"]
        s=self.style; size=round(10*self.font_scale); small=max(8,round(9*self.font_scale)); title=max(20,round(24*self.font_scale))
        s.configure("Shell.TFrame",background=self.BG); s.configure("Panel.TFrame",background=self.PANEL); s.configure("Card.TFrame",background=self.CARD)
        s.configure("TLabel",background=self.PANEL,foreground=self.TEXT,font=("Segoe UI Variable",size)); s.configure("Title.TLabel",background=self.BG,foreground=self.TEXT,font=("Segoe UI Variable",title,"bold")); s.configure("Hero.TLabel",background=self.BG,foreground=self.ACCENT,font=("Segoe UI Variable",small,"bold")); s.configure("Muted.TLabel",background=self.PANEL,foreground=self.MUTED,font=("Segoe UI Variable",small)); s.configure("CardTitle.TLabel",background=self.CARD,foreground=self.TEXT,font=("Segoe UI Variable",size,"bold")); s.configure("Kpi.TLabel",background=self.CARD,foreground=self.TEXT,font=("Segoe UI Variable",round(21*self.font_scale),"bold")); s.configure("KpiSmall.TLabel",background=self.CARD,foreground=self.MUTED,font=("Segoe UI Variable",small)); s.configure("TButton",font=("Segoe UI Variable",size),padding=(13,8)); s.configure("Accent.TButton",font=("Segoe UI Variable",size,"bold"),foreground=self.BG,background=self.ACCENT)
        s.configure("Treeview",background=c["ENTRY"],fieldbackground=c["ENTRY"],foreground=self.TEXT,rowheight=round((31 if self.compact_rows else 36)*self.font_scale),font=("Segoe UI Variable",small)); s.configure("Treeview.Heading",background=c["HEADING"],foreground=self.TEXT,font=("Segoe UI Variable",small,"bold")); s.map("Treeview",background=[("selected",c["SELECT"])],foreground=[("selected",self.TEXT)])
        s.configure("Modern.TNotebook",background=self.BG); s.configure("TNotebook.Tab",background=self.CARD,foreground=self.MUTED,font=("Segoe UI Variable",small,"bold")); s.map("TNotebook.Tab",background=[("selected",self.ACCENT_2)],foreground=[("selected","#ffffff")]); s.configure("TEntry",fieldbackground=c["ENTRY"],foreground=self.TEXT,insertcolor=self.TEXT); s.configure("TCombobox",fieldbackground=c["ENTRY"],foreground=self.TEXT); s.configure("TLabelframe",background=self.CARD,foreground=self.TEXT); s.configure("TLabelframe.Label",background=self.CARD,foreground=self.ACCENT)
        self.configure(bg=self.BG)
        for n in ("month_canvas","category_canvas","resp_canvas"):
            canvas=getattr(self,n,None)
            if canvas is not None: canvas.configure(bg=self.CARD)
        if hasattr(self,"theme_combo"): self.theme_combo.set(self.theme_name)
        self._save_ui_settings(); self.update_idletasks(); self.refresh_analytics()

    def _theme_selected(self): self.theme_name=self.theme_combo.get(); self._apply_theme()

    def open_settings(self):
        win=tk.Toplevel(self); win.title("Налаштування"); win.geometry("560x430"); win.resizable(False,False); win.transient(self); win.grab_set()
        frame=ttk.Frame(win,style="Card.TFrame"); frame.pack(fill="both",expand=True,padx=16,pady=16)
        ttk.Label(frame,text="НАЛАШТУВАННЯ ПРОГРАМИ",style="Title.TLabel").pack(anchor="w",padx=18,pady=(18,16))
        ttk.Label(frame,text="Тема оформлення",style="CardTitle.TLabel").pack(anchor="w",padx=18); theme=ttk.Combobox(frame,values=list(THEMES),state="readonly",width=34); theme.set(self.theme_name); theme.pack(anchor="w",padx=18,pady=(5,14))
        ttk.Label(frame,text="Розмір шрифту",style="CardTitle.TLabel").pack(anchor="w",padx=18); scale=tk.DoubleVar(value=self.font_scale); ttk.Scale(frame,from_=0.85,to=1.35,variable=scale,orient="horizontal",length=350).pack(anchor="w",padx=18,pady=8)
        compact=tk.BooleanVar(value=self.compact_rows); ttk.Checkbutton(frame,text="Компактний режим таблиці",variable=compact).pack(anchor="w",padx=18,pady=8)
        ttk.Label(frame,text="Налаштування зберігаються у вибраній папці даних.",style="Muted.TLabel").pack(anchor="w",padx=18,pady=8)
        def save(): self.theme_name=theme.get(); self.font_scale=round(float(scale.get()),2); self.compact_rows=compact.get(); self._apply_theme(); win.destroy()
        ttk.Button(frame,text="Зберегти",style="Accent.TButton",command=save).pack(anchor="e",padx=18,pady=18)

    def _resource(self,*parts:str)->Path: return Path(getattr(sys,"_MEIPASS",Path(__file__).resolve().parent)).joinpath(*parts)

    def _play_sound(self):
        sound=self._resource("sounds","opiat-rabota.mp3")
        if not sound.exists() or not sys.platform.startswith("win"): return
        try:
            alias="vom_dashboard_sound"; mci=ctypes.windll.winmm.mciSendStringW; mci(f'open "{sound}" type mpegvideo alias {alias}',None,0,0); mci(f"play {alias}",None,0,0); self.after(3500,lambda:mci(f"close {alias}",None,0,0))
        except Exception: pass

    def add_order_dialog(self): self._play_sound(); return super().add_order_dialog()

    def add_attachments_selected(self):
        row=self.selected()
        if not row: return messagebox.showinfo("Додатки","Оберіть розпорядження.")
        paths=filedialog.askopenfilenames(title="Оберіть необов'язкові додатки до розпорядження"); errors=[]
        for raw in paths:
            try: self.service.add_attachment(row["id"],Path(raw))
            except Exception as exc: errors.append(str(exc))
        if errors: messagebox.showerror("Додатки","Не всі додатки вдалося зберегти:\n\n"+"\n".join(errors))
        elif paths: messagebox.showinfo("Додатки",f"Додано файлів: {len(paths)}")

def main(): ReleaseDashboard().mainloop()

if __name__=="__main__": main()
