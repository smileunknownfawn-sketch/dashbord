import base64
import html
import mimetypes
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Процес виконання розпоряджень", page_icon="🇺🇦", layout="wide", initial_sidebar_state="collapsed")
APP = Path(__file__).resolve().parent
DEFAULT_WORKSPACE = APP / "data"

DEFAULTS = {
    "workspace": str(DEFAULT_WORKSPACE), "add_open": False, "response_order": None,
    "language": "Українська", "language_popup": False, "viewer_order": None,
    "viewer_response": None, "delete_order": None, "edit_order": None,
    "page": "Головна", "period_year": date.today().year, "period_month": "Усі місяці",
    "just_added": False,
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

WORK = Path(st.session_state.workspace).resolve()
ORDERS = WORK / "Розпорядження"
BACKUPS = WORK / "Резервні копії"
WORK.mkdir(parents=True, exist_ok=True)
ORDERS.mkdir(parents=True, exist_ok=True)
BACKUPS.mkdir(parents=True, exist_ok=True)
DB = WORK / "database.db"

CSS = """
<style>
@import url('data:text/css,');
html,body,[class*=css]{font-family:"Segoe UI",Arial,sans-serif}
.stApp{background:
radial-gradient(circle at 85% 5%,rgba(96,125,72,.28),transparent 25%),
radial-gradient(circle at 10% 90%,rgba(28,73,55,.22),transparent 30%),
linear-gradient(135deg,#030806 0%,#0b1711 48%,#050907 100%);color:#edf4ed}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.13;background-image:linear-gradient(rgba(180,205,180,.18) 1px,transparent 1px),linear-gradient(90deg,rgba(180,205,180,.18) 1px,transparent 1px);background-size:52px 52px;mask-image:linear-gradient(to bottom,black,transparent 90%)}
.block-container{max-width:1500px;padding:1.2rem 2.7rem 4rem}
.hero{padding:1rem 0 1.2rem}.hero h1{font-size:clamp(2rem,4vw,3.7rem);font-weight:850;letter-spacing:-.045em;margin:.15rem 0 .25rem;font-style:normal}.eyebrow{color:#bdcfac;font-weight:850;font-size:.66rem;letter-spacing:.22em}.version{text-align:right;color:#91a092;font-size:.68rem;letter-spacing:.13em;font-weight:850;padding-top:.3rem}
.panel,.metric,.order,.timeline{background:rgba(7,16,11,.91);border:1px solid rgba(214,232,212,.10);border-radius:18px;padding:1rem;box-shadow:0 15px 40px rgba(0,0,0,.18)}
.metric{min-height:100px}.metric .num{font-size:2rem;font-weight:900}.metric .label{color:#9dac9e;font-size:.67rem;font-weight:800;letter-spacing:.1em}.order{margin:.7rem 0;border-left:5px solid #c8a85c;transition:.15s}.order:hover{border-color:#e2c976;transform:translateY(-1px)}.order.overdue{border-left-color:#e36e68}.order.today{border-left-color:#e1c35f}.order.done{border-left-color:#6db987}.desc{color:#c4cec5;line-height:1.55;margin:.45rem 0}.muted{color:#87958b;font-size:.72rem;letter-spacing:.055em}.badge{display:inline-block;padding:.3rem .62rem;border-radius:999px;font-size:.61rem;font-weight:900;letter-spacing:.04em}.work{color:#d5b663;background:#d5b66318}.late{color:#ef7770;background:#ef777018}.finished{color:#79c393;background:#79c39318}.todaybadge{color:#e5c968;background:#e5c96818}.priority{color:#d7c48a}.stButton>button{border-radius:10px;background:rgba(120,146,95,.12);border:1px solid rgba(169,188,145,.26);color:#e0e9de;font-weight:850;min-height:42px}.stButton>button:hover{border-color:rgba(218,194,111,.75);background:rgba(208,174,98,.13)}.stTabs [data-baseweb="tab-list"]{gap:8px;background:rgba(0,0,0,.14);padding:.4rem;border-radius:13px}.stTabs [data-baseweb="tab"]{height:42px;border-radius:9px}.stTextInput input,.stTextArea textarea,.stDateInput input,.stNumberInput input{background:rgba(0,0,0,.38)!important;color:#fff!important}.stSelectbox div[data-baseweb="select"]>div{background:rgba(0,0,0,.38)}.section-title{font-size:1rem;font-weight:900;letter-spacing:.08em;margin:.5rem 0}.danger{border-color:#d7656040;background:#d7656010}.successbox{padding:16px;border:1px solid #84b88e55;border-radius:14px;background:#1b3925;margin:.5rem 0 1rem}.chartbar{height:14px;border-radius:8px;background:linear-gradient(90deg,#6d8e61,#c9aa5f);box-shadow:0 0 16px #6d8e6130}.kpi{font-size:.72rem;color:#aeb9b0}.timeline-item{padding:.7rem 0;border-left:2px solid #6d8e61;padding-left:1rem;margin-left:.4rem}.small{font-size:.7rem}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT NOT NULL, deadline TEXT NOT NULL,
        description TEXT NOT NULL, folder TEXT NOT NULL, filename TEXT NOT NULL, path TEXT NOT NULL,
        mime TEXT NOT NULL, status TEXT DEFAULT 'progress', completion_outgoing TEXT DEFAULT '',
        priority TEXT DEFAULT 'Звичайний', responsible TEXT DEFAULT '', category TEXT DEFAULT 'Інше',
        received_date TEXT DEFAULT '', created_at TEXT NOT NULL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS responses(
        id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER NOT NULL, response_date TEXT NOT NULL,
        outgoing TEXT DEFAULT '', comment TEXT DEFAULT '', filename TEXT NOT NULL, path TEXT NOT NULL,
        mime TEXT NOT NULL, is_final INTEGER DEFAULT 0, created_at TEXT NOT NULL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, event_type TEXT NOT NULL,
        details TEXT DEFAULT '', created_at TEXT NOT NULL)""")
    c.commit()
    return c


def safe_name(value):
    return "".join(ch if ch.isalnum() or ch in " ._-()[]" else "_" for ch in str(value).strip()) or "Документ"


def save_upload(upload, folder):
    folder.mkdir(parents=True, exist_ok=True)
    p = folder / safe_name(upload.name)
    counter = 2
    while p.exists():
        p = folder / f"{p.stem}_{counter}{p.suffix}"
        counter += 1
    p.write_bytes(upload.getvalue())
    return p


def event(order_id, kind, details=""):
    c = db(); c.execute("INSERT INTO events(order_id,event_type,details,created_at) VALUES(?,?,?,?)", (order_id, kind, details, datetime.now().isoformat())); c.commit(); c.close()


def order_state(row):
    if row["status"] == "done": return "done"
    try:
        d = date.fromisoformat(row["deadline"])
        if d < date.today(): return "overdue"
        if d == date.today(): return "today"
    except Exception:
        pass
    return "progress"


def days_text(deadline):
    try:
        delta = (date.fromisoformat(deadline) - date.today()).days
        if delta < 0: return f"ПРОСТРОЧЕНО НА {abs(delta)} ДНІВ"
        if delta == 0: return "ТЕРМІН СЬОГОДНІ"
        if delta == 1: return "ЗАЛИШИВСЯ 1 ДЕНЬ"
        return f"ЗАЛИШИЛОСЯ {delta} ДНІВ"
    except Exception:
        return ""


def add_order(number, deadline, description, upload, received, priority, responsible, category):
    folder = ORDERS / safe_name(number)
    counter = 2
    while folder.exists():
        folder = ORDERS / f"{safe_name(number)}_{counter}"; counter += 1
    p = save_upload(upload, folder)
    c = db()
    cur = c.execute("""INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,priority,responsible,category,received_date,created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (number.strip(), deadline.isoformat(), description.strip(), folder.name, p.name,
        str(p.relative_to(WORK)), upload.type or mimetypes.guess_type(p.name)[0] or "application/octet-stream", "progress",
        priority, responsible.strip(), category, received.isoformat(), datetime.now().isoformat()))
    oid = cur.lastrowid; c.commit(); c.close(); event(oid, "Створено", f"№ {number.strip()}")


def update_order(oid, number, deadline, description, priority, responsible, category):
    c = db(); c.execute("UPDATE orders SET number=?,deadline=?,description=?,priority=?,responsible=?,category=? WHERE id=?", (number.strip(),deadline.isoformat(),description.strip(),priority,responsible.strip(),category,oid)); c.commit(); c.close(); event(oid,"Змінено","Оновлено дані розпорядження")


def add_response(row, response_date, outgoing, comment, upload, final):
    folder = ORDERS / row["folder"] / "Відповіді"; p = save_upload(upload, folder)
    c = db(); c.execute("""INSERT INTO responses(order_id,response_date,outgoing,comment,filename,path,mime,is_final,created_at)
        VALUES(?,?,?,?,?,?,?,?,?)""", (row["id"],response_date.isoformat(),outgoing.strip(),comment.strip(),p.name,str(p.relative_to(WORK)),upload.type or mimetypes.guess_type(p.name)[0] or "application/octet-stream",int(final),datetime.now().isoformat()))
    if final: c.execute("UPDATE orders SET status='done',completion_outgoing=? WHERE id=?",(outgoing.strip(),row["id"]))
    c.commit(); c.close(); event(row["id"],"Додано відповідь",outgoing.strip() or "Без вихідного номера")
    if final: event(row["id"],"Виконано",outgoing.strip())


def get_responses(order_id):
    c=db(); rows=c.execute("SELECT * FROM responses WHERE order_id=? ORDER BY response_date DESC,id DESC",(order_id,)).fetchall(); c.close(); return rows


def get_events(order_id):
    c=db(); rows=c.execute("SELECT * FROM events WHERE order_id=? ORDER BY created_at ASC",(order_id,)).fetchall(); c.close(); return rows


def delete_order(order_id):
    c=db(); row=c.execute("SELECT folder FROM orders WHERE id=?",(order_id,)).fetchone()
    if not row: c.close(); return False
    folder=(ORDERS/row["folder"]).resolve()
    try: folder.relative_to(ORDERS.resolve())
    except ValueError: c.close(); raise RuntimeError("Небезпечний шлях папки")
    c.execute("DELETE FROM responses WHERE order_id=?",(order_id,)); c.execute("DELETE FROM events WHERE order_id=?",(order_id,)); c.execute("DELETE FROM orders WHERE id=?",(order_id,)); c.commit(); c.close()
    if folder.exists(): shutil.rmtree(folder)
    return True


def make_backup():
    target=BACKUPS/f"Резервна_копія_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"; target.mkdir(parents=True,exist_ok=True)
    if DB.exists(): shutil.copy2(DB,target/"database.db")
    if ORDERS.exists(): shutil.copytree(ORDERS,target/"Розпорядження",dirs_exist_ok=True)
    return target


def local_path(rel):
    p=(WORK/rel).resolve()
    try: p.relative_to(WORK.resolve())
    except ValueError: return None
    return p if p.exists() else None


def show_file_viewer(row, response=False):
    p=local_path(row["path"])
    if not p: st.error("Файл не знайдено у папці даних."); return
    mime=row["mime"] or mimetypes.guess_type(p.name)[0] or "application/octet-stream"; data=p.read_bytes()
    st.markdown(f"**{html.escape(p.name)}** · `{mime}`")
    st.download_button("⬇ ЗАВАНТАЖИТИ ФАЙЛ",data=data,file_name=p.name,mime=mime,key=f"download_{'r' if response else 'o'}_{row['id']}")
    if mime=="application/pdf" or p.suffix.lower()==".pdf":
        b64=base64.b64encode(data).decode(); st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="760" style="border:1px solid #ffffff18;border-radius:12px"></iframe>',unsafe_allow_html=True)
    elif mime.startswith("image/"): st.image(data,use_container_width=True)
    elif mime.startswith("text/") or p.suffix.lower() in {".txt",".csv",".log",".md"}: st.code(data.decode("utf-8",errors="replace"),language="text")
    else: st.info("Для цього формату доступне завантаження файлу. У локальному .exe файл можна буде відкрити програмою ОС.")


def play_add_sound():
    audio_file=APP/"sounds"/"opiat-rabota.mp3"
    if not audio_file.exists(): return
    b64=base64.b64encode(audio_file.read_bytes()).decode()
    st.markdown(f'<audio autoplay><source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg"></audio>',unsafe_allow_html=True)


def load_orders():
    c=db(); rows=c.execute("SELECT * FROM orders ORDER BY deadline ASC,id DESC").fetchall(); c.close(); return rows


def status_label(state):
    return {"done":"ВИКОНАНО","overdue":"ПРОСТРОЧЕНО","today":"ТЕРМІН СЬОГОДНІ","progress":"У РОБОТІ"}[state]


def metric(label, value, hint=""):
    st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="num">{value}</div><div class="kpi">{html.escape(hint)}</div></div>',unsafe_allow_html=True)


# Demo data is created only for an empty database.
c=db()
if c.execute("SELECT COUNT(*) FROM orders").fetchone()[0]==0:
    folder=ORDERS/"01-2026"; folder.mkdir(exist_ok=True); p=folder/"Розпорядження_01-2026.txt"
    p.write_text("ДЕМОНСТРАЦІЙНЕ РОЗПОРЯДЖЕННЯ\n\nПідготувати та надати узагальнену інформацію про стан виконання визначених завдань.",encoding="utf-8")
    cur=c.execute("""INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,priority,responsible,category,received_date,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",("01/2026","2026-10-05","Підготувати та надати узагальнену інформацію про стан виконання визначених завдань.",folder.name,p.name,str(p.relative_to(WORK)),"text/plain","progress","Звичайний","","Організаційне","2026-09-25",datetime.now().isoformat()))
    c.commit(); oid=cur.lastrowid; c.execute("INSERT INTO events(order_id,event_type,details,created_at) VALUES(?,?,?,?)",(oid,"Створено","Демонстраційний запис",datetime.now().isoformat())); c.commit()
c.close()

# Header and language
l,r=st.columns([5,1])
with l:
    lang=st.selectbox("Мова інтерфейсу",["Українська","Російська"],index=0 if st.session_state.language=="Українська" else 1,label_visibility="collapsed")
    if lang!=st.session_state.language:
        st.session_state.language=lang; st.session_state.language_popup=(lang=="Російська"); st.rerun()
    st.markdown(f'<div class="muted">Мова інтерфейсу — <b>{html.escape(lang)}</b></div>',unsafe_allow_html=True)
with r: st.markdown('<div class="version">ВЕРСІЯ 2.0</div>',unsafe_allow_html=True)

if st.session_state.language_popup and st.session_state.language=="Російська":
    img=APP/"language-russian.jpg"
    if img.exists():
        b64=base64.b64encode(img.read_bytes()).decode(); st.markdown(f'<div style="text-align:center;background:#050807;border:1px solid #d0ae6266;border-radius:18px;padding:16px;margin:.5rem 0 1rem"><div style="font-size:30px;font-weight:900;color:#f1df8d;margin-bottom:12px">Ти що москать?</div><img src="data:image/jpeg;base64,{b64}" style="width:min(760px,100%);border-radius:12px;display:block;margin:auto"></div>',unsafe_allow_html=True); time.sleep(3.5); st.session_state.language_popup=False; st.rerun()
    else: st.warning("Файл language-russian.jpg не знайдено."); st.session_state.language_popup=False

st.markdown('<div class="eyebrow">ЗБРОЙНІ СИЛИ УКРАЇНИ · LOCAL CONTROL CENTER</div><div class="hero"><h1>Процес виконання розпоряджень</h1><p class="muted">Єдиний простір для контролю термінів, документів, відповідей та статистики виконання.</p></div>',unsafe_allow_html=True)

orders=load_orders()
states=[order_state(o) for o in orders]

# Navigation
p1,p2,p3,p4=st.columns([1,1,1,1])
for col,label,key in [(p1,"🏠 ГОЛОВНА","Головна"),(p2,"📋 РОЗПОРЯДЖЕННЯ","Розпорядження"),(p3,"📊 АНАЛІТИКА","Аналітика"),(p4,"⚙️ НАЛАШТУВАННЯ","Налаштування")]:
    with col:
        if st.button(label,key=f"nav_{key}"): st.session_state.page=key; st.rerun()

# Global action
if st.button("＋ ДОДАТИ РОЗПОРЯДЖЕННЯ",key="add_top"):
    st.session_state.add_open=not st.session_state.add_open; st.rerun()

if st.session_state.add_open:
    with st.form("new_order"):
        st.markdown("### НОВЕ РОЗПОРЯДЖЕННЯ")
        a,b,c1=st.columns(3)
        with a: n=st.text_input("№ розпорядження")
        with b: received=st.date_input("Дата отримання",value=date.today())
        with c1: deadline=st.date_input("Виконати до",value=date.today())
        a,b,c1=st.columns(3)
        with a: priority=st.selectbox("Пріоритет",["Звичайний","Важливий","Терміновий","Критичний"])
        with b: category=st.selectbox("Категорія",["Організаційне","Особовий склад","Матеріальне","Навчання","Інше"])
        with c1: responsible=st.text_input("Відповідальний")
        desc=st.text_area("Короткий опис розпорядження",height=110)
        f=st.file_uploader("📎 Файл розпорядження")
        x,y=st.columns(2)
        with x: save=st.form_submit_button("ЗБЕРЕГТИ")
        with y: cancel=st.form_submit_button("СКАСУВАТИ")
        if cancel: st.session_state.add_open=False; st.rerun()
        if save:
            if not n or not desc or not f: st.error("Заповніть №, короткий опис та додайте файл.")
            else: add_order(n,deadline,desc,f,received,priority,responsible,category); st.session_state.add_open=False; st.session_state.just_added=True; st.rerun()

if st.session_state.just_added:
    st.markdown('<div class="successbox"><b>✓ РОЗПОРЯДЖЕННЯ ДОДАНО</b><br><span class="muted">Файл збережено у власній папці розпорядження.</span></div>',unsafe_allow_html=True)
    play_add_sound(); st.session_state.just_added=False

# MAIN
if st.session_state.page=="Головна":
    overdue=sum(s=="overdue" for s in states); today=sum(s=="today" for s in states); done=sum(s=="done" for s in states); progress=sum(s=="progress" for s in states)
    m=st.columns(5)
    with m[0]: metric("УСЬОГО",len(orders),"усі зареєстровані")
    with m[1]: metric("У РОБОТІ",progress,"активні")
    with m[2]: metric("СЬОГОДНІ",today,"контрольна дата")
    with m[3]: metric("ПРОСТРОЧЕНО",overdue,"потребують уваги")
    with m[4]: metric("ВИКОНАНО",done,"закриті")
    st.markdown("### 🔴 КОНТРОЛЬНА ПАНЕЛЬ")
    critical=[(o,s) for o,s in zip(orders,states) if s in {"overdue","today"}]
    if not critical: st.success("Критичних дедлайнів зараз немає.")
    for o,s in critical[:8]:
        st.markdown(f'<div class="order {s}"><b>№ {html.escape(o["number"])}</b> · <span class="badge {"late" if s=="overdue" else "todaybadge"}">{status_label(s)}</span><br><span class="desc">{html.escape(o["description"])}</span><br><span class="muted">До: {o["deadline"]} · {days_text(o["deadline"])}</span></div>',unsafe_allow_html=True)
    st.markdown("### 📈 ШВИДКА ДИНАМІКА")
    c=db(); rows=c.execute("SELECT substr(received_date,1,7) ym, COUNT(*) n FROM orders GROUP BY ym ORDER BY ym DESC LIMIT 12").fetchall(); c.close()
    maxv=max([r["n"] for r in rows],default=1)
    for row in reversed(rows):
        st.markdown(f'<div style="display:grid;grid-template-columns:90px 1fr 40px;gap:10px;align-items:center;margin:.35rem 0"><span class="muted">{row["ym"]}</span><div class="chartbar" style="width:{max(4,int(row["n"]*100/maxv))}%"></div><b>{row["n"]}</b></div>',unsafe_allow_html=True)

# ORDERS
elif st.session_state.page=="Розпорядження":
    st.markdown("### 📋 РОЗПОРЯДЖЕННЯ")
    a,b,c1,d=st.columns([2,1,1,1])
    with a: query=st.text_input("Пошук",placeholder="№, вихідний №, опис, відповідальний...")
    with b: filter_status=st.selectbox("Статус",["Усі","У роботі","Термін сьогодні","Прострочено","Виконано"])
    with c1: filter_priority=st.selectbox("Пріоритет",["Усі","Звичайний","Важливий","Терміновий","Критичний"])
    with d: sort_mode=st.selectbox("Сортування",["Дедлайн","Новіші","Старіші"])
    filtered=[]
    for o in orders:
        s=order_state(o); sl=status_label(s)
        hay=f'{o["number"]} {o["completion_outgoing"]} {o["description"]} {o["responsible"]} {o["category"]}'.lower()
        if query and query.lower() not in hay: continue
        if filter_status!="Усі" and sl!=filter_status: continue
        if filter_priority!="Усі" and o["priority"]!=filter_priority: continue
        filtered.append((o,s))
    if sort_mode=="Новіші": filtered.sort(key=lambda x:x[0]["created_at"],reverse=True)
    elif sort_mode=="Старіші": filtered.sort(key=lambda x:x[0]["created_at"])
    else: filtered.sort(key=lambda x:x[0]["deadline"])
    st.markdown(f'<div class="muted">ЗНАЙДЕНО: {len(filtered)} · СЬОГОДНІ: {date.today().isoformat()}</div>',unsafe_allow_html=True)
    for o,s in filtered:
        st.markdown(f'<div class="order {s}"><div style="display:flex;justify-content:space-between;gap:12px"><div><b style="font-size:1.15rem">№ {html.escape(o["number"])}</b> <span class="badge {"finished" if s=="done" else "late" if s=="overdue" else "todaybadge" if s=="today" else "work"}">{status_label(s)}</span></div><span class="priority">{html.escape(o["priority"])}</span></div><div class="desc">{html.escape(o["description"])}</div><div class="muted">До: {o["deadline"]} · {days_text(o["deadline"])} · {html.escape(o["category"])} · {html.escape(o["responsible"] or "Відповідальний не вказаний")}</div></div>',unsafe_allow_html=True)
        a,b,c1,e=st.columns(4)
        with a:
            if st.button("📄 ВІДКРИТИ",key=f"open_{o['id']}"): st.session_state.viewer_order=o["id"]; st.session_state.viewer_response=None; st.rerun()
        with b:
            if st.button("↩ ВІДПОВІДЬ",key=f"resp_{o['id']}"): st.session_state.response_order=o["id"]; st.rerun()
        with c1:
            if st.button("✏ РЕДАГУВАТИ",key=f"edit_{o['id']}"): st.session_state.edit_order=o["id"]; st.rerun()
        with e:
            if st.button("🗑 ВИДАЛИТИ",key=f"del_{o['id']}"): st.session_state.delete_order=o["id"]; st.rerun()
        if st.session_state.delete_order==o["id"]:
            st.warning(f"Видалити № {o['number']} разом із файлом та всіма відповідями?")
            x,y=st.columns(2)
            with x:
                if st.button("ТАК, ВИДАЛИТИ",key=f"yes_{o['id']}"): delete_order(o["id"]); st.session_state.delete_order=None; st.rerun()
            with y:
                if st.button("СКАСУВАТИ",key=f"no_{o['id']}"): st.session_state.delete_order=None; st.rerun()
        if st.session_state.edit_order==o["id"]:
            with st.form(f"editform_{o['id']}"):
                a,b,c1=st.columns(3); nn=a.text_input("№",value=o["number"]); dd=b.date_input("Термін",value=date.fromisoformat(o["deadline"])); pp=c1.selectbox("Пріоритет",["Звичайний","Важливий","Терміновий","Критичний"],index=["Звичайний","Важливий","Терміновий","Критичний"].index(o["priority"]))
                desc=st.text_area("Короткий опис",value=o["description"]); rr=st.text_input("Відповідальний",value=o["responsible"]); cc=st.selectbox("Категорія",["Організаційне","Особовий склад","Матеріальне","Навчання","Інше"],index=["Організаційне","Особовий склад","Матеріальне","Навчання","Інше"].index(o["category"]))
                x,y=st.columns(2); ok=x.form_submit_button("ЗБЕРЕГТИ"); no=y.form_submit_button("СКАСУВАТИ")
                if ok: update_order(o["id"],nn,dd,desc,pp,rr,cc); st.session_state.edit_order=None; st.rerun()
                if no: st.session_state.edit_order=None; st.rerun()

# VIEWER
if st.session_state.viewer_order:
    c=db(); row=c.execute("SELECT * FROM orders WHERE id=?",(st.session_state.viewer_order,)).fetchone(); c.close()
    if row:
        st.markdown("---"); st.markdown(f"## 📄 РОЗПОРЯДЖЕННЯ № {html.escape(row['number'])}")
        st.markdown(f'<div class="panel"><b>Короткий опис</b><p class="desc">{html.escape(row["description"])}</p><span class="muted">Термін: {row["deadline"]} · Статус: {status_label(order_state(row))}</span></div>',unsafe_allow_html=True)
        show_file_viewer(row)
        responses=get_responses(row["id"])
        st.markdown("### ↩ ВІДПОВІДІ")
        if not responses: st.info("Відповідей ще немає.")
        for r in responses:
            st.markdown(f'<div class="panel"><b>{html.escape(r["outgoing"] or "Без вихідного номера")}</b> · {r["response_date"]} · {"🟢 Виконано" if r["is_final"] else "У роботі"}<br>{html.escape(r["comment"] or "Без коментаря")}</div>',unsafe_allow_html=True)
            if st.button("👁 Переглянути відповідь",key=f"vr_{r['id']}"): st.session_state.viewer_response=r["id"]; st.rerun()
        if st.session_state.viewer_response:
            rr=next((x for x in responses if x["id"]==st.session_state.viewer_response),None)
            if rr: show_file_viewer(rr,True)
        st.markdown("### 🕒 ІСТОРІЯ")
        for ev in get_events(row["id"]): st.markdown(f'<div class="timeline-item"><b>{html.escape(ev["event_type"])}</b><br><span class="muted">{ev["created_at"][:19].replace("T"," ")}</span> · {html.escape(ev["details"])}</div>',unsafe_allow_html=True)

# RESPONSE FORM
if st.session_state.response_order:
    c=db(); row=c.execute("SELECT * FROM orders WHERE id=?",(st.session_state.response_order,)).fetchone(); c.close()
    if row:
        st.markdown("---"); st.markdown(f"## ↩ ВІДПОВІДЬ НА РОЗПОРЯДЖЕННЯ № {html.escape(row['number'])}")
        with st.form(f"response_{row['id']}"):
            a,b=st.columns(2)
            with a: rd=st.date_input("Дата відповіді",value=date.today()); outgoing=st.text_input("Вихідний номер")
            with b: final=st.checkbox("Вважати розпорядження виконаним"); upload=st.file_uploader("Файл відповіді / архів")
            comment=st.text_area("Короткий зміст відповіді")
            x,y=st.columns(2); save=x.form_submit_button("ЗБЕРЕГТИ ВІДПОВІДЬ"); cancel=y.form_submit_button("СКАСУВАТИ")
            if cancel: st.session_state.response_order=None; st.rerun()
            if save:
                if not upload: st.error("Додайте файл відповіді або архів.")
                else: add_response(row,rd,outgoing,comment,upload,final); st.session_state.response_order=None; st.rerun()

# ANALYTICS
if st.session_state.page=="Аналітика":
    st.markdown("## 📊 АНАЛІТИКА ВИКОНАННЯ")
    a,b,c1=st.columns(3)
    with a: year=st.number_input("Рік",min_value=2000,max_value=2100,value=int(st.session_state.period_year),step=1)
    with b: month=st.selectbox("Місяць",["Усі місяці","Січень","Лютий","Березень","Квітень","Травень","Червень","Липень","Серпень","Вересень","Жовтень","Листопад","Грудень"])
    with c1: mode=st.selectbox("Порівняння",["Отримано / виконано / прострочено","Тільки отримані","Тільки виконані"])
    months=["Січень","Лютий","Березень","Квітень","Травень","Червень","Липень","Серпень","Вересень","Жовтень","Листопад","Грудень"]
    c=db(); data=[]
    for i,mn in enumerate(months,1):
        total=c.execute("SELECT COUNT(*) FROM orders WHERE substr(received_date,1,4)=? AND substr(received_date,6,2)=?",(str(int(year)),f"{i:02d}")).fetchone()[0]
        finished=c.execute("SELECT COUNT(*) FROM orders WHERE status='done' AND substr(received_date,1,4)=? AND substr(received_date,6,2)=?",(str(int(year)),f"{i:02d}")).fetchone()[0]
        late=c.execute("SELECT COUNT(*) FROM orders WHERE substr(received_date,1,4)=? AND substr(received_date,6,2)=? AND deadline < date('now') AND status!='done'",(str(int(year)),f"{i:02d}")).fetchone()[0]
        data.append((mn,total,finished,late))
    c.close()
    if month!="Усі місяці": data=[x for x in data if x[0]==month]
    maxv=max([max(x[1],x[2],x[3]) for x in data],default=1)
    for mn,total,finished,late in data:
        st.markdown(f"### {mn} {int(year)}")
        if mode=="Тільки отримані": vals=[("Отримано",total,"#7f9b68")]
        elif mode=="Тільки виконані": vals=[("Виконано",finished,"#79b88a")]
        else: vals=[("Отримано",total,"#7f9b68"),("Виконано",finished,"#79b88a"),("Прострочено",late,"#e36e68")]
        for label,val,_ in vals:
            width=max(3,int(val*100/maxv))
            st.markdown(f'<div style="display:grid;grid-template-columns:120px 1fr 45px;gap:10px;align-items:center;margin:.35rem 0"><span class="muted">{label}</span><div style="height:15px;width:{width}%;border-radius:8px;background:linear-gradient(90deg,#607c58,#c7a85c)"></div><b>{val}</b></div>',unsafe_allow_html=True)
    c=db(); yearly=c.execute("SELECT COUNT(*) total,SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) done FROM orders WHERE substr(received_date,1,4)=?",(str(int(year)),)).fetchone(); c.close()
    total=int(yearly["total"] or 0); finished=int(yearly["done"] or 0); rate=(finished/total*100) if total else 0
    st.markdown("### 🎯 ПІДСУМОК РОКУ")
    a,b,c1=st.columns(3)
    with a: metric("ОТРИМАНО",total,str(year))
    with b: metric("ВИКОНАНО",finished,str(year))
    with c1: metric("ЧАСТКА ВИКОНАНИХ",f"{rate:.0f}%","від отриманих за рік")

# SETTINGS
if st.session_state.page=="Налаштування":
    st.markdown("## ⚙️ НАЛАШТУВАННЯ")
    st.markdown('<div class="panel"><b>📁 Локальне сховище</b><br><span class="muted">Поточна папка даних</span></div>',unsafe_allow_html=True)
    st.code(str(WORK),language="text")
    if st.button("💾 СТВОРИТИ РЕЗЕРВНУ КОПІЮ"): path=make_backup(); st.success(f"Резервну копію створено: {path.name}")
    st.markdown("### 🔐 ПРИНЦИПИ ЛОКАЛЬНОЇ РОБОТИ")
    st.info("Дані, документи, відповіді та база зберігаються у вибраній локальній папці. Застосунок не містить API, зовнішніх шрифтів або зовнішніх сервісів. Для майбутнього .exe буде додатково зафіксовано локальний режим та мережеві обмеження.")
    st.markdown("### 📦 СТРУКТУРА ДАНИХ")
    st.code("Дані/\n├── database.db\n├── Розпорядження/\n│   └── <номер>/\n│       ├── основний файл\n│       └── Відповіді/\n└── Резервні копії/",language="text")

st.markdown('<div style="margin-top:2rem;text-align:center" class="muted">LOCAL CONTROL CENTER · Документи та база зберігаються локально</div>',unsafe_allow_html=True)
