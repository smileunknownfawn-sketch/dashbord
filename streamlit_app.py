from __future__ import annotations

import base64
import html
import mimetypes
import os
import sqlite3
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

import streamlit as st

# ============================================================
# ДАШБОРД ВИКОНАННЯ РОЗПОРЯДЖЕНЬ — v1.1
# Local-first architecture: documents and database live in DATA_DIR.
# ============================================================

st.set_page_config(
    page_title="Процес виконання розпоряджень",
    page_icon="🇺🇦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP = Path(__file__).resolve().parent
DEFAULT_WORKSPACE = APP / "data"

for key, value in {
    "workspace": str(DEFAULT_WORKSPACE),
    "add_open": False,
    "response_order": None,
    "language": "Українська",
    "language_popup": False,
    "just_added": False,
    "settings_open": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

WORK = Path(st.session_state.workspace)
ORDERS = WORK / "Розпорядження"
BACKUPS = WORK / "Резервні копії"
WORK.mkdir(parents=True, exist_ok=True)
ORDERS.mkdir(parents=True, exist_ok=True)
BACKUPS.mkdir(parents=True, exist_ok=True)
DB = WORK / "database.db"

# ----------------------------- styling -----------------------------
CSS = """
<style>
:root { --bg:#07100a; --panel:#0c1710; --line:#dce9d91c; --text:#edf2ec; --muted:#8c9a90; --gold:#d0ae62; --red:#e36e68; --green:#79b88a; }
html, body, [class*=css] { font-family: Inter, Segoe UI, Arial, sans-serif; }
.stApp { background: radial-gradient(circle at 80% 10%, #263c2b 0, transparent 28%), linear-gradient(135deg,#050a06,#142118 50%,#050806); color:var(--text); }
.block-container { max-width:1480px; padding:1.5rem 3rem 3rem; }
.hero h1 { font-family: "Segoe UI", Inter, Arial, sans-serif; font-style:normal; font-weight:800; font-size:clamp(2.1rem,4vw,3.7rem); letter-spacing:-.045em; margin:.2rem 0 .3rem; }
.eyebrow { color:#b8cba9; font-weight:800; font-size:.66rem; letter-spacing:.20em; }
.version { text-align:right; color:#8e9a91; font-size:.68rem; letter-spacing:.12em; font-weight:800; }
.panel,.order,.metric { background:rgba(8,18,12,.91); border:1px solid var(--line); border-radius:16px; padding:1rem; }
.metric { min-height:90px; }
.order { margin:.75rem 0 .25rem; border-left:5px solid var(--gold); box-shadow:0 10px 30px #0003; }
.order.overdue { border-left-color:var(--red); }
.order.done { border-left-color:var(--green); }
.desc { color:#c3cdc6; margin:.55rem 0; line-height:1.55; }
.muted { color:var(--muted); font-size:.70rem; letter-spacing:.06em; }
.badge { padding:.28rem .58rem; border-radius:999px; font-size:.62rem; font-weight:850; }
.work { color:var(--gold); background:#d0ae6218; }
.late { color:var(--red); background:#e36e6818; }
.finished { color:var(--green); background:#79b88a18; }
.stButton>button { border-radius:9px; background:#78925f20; border:1px solid #a9bc9140; color:#dce7d8; font-weight:800; min-height:42px; }
.stButton>button:hover { border-color:#d0ae62aa; background:#d0ae6215; }
.successbox { padding:18px; border:1px solid #9ab58a55; border-radius:14px; background:#263d2a; margin:.5rem 0 1rem; }
.alertbox { padding:14px 18px; border:1px solid #e36e6855; border-radius:14px; background:#3a1717; }
.todaybox { padding:14px 18px; border:1px solid #d0ae6255; border-radius:14px; background:#302711; }
.stTextInput input,.stTextArea textarea,.stDateInput input { background:#0005!important; color:#fff!important; }
hr { border-color:#ffffff12!important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ----------------------------- database -----------------------------
def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            deadline TEXT NOT NULL,
            description TEXT NOT NULL,
            folder TEXT NOT NULL,
            filename TEXT NOT NULL,
            path TEXT NOT NULL,
            mime TEXT NOT NULL,
            status TEXT DEFAULT 'progress',
            completion_outgoing TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS responses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            response_date TEXT NOT NULL,
            outgoing TEXT DEFAULT '',
            comment TEXT DEFAULT '',
            filename TEXT NOT NULL,
            path TEXT NOT NULL,
            mime TEXT NOT NULL,
            is_final INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
    """)
    c.commit()
    return c


def safe_name(value: str) -> str:
    value = str(value).strip()
    return "".join(ch if ch.isalnum() or ch in " ._-()[]" else "_" for ch in value) or "Документ"


def save_upload(upload, folder: Path) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    p = folder / safe_name(upload.name)
    counter = 2
    while p.exists():
        p = folder / f"{p.stem}_{counter}{p.suffix}"
        counter += 1
    p.write_bytes(upload.getvalue())
    return p


def order_state(row):
    if row["status"] == "done":
        return "done"
    try:
        d = date.fromisoformat(row["deadline"])
        if d < date.today():
            return "overdue"
        if d == date.today():
            return "today"
    except Exception:
        pass
    return "progress"


def days_text(deadline: str) -> str:
    try:
        delta = (date.fromisoformat(deadline) - date.today()).days
        if delta < 0:
            return f"ПРОСТРОЧЕНО НА {abs(delta)} ДНІВ"
        if delta == 0:
            return "ТЕРМІН СЬОГОДНІ"
        if delta == 1:
            return "ЗАЛИШИВСЯ 1 ДЕНЬ"
        return f"ЗАЛИШИЛОСЯ {delta} ДНІВ"
    except Exception:
        return ""


def add_order(number, deadline, description, upload):
    folder = ORDERS / safe_name(number)
    counter = 2
    while folder.exists():
        folder = ORDERS / f"{safe_name(number)}_{counter}"
        counter += 1
    p = save_upload(upload, folder)
    c = db()
    c.execute(
        "INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
        (number, deadline.isoformat(), description, folder.name, p.name,
         str(p.relative_to(WORK)), upload.type or mimetypes.guess_type(p.name)[0] or "application/octet-stream",
         "progress", datetime.now().isoformat()),
    )
    c.commit(); c.close()


def add_response(row, response_date, outgoing, comment, upload, final):
    folder = ORDERS / row["folder"] / "Відповіді"
    p = save_upload(upload, folder)
    c = db()
    c.execute(
        "INSERT INTO responses(order_id,response_date,outgoing,comment,filename,path,mime,is_final,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
        (row["id"], response_date.isoformat(), outgoing.strip(), comment.strip(), p.name,
         str(p.relative_to(WORK)), upload.type or mimetypes.guess_type(p.name)[0] or "application/octet-stream",
         int(final), datetime.now().isoformat()),
    )
    if final:
        c.execute("UPDATE orders SET status='done', completion_outgoing=? WHERE id=?", (outgoing.strip(), row["id"]))
    c.commit(); c.close()


def get_responses(order_id):
    c = db(); rows = c.execute("SELECT * FROM responses WHERE order_id=? ORDER BY response_date DESC, id DESC", (order_id,)).fetchall(); c.close(); return rows


def make_backup():
    import shutil
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    target = BACKUPS / f"Резервна_копія_{stamp}"
    target.mkdir(parents=True, exist_ok=True)
    if DB.exists(): shutil.copy2(DB, target / "database.db")
    if ORDERS.exists(): shutil.copytree(ORDERS, target / "Розпорядження", dirs_exist_ok=True)
    return target

# ----------------------------- viewer -----------------------------
def local_path(rel):
    p = (WORK / rel).resolve()
    try:
        p.relative_to(WORK.resolve())
    except ValueError:
        return None
    return p if p.exists() else None


def show_file_viewer(row, response=False):
    rel = row["path"]
    p = local_path(rel)
    if not p:
        st.error("Файл не знайдено у папці даних.")
        return
    mime = row["mime"] or mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    st.markdown(f"**{html.escape(p.name)}** · `{mime}`")
    data = p.read_bytes()
    st.download_button("⬇ ЗАВАНТАЖИТИ ФАЙЛ", data=data, file_name=p.name, mime=mime, key=f"download_{'r' if response else 'o'}_{row['id']}")
    if mime == "application/pdf" or p.suffix.lower() == ".pdf":
        # Works in Streamlit web and local builds without opening a server-side OS program.
        b64 = base64.b64encode(data).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="760" style="border:1px solid #ffffff18;border-radius:12px"></iframe>',
            unsafe_allow_html=True,
        )
    elif mime.startswith("image/"):
        st.image(data, use_container_width=True)
    elif mime.startswith("text/") or p.suffix.lower() in {".txt", ".csv", ".log", ".md"}:
        try:
            st.code(data.decode("utf-8", errors="replace"), language="text")
        except Exception:
            pass
    else:
        st.info("Для цього формату вбудований перегляд не використовується. Натисніть «Завантажити файл» або відкрийте його у програмі ОС.")
        if st.button("🖥 ВІДКРИТИ У ПРОГРАМІ ОС", key=f"os_{'r' if response else 'o'}_{row['id']}"):
            try:
                if sys.platform.startswith("win"):
                    os.startfile(str(p))
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", str(p)])
                else:
                    subprocess.Popen(["xdg-open", str(p)])
            except Exception as exc:
                st.error(f"Не вдалося відкрити файл: {exc}")

# ----------------------------- initial demo -----------------------------
c = db()
if c.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
    folder = ORDERS / "01-2026"
    folder.mkdir(exist_ok=True)
    p = folder / "Розпорядження_01-2026.txt"
    p.write_text("ДЕМОНСТРАЦІЙНЕ РОЗПОРЯДЖЕННЯ\n\nПідготувати та надати узагальнену інформацію про стан виконання визначених завдань.", encoding="utf-8")
    c.execute(
        "INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
        ("01/2026", "2026-10-05", "Підготувати та надати узагальнену інформацію про стан виконання визначених завдань.", folder.name, p.name, str(p.relative_to(WORK)), "text/plain", "progress", datetime.now().isoformat()),
    )
    c.commit()
c.close()

# ----------------------------- language -----------------------------
top_left, top_right = st.columns([4, 1])
with top_left:
    lang = st.selectbox("Мова інтерфейсу", ["Українська", "Російська"], index=0 if st.session_state.language == "Українська" else 1, label_visibility="collapsed")
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.session_state.language_popup = lang == "Російська"
        st.rerun()
    st.markdown(f'<div class="muted">Мова інтерфейсу — <b>{html.escape(lang)}</b></div>', unsafe_allow_html=True)
with top_right:
    st.markdown('<div class="version">ВЕРСІЯ 1.1</div>', unsafe_allow_html=True)

if st.session_state.language_popup and st.session_state.language == "Російська":
    img = APP / "language-russian.jpg"
    if img.exists():
        b64 = base64.b64encode(img.read_bytes()).decode()
        st.markdown(
            f'<div style="text-align:center;background:#050807;border:1px solid #d0ae6266;border-radius:18px;padding:16px;margin:.5rem 0 1rem">'
            f'<div style="font-size:30px;font-weight:900;color:#f1df8d;margin-bottom:12px">Ти що москать?</div>'
            f'<img src="data:image/jpeg;base64,{b64}" style="width:min(760px,100%);border-radius:12px;display:block;margin:auto">'
            f'</div>', unsafe_allow_html=True)
        time.sleep(3.5)
        st.session_state.language_popup = False
        st.rerun()
    else:
        st.warning("Файл language-russian.jpg не знайдено у папці програми.")
        st.session_state.language_popup = False

# ----------------------------- header -----------------------------
st.markdown(
    '<div class="eyebrow">ЗБРОЙНІ СИЛИ УКРАЇНИ</div>'
    '<div class="hero"><h1>Процес виконання розпоряджень</h1>'
    '<p class="muted">Контроль термінів, документів та відповідей у єдиному робочому просторі.</p></div>',
    unsafe_allow_html=True,
)

# ----------------------------- settings -----------------------------
settings_col1, settings_col2 = st.columns([1, 1])
with settings_col1:
    if st.button("⚙ НАЛАШТУВАННЯ", key="settings_btn"):
        st.session_state.settings_open = not st.session_state.settings_open
        st.rerun()
with settings_col2:
    if st.button("💾 РЕЗЕРВНА КОПІЯ", key="backup_btn"):
        target = make_backup()
        st.success(f"Резервну копію створено: {target.name}")

if st.session_state.settings_open:
    with st.expander("Налаштування системи", expanded=True):
        st.markdown(f"**Папка даних:** `{WORK}`")
        st.caption("У локальній версії тут буде основна папка з базою, розпорядженнями та відповідями. Інтернет для даних не потрібен.")
        st.info("Перемикання папки даних буде підключено під час пакування у .exe, щоб Windows-діалог вибору папки працював без обхідних рішень.")

# ----------------------------- add order -----------------------------
if st.button("＋ ДОДАТИ РОЗПОРЯДЖЕННЯ", key="add_btn"):
    st.session_state.add_open = not st.session_state.add_open
    st.rerun()

if st.session_state.add_open:
    with st.form("new_order", clear_on_submit=False):
        st.markdown("### Нове розпорядження")
        a, b = st.columns(2)
        with a:
            number = st.text_input("№ розпорядження")
            deadline = st.date_input("Дата, до якої потрібно виконати", value=date.today())
        with b:
            description = st.text_area("Короткий опис розпорядження", height=125)
            upload = st.file_uploader("Файл розпорядження")
        s1, s2 = st.columns(2)
        with s1:
            save = st.form_submit_button("ЗБЕРЕГТИ РОЗПОРЯДЖЕННЯ", use_container_width=True)
        with s2:
            cancel = st.form_submit_button("СКАСУВАТИ", use_container_width=True)
        if cancel:
            st.session_state.add_open = False
            st.rerun()
        if save:
            if not number.strip() or not description.strip() or not upload:
                st.error("Заповніть №, короткий опис та додайте файл розпорядження.")
            else:
                add_order(number, deadline, description, upload)
                st.session_state.add_open = False
                st.session_state.just_added = True
                st.rerun()

if st.session_state.pop("just_added", False):
    st.markdown('<div class="successbox"><b>РОЗПОРЯДЖЕННЯ ДОДАНО</b><br><span class="muted">Опять работа? 😄</span></div>', unsafe_allow_html=True)
    sound = APP / "opiat-rabota.mp3"
    if sound.exists():
        b64 = base64.b64encode(sound.read_bytes()).decode()
        st.markdown(f'<audio controls autoplay style="width:100%;max-width:420px"><source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg"></audio>', unsafe_allow_html=True)
    else:
        st.warning("opiat-rabota.mp3 не знайдено. Додайте його поруч із streamlit_app.py.")

# ----------------------------- metrics -----------------------------
c = db(); rows = c.execute("SELECT * FROM orders ORDER BY deadline, id DESC").fetchall(); c.close()
counts = {"progress": 0, "today": 0, "overdue": 0, "done": 0}
for row in rows:
    counts[order_state(row)] += 1

for col, label, value in zip(
    st.columns(4),
    ["УСЬОГО", "У РОБОТІ", "ТЕРМІН СЬОГОДНІ / ПРОСТРОЧЕНО", "ВИКОНАНО"],
    [len(rows), counts["progress"], counts["today"] + counts["overdue"], counts["done"]],
):
    with col:
        st.markdown(f'<div class="metric"><div class="muted">{label}</div><b style="font-size:1.8rem">{value}</b></div>', unsafe_allow_html=True)

# ----------------------------- filters -----------------------------
search = st.text_input("🔎 Пошук", placeholder="№, вихідний номер, короткий опис або назва файлу...")
filter_value = st.radio("ФІЛЬТР", ["Усі", "У роботі", "Термін сьогодні", "Прострочені", "Виконані"], horizontal=True)

# ----------------------------- order cards -----------------------------
for row in rows:
    state = order_state(row)
    response_rows = get_responses(row["id"])
    outgoing_blob = " ".join(r["outgoing"] or "" for r in response_rows)
    haystack = f'{row["number"]} {row["description"]} {row["filename"]} {outgoing_blob}'.lower()
    if search.lower() not in haystack:
        continue
    if filter_value == "У роботі" and state not in {"progress", "today"}:
        continue
    if filter_value == "Термін сьогодні" and state != "today":
        continue
    if filter_value == "Прострочені" and state != "overdue":
        continue
    if filter_value == "Виконані" and state != "done":
        continue

    label = {"overdue": "ПРОСТРОЧЕНО", "today": "ТЕРМІН СЬОГОДНІ", "done": "ВИКОНАНО", "progress": "У РОБОТІ"}[state]
    badge_class = "late" if state == "overdue" else ("finished" if state == "done" else "work")
    order_class = "overdue" if state == "overdue" else ("done" if state == "done" else "")
    extra = days_text(row["deadline"])
    completion = f' · Вих. № {html.escape(row["completion_outgoing"])}' if row["completion_outgoing"] else ""

    st.markdown(
        f'<div class="order {order_class}">'
        f'<div><b>№ {html.escape(row["number"])}</b> <span class="badge {badge_class}">{label}</span></div>'
        f'<div class="desc">{html.escape(row["description"])}</div>'
        f'<div class="muted">ТЕРМІН: {row["deadline"]} · {extra}{completion}</div>'
        f'</div>', unsafe_allow_html=True)

    a, b, c = st.columns(3)
    with a:
        if st.button("📄 ВІДКРИТИ / ПЕРЕГЛЯНУТИ", key=f"open_{row['id']}"):
            st.session_state.viewer = ("order", row["id"])
            st.rerun()
    with b:
        if st.button("↩ ДОДАТИ ВІДПОВІДЬ", key=f"resp_{row['id']}"):
            st.session_state.response_order = row["id"]
            st.rerun()
    with c:
        if state != "done" and st.button("✓ ВИКОНАНО", key=f"done_{row['id']}"):
            st.session_state.response_order = row["id"]
            st.session_state.final_response = True
            st.rerun()

    # Inline viewer. No os.startfile() is used for the web dashboard.
    if st.session_state.get("viewer") == ("order", row["id"]):
        with st.expander(f"📖 Перегляд розпорядження № {row['number']}", expanded=True):
            show_file_viewer(row)
            if st.button("Закрити перегляд", key=f"close_view_{row['id']}"):
                st.session_state.viewer = None
                st.rerun()

    if st.session_state.response_order == row["id"]:
        st.markdown('<div class="panel"><b>ВІДПОВІДЬ НА РОЗПОРЯДЖЕННЯ</b></div>', unsafe_allow_html=True)
        with st.form(f"response_form_{row['id']}"):
            rd = st.date_input("Дата відповіді", value=date.today(), key=f"rd_{row['id']}")
            outgoing = st.text_input("Вихідний номер відповіді", key=f"out_{row['id']}")
            comment = st.text_area("Короткий зміст відповіді", key=f"comment_{row['id']}")
            response_file = st.file_uploader("Файл відповіді / архів", key=f"rf_{row['id']}")
            default_final = st.session_state.pop("final_response", False)
            final = st.checkbox("Позначити розпорядження виконаним", value=default_final, key=f"final_{row['id']}")
            save_response = st.form_submit_button("ЗБЕРЕГТИ ВІДПОВІДЬ", use_container_width=True)
            if save_response:
                if not response_file:
                    st.error("Додайте файл відповіді або архів.")
                else:
                    add_response(row, rd, outgoing, comment, response_file, final)
                    st.session_state.response_order = None
                    st.success("Відповідь збережено у папці цього розпорядження.")
                    st.rerun()

    # Response history
    if response_rows:
        with st.expander(f"📎 Відповіді та історія ({len(response_rows)})"):
            for rr in response_rows:
                status_text = "ВИКОНАНО" if rr["is_final"] else "ДОДАНО"
                out = f' · Вих. № {html.escape(rr["outgoing"])}' if rr["outgoing"] else ""
                st.markdown(f'**{rr["response_date"]}** · {status_text}{out} · `{html.escape(rr["filename"])}`')
                if rr["comment"]:
                    st.caption(rr["comment"])
                if st.button("📖 Переглянути відповідь", key=f"view_resp_{rr['id']}"):
                    st.session_state.viewer = ("response", rr["id"])
                    st.rerun()
                if st.session_state.get("viewer") == ("response", rr["id"]):
                    show_file_viewer(rr, response=True)

st.markdown('<div class="muted" style="text-align:center;margin-top:3rem">СИСТЕМА КОНТРОЛЮ ВИКОНАННЯ • LOCAL-FIRST • ВЕРСІЯ 1.1</div>', unsafe_allow_html=True)
