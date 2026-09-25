import base64
import html
import mimetypes
import shutil
import sqlite3
import time
from calendar import monthrange
from datetime import date, datetime, timedelta
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Процес виконання розпоряджень", page_icon="🇺🇦", layout="wide", initial_sidebar_state="collapsed")

APP = Path(__file__).resolve().parent
DEFAULT_WORKSPACE = APP / "data"
DEFAULTS = {
    "workspace": str(DEFAULT_WORKSPACE), "page": "Головна", "add_open": False,
    "response_order": None, "viewer_order": None, "viewer_response": None,
    "delete_order": None, "edit_order": None, "language": "Українська",
    "language_popup": False, "just_added": False, "calendar_year": date.today().year,
    "calendar_month": date.today().month, "calendar_selected": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

WORK = Path(st.session_state.workspace).resolve()
ORDERS = WORK / "Розпорядження"
BACKUPS = WORK / "Резервні копії"
WORK.mkdir(parents=True, exist_ok=True)
ORDERS.mkdir(parents=True, exist_ok=True)
BACKUPS.mkdir(parents=True, exist_ok=True)
DB = WORK / "database.db"

MONTHS = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]
PRIORITIES = ["Звичайний", "Важливий", "Терміновий", "Критичний"]
CATEGORIES = ["Організаційне", "Особовий склад", "Матеріальне", "Навчання", "Інше"]
STATUSES = {"progress": "У РОБОТІ", "today": "ТЕРМІН СЬОГОДНІ", "overdue": "ПРОСТРОЧЕНО", "done": "ВИКОНАНО"}

CSS = """
<style>
:root{--bg:#050907;--panel:rgba(10,19,14,.94);--line:rgba(190,214,193,.12);--text:#eef5ef;--muted:#9eaca1;--gold:#d3b263;--green:#75bd8c;--red:#ef746d;--yellow:#e5c766}
html,body,[class*=css]{font-family:"Segoe UI",Arial,sans-serif}
.stApp{background:radial-gradient(circle at 15% 10%,rgba(81,111,70,.24),transparent 26%),radial-gradient(circle at 88% 18%,rgba(191,157,75,.10),transparent 24%),linear-gradient(135deg,#020504 0%,#08120d 46%,#030605 100%);color:var(--text)}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.09;background-image:linear-gradient(rgba(200,220,200,.2) 1px,transparent 1px),linear-gradient(90deg,rgba(200,220,200,.2) 1px,transparent 1px);background-size:56px 56px}
.stApp:after{content:"";position:fixed;inset:0;pointer-events:none;opacity:.05;background:radial-gradient(ellipse at center,transparent 40%,#000 100%)}
.block-container{max-width:1550px;padding:1rem 2.5rem 5rem}.hero{padding:.8rem 0 1.1rem}.hero h1{font-size:clamp(2.1rem,4vw,3.9rem);font-weight:900;letter-spacing:-.055em;margin:.15rem 0 .25rem;font-style:normal}.eyebrow{font-size:.65rem;letter-spacing:.24em;color:#b8c7b5;font-weight:900}.version{text-align:right;color:#8f9e92;font-size:.68rem;letter-spacing:.14em;font-weight:900;padding-top:.25rem}
.panel,.metric,.order,.notice,.calendar-card{background:var(--panel);border:1px solid var(--line);border-radius:18px;box-shadow:0 18px 50px rgba(0,0,0,.2)}.panel{padding:1.1rem}.metric{padding:1rem;min-height:105px}.metric .label{color:#9eaca1;font-size:.66rem;font-weight:900;letter-spacing:.12em}.metric .num{font-size:2.15rem;font-weight:950;margin:.12rem 0}.kpi,.muted{color:var(--muted);font-size:.72rem}.order{margin:.65rem 0;padding:1rem 1.1rem;border-left:5px solid var(--gold)}.order.overdue{border-left-color:var(--red)}.order.today{border-left-color:var(--yellow)}.order.done{border-left-color:var(--green)}.desc{color:#cbd5cc;line-height:1.55;margin:.45rem 0}.badge{display:inline-block;padding:.32rem .65rem;border-radius:999px;font-size:.61rem;font-weight:950}.work{color:#d8ba69;background:#d8ba6918}.late{color:#ef7770;background:#ef777018}.finished{color:#79c995;background:#79c99518}.todaybadge{color:#ead06b;background:#ead06b18}.critical{color:#ff8b83}.navrow{margin:.5rem 0 1.2rem}.section-title{font-size:1.05rem;font-weight:950;letter-spacing:.04em;margin:1.2rem 0 .7rem}.stButton>button{border-radius:11px;background:rgba(120,146,95,.10);border:1px solid rgba(169,188,145,.23);color:#e4ece3;font-weight:900;min-height:42px}.stButton>button:hover{border-color:rgba(218,194,111,.8);background:rgba(208,174,98,.13)}.stTextInput input,.stTextArea textarea,.stDateInput input,.stNumberInput input{background:rgba(0,0,0,.40)!important;color:#fff!important;border-color:rgba(190,214,193,.15)!important}.stSelectbox div[data-baseweb="select"]>div{background:rgba(0,0,0,.40)}.stFileUploader{background:rgba(0,0,0,.16);border-radius:14px}.successbox{padding:15px;border:1px solid #84b88e55;border-radius:14px;background:#183522;margin:.5rem 0 1rem}.chartbar{height:13px;border-radius:8px;background:linear-gradient(90deg,#63875a,#d1b05e)}.timeline-item{padding:.72rem 0;border-left:2px solid #63875a;padding-left:1rem;margin-left:.4rem}.calendar-card{padding:.8rem;text-align:center;min-height:92px}.calendar-day{font-size:.72rem;color:#9eaca1}.calendar-count{font-size:1.45rem;font-weight:950}.calendar-red{color:#ef746d}.calendar-green{color:#75bd8c}.focus{border:1px solid #d3b26345;background:linear-gradient(135deg,rgba(211,178,99,.10),rgba(10,19,14,.95));border-radius:18px;padding:1.1rem}.tag{display:inline-block;padding:.25rem .55rem;margin:.15rem;border-radius:999px;background:#ffffff0b;border:1px solid #ffffff12;font-size:.65rem;color:#bdc9be}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,number TEXT NOT NULL,deadline TEXT NOT NULL,description TEXT NOT NULL,folder TEXT NOT NULL,filename TEXT NOT NULL,path TEXT NOT NULL,mime TEXT NOT NULL,status TEXT DEFAULT 'progress',completion_outgoing TEXT DEFAULT '',priority TEXT DEFAULT 'Звичайний',responsible TEXT DEFAULT '',category TEXT DEFAULT 'Інше',received_date TEXT DEFAULT '',tags TEXT DEFAULT '',created_at TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS responses(id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER NOT NULL,response_date TEXT NOT NULL,outgoing TEXT DEFAULT '',comment TEXT DEFAULT '',filename TEXT NOT NULL,path TEXT NOT NULL,mime TEXT NOT NULL,is_final INTEGER DEFAULT 0,created_at TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER,event_type TEXT NOT NULL,details TEXT DEFAULT '',created_at TEXT NOT NULL)")
    cols = {r[1] for r in c.execute("PRAGMA table_info(orders)").fetchall()}
    migrations = {"priority":"TEXT DEFAULT 'Звичайний'","responsible":"TEXT DEFAULT ''","category":"TEXT DEFAULT 'Інше'","received_date":"TEXT DEFAULT ''","tags":"TEXT DEFAULT ''"}
    for name, definition in migrations.items():
        if name not in cols:
            c.execute(f"ALTER TABLE orders ADD COLUMN {name} {definition}")
    c.commit()
    return c


def safe_name(value):
    return "".join(ch if ch.isalnum() or ch in " ._-()[]" else "_" for ch in str(value).strip()) or "Документ"


def event(order_id, kind, details=""):
    c = db(); c.execute("INSERT INTO events(order_id,event_type,details,created_at) VALUES(?,?,?,?)", (order_id, kind, details, datetime.now().isoformat())); c.commit(); c.close()


def save_upload(upload, folder):
    folder.mkdir(parents=True, exist_ok=True); p = folder / safe_name(upload.name); n = 2
    while p.exists(): p = folder / f"{p.stem}_{n}{p.suffix}"; n += 1
    p.write_bytes(upload.getvalue()); return p


def state(row):
    if row["status"] == "done": return "done"
    try:
        d = date.fromisoformat(row["deadline"])
        if d < date.today(): return "overdue"
        if d == date.today(): return "today"
    except Exception: pass
    return "progress"


def remaining(deadline):
    try:
        d = (date.fromisoformat(deadline) - date.today()).days
        if d < 0: return f"прострочено на {abs(d)} дн."
        if d == 0: return "термін сьогодні"
        if d == 1: return "залишився 1 день"
        return f"залишилося {d} днів"
    except Exception: return ""


def add_order(number, received, deadline, description, upload, priority, responsible, category, tags):
    folder = ORDERS / safe_name(number); n = 2
    while folder.exists(): folder = ORDERS / f"{safe_name(number)}_{n}"; n += 1
    p = save_upload(upload, folder)
    c = db(); cur = c.execute("INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,priority,responsible,category,received_date,tags,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (number.strip(), deadline.isoformat(), description.strip(), folder.name, p.name, str(p.relative_to(WORK)), upload.type or mimetypes.guess_type(p.name)[0] or "application/octet-stream", "progress", priority, responsible.strip(), category, received.isoformat(), tags.strip(), datetime.now().isoformat())); oid = cur.lastrowid; c.commit(); c.close(); event(oid, "Створено", f"№ {number.strip()}")


def update_order(oid, number, deadline, description, priority, responsible, category, tags):
    c = db(); c.execute("UPDATE orders SET number=?,deadline=?,description=?,priority=?,responsible=?,category=?,tags=? WHERE id=?", (number.strip(), deadline.isoformat(), description.strip(), priority, responsible.strip(), category, tags.strip(), oid)); c.commit(); c.close(); event(oid, "Змінено", "Оновлено дані розпорядження")


def add_response(row, response_date, outgoing, comment, upload, final):
    folder = ORDERS / row["folder"] / "Відповіді"; p = save_upload(upload, folder); c = db(); c.execute("INSERT INTO responses(order_id,response_date,outgoing,comment,filename,path,mime,is_final,created_at) VALUES(?,?,?,?,?,?,?,?,?)", (row["id"], response_date.isoformat(), outgoing.strip(), comment.strip(), p.name, str(p.relative_to(WORK)), upload.type or mimetypes.guess_type(p.name)[0] or "application/octet-stream", int(final), datetime.now().isoformat()))
    if final: c.execute("UPDATE orders SET status='done',completion_outgoing=? WHERE id=?", (outgoing.strip(), row["id"]))
    c.commit(); c.close(); event(row["id"], "Додано відповідь", outgoing.strip() or "Без вихідного номера")
    if final: event(row["id"], "Виконано", outgoing.strip())


def delete_order(oid):
    c = db(); row = c.execute("SELECT folder FROM orders WHERE id=?", (oid,)).fetchone()
    if not row: c.close(); return
    folder = (ORDERS / row["folder"]).resolve()
    try: folder.relative_to(ORDERS.resolve())
    except ValueError: c.close(); raise RuntimeError("Небезпечний шлях папки")
    c.execute("DELETE FROM responses WHERE order_id=?", (oid,)); c.execute("DELETE FROM events WHERE order_id=?", (oid,)); c.execute("DELETE FROM orders WHERE id=?", (oid,)); c.commit(); c.close()
    if folder.exists(): shutil.rmtree(folder)


def backup():
    target = BACKUPS / f"Резервна_копія_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"; target.mkdir(parents=True, exist_ok=True)
    if DB.exists(): shutil.copy2(DB, target / "database.db")
    if ORDERS.exists(): shutil.copytree(ORDERS, target / "Розпорядження", dirs_exist_ok=True)
    return target


def local_path(rel):
    p = (WORK / rel).resolve()
    try: p.relative_to(WORK.resolve())
    except ValueError: return None
    return p if p.exists() else None


def show_file(row):
    p = local_path(row["path"])
    if not p: st.error("Файл не знайдено у папці даних."); return
    mime = row["mime"] or mimetypes.guess_type(p.name)[0] or "application/octet-stream"; data = p.read_bytes()
    st.markdown(f"**{html.escape(p.name)}** · `{mime}`")
    st.download_button("⬇ ЗАВАНТАЖИТИ ФАЙЛ", data=data, file_name=p.name, mime=mime, key=f"download_{row['id']}")
    if mime == "application/pdf" or p.suffix.lower() == ".pdf":
        b64 = base64.b64encode(data).decode(); st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="760" style="border:1px solid #ffffff18;border-radius:12px"></iframe>', unsafe_allow_html=True)
    elif mime.startswith("image/"): st.image(data, use_container_width=True)
    elif mime.startswith("text/") or p.suffix.lower() in {".txt", ".csv", ".log", ".md"}: st.code(data.decode("utf-8", errors="replace"), language="text")
    else: st.info("Для цього формату доступне завантаження файлу.")


def play_sound():
    p = APP / "sounds" / "opiat-rabota.mp3"
    if p.exists():
        b64 = base64.b64encode(p.read_bytes()).decode(); st.markdown(f'<audio autoplay><source src="data:audio/mpeg;base64,{b64}"></audio>', unsafe_allow_html=True)


def orders():
    c = db(); rows = c.execute("SELECT * FROM orders ORDER BY deadline ASC,id DESC").fetchall(); c.close(); return rows


def events(oid):
    c = db(); r = c.execute("SELECT * FROM events WHERE order_id=? ORDER BY created_at ASC", (oid,)).fetchall(); c.close(); return r


def responses(oid):
    c = db(); r = c.execute("SELECT * FROM responses WHERE order_id=? ORDER BY response_date DESC,id DESC", (oid,)).fetchall(); c.close(); return r


def metric(label, value, hint):
    st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="num">{value}</div><div class="kpi">{html.escape(hint)}</div></div>', unsafe_allow_html=True)


def ensure_demo():
    c = db()
    if c.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
        folder = ORDERS / "01-2026"; folder.mkdir(exist_ok=True); p = folder / "Розпорядження_01-2026.txt"; p.write_text("ДЕМОНСТРАЦІЙНЕ РОЗПОРЯДЖЕННЯ\n\nПідготувати та надати узагальнену інформацію про стан виконання визначених завдань.", encoding="utf-8")
        cur = c.execute("INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,priority,responsible,category,received_date,tags,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", ("01/2026", "2026-10-05", "Підготувати та надати узагальнену інформацію про стан виконання визначених завдань.", folder.name, p.name, str(p.relative_to(WORK)), "text/plain", "progress", "Звичайний", "", "Організаційне", date.today().isoformat(), "демо", datetime.now().isoformat())); oid = cur.lastrowid; c.execute("INSERT INTO events(order_id,event_type,details,created_at) VALUES(?,?,?,?)", (oid, "Створено", "Демонстраційний запис", datetime.now().isoformat())); c.commit()
    c.close()


def navigation():
    labels = [("🏠 ГОЛОВНА", "Головна"), ("📋 РОЗПОРЯДЖЕННЯ", "Розпорядження"), ("📊 АНАЛІТИКА", "Аналітика"), ("🗓 КАЛЕНДАР", "Календар"), ("⚙️ НАЛАШТУВАННЯ", "Налаштування")]
    cols = st.columns(5)
    for col, (label, page) in zip(cols, labels):
        with col:
            if st.button(label, key=f"nav_{page}"): st.session_state.page = page; st.rerun()


def add_form():
    if not st.session_state.add_open: return
    with st.form("new_order", clear_on_submit=True):
        st.markdown("### ＋ НОВЕ РОЗПОРЯДЖЕННЯ")
        st.caption("Усі дані збережуться у локальній папці, а файл автоматично буде прив'язаний до цього номера.")
        a,b,c = st.columns(3)
        with a: number = st.text_input("№ розпорядження", placeholder="Наприклад: 1111/2026")
        with b: received = st.date_input("Дата отримання", value=date.today())
        with c: deadline = st.date_input("Термін виконання", value=date.today())
        a,b,c = st.columns(3)
        with a: priority = st.selectbox("Пріоритет", PRIORITIES)
        with b: category = st.selectbox("Категорія", CATEGORIES)
        with c: responsible = st.text_input("Відповідальний", placeholder="Підрозділ або прізвище")
        tags = st.text_input("Мітки", placeholder="Наприклад: термінове, контроль, навчання")
        description = st.text_area("Короткий опис розпорядження", placeholder="Коротко опишіть, що саме необхідно виконати...", height=120)
        upload = st.file_uploader("Файл розпорядження", type=None, help="Оберіть PDF, Word, Excel, архів або інший файл розпорядження.")
        a,b = st.columns(2); save = a.form_submit_button("💾 ЗБЕРЕГТИ РОЗПОРЯДЖЕННЯ"); cancel = b.form_submit_button("СКАСУВАТИ")
        if cancel: st.session_state.add_open = False; st.rerun()
        if save:
            if not number.strip(): st.error("Вкажіть номер розпорядження.")
            elif not description.strip(): st.error("Додайте короткий опис розпорядження.")
            elif not upload: st.error("Оберіть файл розпорядження.")
            else: add_order(number, received, deadline, description, upload, priority, responsible, category, tags); st.session_state.add_open = False; st.session_state.just_added = True; st.rerun()


ensure_demo()

# Верхня панель
left, right = st.columns([5,1])
with left:
    lang = st.selectbox("Мова інтерфейсу", ["Українська", "Російська"], index=0 if st.session_state.language == "Українська" else 1, label_visibility="collapsed")
    if lang != st.session_state.language: st.session_state.language = lang; st.session_state.language_popup = lang == "Російська"; st.rerun()
    st.markdown(f'<div class="muted">Мова інтерфейсу — <b>{html.escape(lang)}</b></div>', unsafe_allow_html=True)
with right: st.markdown('<div class="version">ВЕРСІЯ 2.1</div>', unsafe_allow_html=True)

if st.session_state.language_popup and st.session_state.language == "Російська":
    img = APP / "language-russian.jpg"
    if img.exists():
        b64 = base64.b64encode(img.read_bytes()).decode(); st.markdown(f'<div style="text-align:center;background:#050807;border:1px solid #d0ae6266;border-radius:18px;padding:16px;margin:.5rem 0 1rem"><div style="font-size:30px;font-weight:950;color:#f1df8d;margin-bottom:12px">Ти що москать?</div><img src="data:image/jpeg;base64,{b64}" style="width:min(760px,100%);border-radius:12px;display:block;margin:auto"></div>', unsafe_allow_html=True); time.sleep(3.5); st.session_state.language_popup = False; st.rerun()
    else: st.warning("Файл зображення для цього повідомлення не знайдено."); st.session_state.language_popup = False

st.markdown('<div class="eyebrow">ЗБРОЙНІ СИЛИ УКРАЇНИ · LOCAL COMMAND CENTER</div><div class="hero"><h1>Процес виконання розпоряджень</h1><p class="muted">Єдиний простір для контролю термінів, документів, відповідей та статистики виконання.</p></div>', unsafe_allow_html=True)
navigation()

if st.button("＋ ДОДАТИ РОЗПОРЯДЖЕННЯ", key="add_top"): st.session_state.add_open = not st.session_state.add_open; st.rerun()
add_form()

if st.session_state.just_added:
    st.markdown('<div class="successbox"><b>✓ РОЗПОРЯДЖЕННЯ ДОДАНО</b><br><span class="muted">Документ збережено у власній папці розпорядження.</span></div>', unsafe_allow_html=True); play_sound(); st.session_state.just_added = False

rows = orders(); states = [state(o) for o in rows]

if st.session_state.page == "Головна":
    overdue = states.count("overdue"); today = states.count("today"); done = states.count("done"); progress = states.count("progress")
    m = st.columns(5)
    for col,label,val,hint in [(m[0],"УСЬОГО",len(rows),"усі зареєстровані"),(m[1],"У РОБОТІ",progress,"активні"),(m[2],"СЬОГОДНІ",today,"контрольна дата"),(m[3],"ПРОСТРОЧЕНО",overdue,"потребують уваги"),(m[4],"ВИКОНАНО",done,"закриті")]:
        with col: metric(label,val,hint)
    st.markdown('<div class="section-title">🎯 ФОКУС ДНЯ</div>', unsafe_allow_html=True)
    critical = [(o,s) for o,s in zip(rows,states) if s in {"overdue","today"} or o["priority"] in {"Терміновий","Критичний"}]
    if critical:
        for o,s in critical[:6]:
            badge = "finished" if s == "done" else "late" if s == "overdue" else "todaybadge" if s == "today" else "work"
            st.markdown(f'<div class="focus"><b>№ {html.escape(o["number"])}</b> <span class="badge {badge}">{STATUSES[s]}</span><div class="desc">{html.escape(o["description"])}</div><span class="muted">До: {o["deadline"]} · {remaining(o["deadline"])} · Пріоритет: {html.escape(o["priority"])}</span></div>', unsafe_allow_html=True)
    else: st.success("На сьогодні критичних завдань немає.")
    st.markdown('<div class="section-title">📈 ДИНАМІКА ОТРИМАННЯ</div>', unsafe_allow_html=True)
    c = db(); monthly = c.execute("SELECT substr(received_date,1,7) ym,COUNT(*) n FROM orders GROUP BY ym ORDER BY ym DESC LIMIT 12").fetchall(); c.close(); maxv = max([r["n"] for r in monthly], default=1)
    for r in reversed(monthly): st.markdown(f'<div style="display:grid;grid-template-columns:90px 1fr 45px;gap:10px;align-items:center;margin:.4rem 0"><span class="muted">{r["ym"]}</span><div class="chartbar" style="width:{max(4,int(r["n"]*100/maxv))}%"></div><b>{r["n"]}</b></div>', unsafe_allow_html=True)

elif st.session_state.page == "Розпорядження":
    st.markdown('<div class="section-title">📋 РЕЄСТР РОЗПОРЯДЖЕНЬ</div>', unsafe_allow_html=True)
    a,b,c,d = st.columns([2,1,1,1])
    with a: query = st.text_input("Пошук", placeholder="Номер, вихідний №, опис, відповідальний, мітка...")
    with b: fs = st.selectbox("Статус", ["Усі"] + list(STATUSES.values()))
    with c: fp = st.selectbox("Пріоритет", ["Усі"] + PRIORITIES)
    with d: sort = st.selectbox("Сортування", ["Дедлайн", "Найновіші", "Найстаріші"])
    filtered=[]
    for o in rows:
        s=state(o); hay=f'{o["number"]} {o["completion_outgoing"]} {o["description"]} {o["responsible"]} {o["category"]} {o["tags"]}'.lower()
        if query and query.lower() not in hay: continue
        if fs != "Усі" and STATUSES[s] != fs: continue
        if fp != "Усі" and o["priority"] != fp: continue
        filtered.append((o,s))
    if sort == "Найновіші": filtered.sort(key=lambda x:x[0]["created_at"], reverse=True)
    elif sort == "Найстаріші": filtered.sort(key=lambda x:x[0]["created_at"])
    st.markdown(f'<span class="muted">ЗНАЙДЕНО: {len(filtered)}</span>', unsafe_allow_html=True)
    for o,s in filtered:
        badge="finished" if s=="done" else "late" if s=="overdue" else "todaybadge" if s=="today" else "work"
        st.markdown(f'<div class="order {s}"><div style="display:flex;justify-content:space-between;gap:10px"><div><b style="font-size:1.18rem">№ {html.escape(o["number"])}</b> <span class="badge {badge}">{STATUSES[s]}</span></div><b>{html.escape(o["priority"])}</b></div><div class="desc">{html.escape(o["description"])}</div><div class="muted">До: {o["deadline"]} · {remaining(o["deadline"])} · {html.escape(o["category"])} · {html.escape(o["responsible"] or "Відповідальний не вказаний")}</div>{''.join(f'<span class="tag">#{html.escape(t.strip())}</span>' for t in o["tags"].split(",") if t.strip())}</div>', unsafe_allow_html=True)
        a,b,c,d = st.columns(4)
        with a:
            if st.button("📄 ВІДКРИТИ", key=f"open_{o['id']}"): st.session_state.viewer_order=o["id"]; st.session_state.viewer_response=None; st.rerun()
        with b:
            if st.button("↩ ВІДПОВІДЬ", key=f"resp_{o['id']}"): st.session_state.response_order=o["id"]; st.rerun()
        with c:
            if st.button("✏ РЕДАГУВАТИ", key=f"edit_{o['id']}"): st.session_state.edit_order=o["id"]; st.rerun()
        with d:
            if st.button("🗑 ВИДАЛИТИ", key=f"del_{o['id']}"): st.session_state.delete_order=o["id"]; st.rerun()
        if st.session_state.delete_order == o["id"]:
            st.warning(f"Видалити № {o['number']} разом із файлом та всіма відповідями?")
            x,y=st.columns(2)
            with x:
                if st.button("ТАК, ВИДАЛИТИ", key=f"yes_{o['id']}"): delete_order(o["id"]); st.session_state.delete_order=None; st.rerun()
            with y:
                if st.button("СКАСУВАТИ", key=f"no_{o['id']}"): st.session_state.delete_order=None; st.rerun()
        if st.session_state.edit_order == o["id"]:
            with st.form(f"edit_{o['id']}"):
                a,b,c,d=st.columns(4)
                nn=a.text_input("№ розпорядження", value=o["number"], placeholder="Введіть номер")
                dd=b.date_input("Термін виконання", value=date.fromisoformat(o["deadline"]))
                pp=c.selectbox("Пріоритет", PRIORITIES, index=PRIORITIES.index(o["priority"]) if o["priority"] in PRIORITIES else 0)
                rr=d.text_input("Відповідальний", value=o["responsible"], placeholder="Підрозділ або прізвище")
                desc=st.text_area("Короткий опис розпорядження", value=o["description"], placeholder="Опишіть завдання...")
                a,b=st.columns(2); cc=a.selectbox("Категорія", CATEGORIES, index=CATEGORIES.index(o["category"]) if o["category"] in CATEGORIES else 0); tags= b.text_input("Мітки", value=o["tags"], placeholder="Наприклад: контроль, термінове")
                x,y=st.columns(2); ok=x.form_submit_button("💾 ЗБЕРЕГТИ ЗМІНИ"); no=y.form_submit_button("СКАСУВАТИ")
                if ok: update_order(o["id"],nn,dd,desc,pp,rr,cc,tags); st.session_state.edit_order=None; st.rerun()
                if no: st.session_state.edit_order=None; st.rerun()

if st.session_state.viewer_order:
    c=db(); row=c.execute("SELECT * FROM orders WHERE id=?",(st.session_state.viewer_order,)).fetchone(); c.close()
    if row:
        st.markdown("---"); st.markdown(f"## 📄 РОЗПОРЯДЖЕННЯ № {html.escape(row['number'])}")
        st.markdown(f'<div class="panel"><b>Короткий опис</b><p class="desc">{html.escape(row["description"])}</p><span class="muted">Термін: {row["deadline"]} · Статус: {STATUSES[state(row)]} · Пріоритет: {html.escape(row["priority"])}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📄 ОСНОВНИЙ ДОКУМЕНТ</div>', unsafe_allow_html=True); show_file(row)
        rs=responses(row["id"]); st.markdown('<div class="section-title">↩ ВІДПОВІДІ</div>', unsafe_allow_html=True)
        if not rs: st.info("Відповідей ще немає.")
        for r in rs:
            st.markdown(f'<div class="panel"><b>{html.escape(r["outgoing"] or "Без вихідного номера")}</b> · {r["response_date"]} · {"🟢 Виконано" if r["is_final"] else "У роботі"}<br>{html.escape(r["comment"] or "Без короткого змісту")}</div>', unsafe_allow_html=True)
            if st.button("👁 ПЕРЕГЛЯНУТИ ВІДПОВІДЬ", key=f"vr_{r['id']}"): st.session_state.viewer_response=r["id"]; st.rerun()
        st.markdown('<div class="section-title">🕒 ІСТОРІЯ ЗМІН</div>', unsafe_allow_html=True)
        for e in events(row["id"]): st.markdown(f'<div class="timeline-item"><b>{html.escape(e["event_type"])}</b><br><span class="muted">{e["created_at"][:19].replace("T"," ")}</span> · {html.escape(e["details"])}</div>', unsafe_allow_html=True)

if st.session_state.viewer_response:
    c=db(); rr=c.execute("SELECT * FROM responses WHERE id=?",(st.session_state.viewer_response,)).fetchone(); c.close()
    if rr:
        st.markdown('<div class="section-title">📎 ВІДПОВІДЬ</div>', unsafe_allow_html=True); show_file(rr)

if st.session_state.response_order:
    c=db(); row=c.execute("SELECT * FROM orders WHERE id=?",(st.session_state.response_order,)).fetchone(); c.close()
    if row:
        st.markdown("---"); st.markdown(f"## ↩ ВІДПОВІДЬ НА РОЗПОРЯДЖЕННЯ № {html.escape(row['number'])}")
        with st.form(f"response_{row['id']}"):
            a,b=st.columns(2)
            with a: rd=st.date_input("Дата відповіді",value=date.today()); outgoing=st.text_input("Вихідний номер",placeholder="Наприклад: 123/45-26")
            with b: final=st.checkbox("Вважати розпорядження виконаним"); upload=st.file_uploader("Файл відповіді або архів")
            comment=st.text_area("Короткий зміст відповіді",placeholder="Коротко зазначте, що виконано або що надано у відповіді...")
            x,y=st.columns(2); save=x.form_submit_button("💾 ЗБЕРЕГТИ ВІДПОВІДЬ"); cancel=y.form_submit_button("СКАСУВАТИ")
            if cancel: st.session_state.response_order=None; st.rerun()
            if save:
                if not upload: st.error("Додайте файл відповіді або архів.")
                else: add_response(row,rd,outgoing,comment,upload,final); st.session_state.response_order=None; st.rerun()

if st.session_state.page == "Аналітика":
    st.markdown('<div class="section-title">📊 АНАЛІТИКА ВИКОНАННЯ</div>', unsafe_allow_html=True)
    a,b,c=st.columns(3)
    with a: year=st.number_input("Рік", min_value=2000, max_value=2100, value=date.today().year, step=1)
    with b: month=st.selectbox("Місяць", ["Усі місяці"]+MONTHS)
    with c: mode=st.selectbox("Показати", ["Отримано / виконано / прострочено", "Тільки отримані", "Тільки виконані"])
    data=[]; conn=db()
    for i,mn in enumerate(MONTHS,1):
        y=str(int(year)); mm=f"{i:02d}"
        total=conn.execute("SELECT COUNT(*) n FROM orders WHERE substr(received_date,1,4)=? AND substr(received_date,6,2)=?",(y,mm)).fetchone()["n"]
        finished=conn.execute("SELECT COUNT(*) n FROM orders WHERE status='done' AND substr(received_date,1,4)=? AND substr(received_date,6,2)=?",(y,mm)).fetchone()["n"]
        late=conn.execute("SELECT COUNT(*) n FROM orders WHERE status!='done' AND deadline < date('now') AND substr(received_date,1,4)=? AND substr(received_date,6,2)=?",(y,mm)).fetchone()["n"]
        data.append((mn,total,finished,late))
    conn.close()
    if month != "Усі місяці": data=[x for x in data if x[0]==month]
    maxv=max([max(x[1],x[2],x[3]) for x in data],default=1)
    for mn,total,finished,late in data:
        st.markdown(f"**{mn} {int(year)}**")
        vals=[("Отримано",total),("Виконано",finished),("Прострочено",late)] if mode.startswith("Отримано") else [("Отримано",total)] if mode.startswith("Тільки отримані") else [("Виконано",finished)]
        for label,val in vals: st.markdown(f'<div style="display:grid;grid-template-columns:120px 1fr 45px;gap:10px;align-items:center;margin:.35rem 0"><span class="muted">{label}</span><div class="chartbar" style="width:{max(3,int(val*100/maxv))}%"></div><b>{val}</b></div>',unsafe_allow_html=True)
    conn=db(); yr=conn.execute("SELECT COUNT(*) total,SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) done FROM orders WHERE substr(received_date,1,4)=?",(str(int(year)),)).fetchone(); conn.close(); total=int(yr["total"] or 0); finished=int(yr["done"] or 0); rate=finished/total*100 if total else 0
    a,b,c=st.columns(3)
    with a: metric("ОТРИМАНО",total,str(year))
    with b: metric("ВИКОНАНО",finished,str(year))
    with c: metric("ЧАСТКА ВИКОНАНИХ",f"{rate:.0f}%",f"за {year} рік")

if st.session_state.page == "Календар":
    st.markdown('<div class="section-title">🗓 КАЛЕНДАР ДЕДЛАЙНІВ</div>', unsafe_allow_html=True)
    a,b=st.columns(2)
    with a: cy=st.number_input("Рік календаря",min_value=2000,max_value=2100,value=st.session_state.calendar_year,step=1)
    with b: cm=st.selectbox("Місяць календаря",MONTHS,index=st.session_state.calendar_month-1)
    st.session_state.calendar_year=int(cy); st.session_state.calendar_month=MONTHS.index(cm)+1
    first=date(st.session_state.calendar_year,st.session_state.calendar_month,1); days=monthrange(first.year,first.month)[1]
    start=(first.weekday())
    cells=[None]*start+list(range(1,days+1)); cells += [None]*((7-len(cells)%7)%7)
    c=db(); calrows=c.execute("SELECT deadline,status,number FROM orders WHERE substr(deadline,1,7)=?",(f"{first.year:04d}-{first.month:02d}",)).fetchall(); c.close()
    byday={}
    for r in calrows: byday.setdefault(int(r["deadline"][-2:]),[]).append(r)
    headers=["Пн","Вт","Ср","Чт","Пт","Сб","Нд"]
    h=st.columns(7)
    for col,text in zip(h,headers):
        with col: st.markdown(f'<div class="muted" style="text-align:center;font-weight:900">{text}</div>',unsafe_allow_html=True)
    for i in range(0,len(cells),7):
        cols=st.columns(7)
        for col,day in zip(cols,cells[i:i+7]):
            with col:
                if not day: st.markdown('<div style="min-height:92px"></div>',unsafe_allow_html=True); continue
                items=byday.get(day,[]); late=sum(1 for x in items if x["status"]!="done" and day < date.today().day and first.year==date.today().year and first.month==date.today().month); done=sum(1 for x in items if x["status"]=="done")
                cls="calendar-red" if late else "calendar-green" if done==len(items) and items else ""
                st.markdown(f'<div class="calendar-card"><div class="calendar-day">{day}</div><div class="calendar-count {cls}">{len(items) if items else "·"}</div><div class="muted">{("простр. " + str(late)) if late else ("виконано" if done and done==len(items) else "")}</div></div>',unsafe_allow_html=True)

if st.session_state.page == "Налаштування":
    st.markdown('<div class="section-title">⚙️ НАЛАШТУВАННЯ ТА БЕЗПЕКА</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><b>📁 Локальне сховище</b><br><span class="muted">Поточна папка даних</span></div>',unsafe_allow_html=True); st.code(str(WORK),language="text")
    if st.button("💾 СТВОРИТИ РЕЗЕРВНУ КОПІЮ"): st.success(f"Резервну копію створено: {backup().name}")
    st.markdown('<div class="section-title">🛡 СТАН СИСТЕМИ</div>',unsafe_allow_html=True)
    checks=[("База даних",DB.exists()),("Папка розпоряджень",ORDERS.exists()),("Папка резервних копій",BACKUPS.exists()),("Звуковий файл",(APP/"sounds"/"opiat-rabota.mp3").exists()),("Зображення мови",(APP/"language-russian.jpg").exists())]
    for name,ok in checks: st.markdown(f'<div class="panel" style="margin:.35rem 0">{"🟢" if ok else "🔴"} <b>{name}</b><span class="muted"> — {"доступно" if ok else "не знайдено"}</span></div>',unsafe_allow_html=True)
    st.info("Поточний застосунок використовує локальні файли та SQLite. Для фінального .exe окремо буде зафіксовано локальний режим без зовнішніх мережевих залежностей.")

if st.session_state.page == "Головна" and st.session_state.calendar_selected:
    pass

st.markdown('<div style="margin-top:2.5rem;text-align:center" class="muted">LOCAL COMMAND CENTER · Усі документи та база зберігаються локально</div>',unsafe_allow_html=True)
