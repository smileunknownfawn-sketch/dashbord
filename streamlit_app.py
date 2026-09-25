from __future__ import annotations
import base64, hashlib, html, mimetypes, sqlite3
from datetime import date, datetime
from pathlib import Path
import streamlit as st
try:
    from docx import Document
except Exception:
    Document = None

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
UPLOAD_DIR = DATA_DIR / "documents"
DB_PATH = DATA_DIR / "orders.db"
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Контроль виконання розпоряджень", page_icon="🇺🇦", layout="wide", initial_sidebar_state="collapsed")

# ---------- Database ----------
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL,
        outgoing_number TEXT DEFAULT '',
        deadline TEXT NOT NULL,
        description TEXT NOT NULL,
        filename TEXT NOT NULL,
        stored_name TEXT NOT NULL,
        mime_type TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'progress',
        completed_at TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )""")
    # Upgrade an existing prototype database without losing its records.
    cols = {r[1] for r in conn.execute("PRAGMA table_info(orders)").fetchall()}
    if "outgoing_number" not in cols:
        conn.execute("ALTER TABLE orders ADD COLUMN outgoing_number TEXT DEFAULT ''")
    if "completed_at" not in cols:
        conn.execute("ALTER TABLE orders ADD COLUMN completed_at TEXT DEFAULT ''")
    conn.commit()
    return conn


def seed_demo():
    conn = db()
    if conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
        name = "demo_order_01_2026.txt"
        text = """ЗБРОЙНІ СИЛИ УКРАЇНИ\n\nНАВЧАЛЬНИЙ ПРИКЛАД РОЗПОРЯДЖЕННЯ\n№ 01/2026\n\nТермін виконання: 05 жовтня 2026 року\n\nЗАВДАННЯ\nПідготувати та надати узагальнену інформацію про стан виконання визначених завдань.\n\nПРИМІТКА\nЦей документ є демонстраційним прикладом для перевірки роботи дашборда. Не є службовим документом."""
        (UPLOAD_DIR / name).write_text(text, encoding="utf-8")
        now = datetime.now().isoformat(timespec="seconds")
        conn.execute("INSERT INTO orders(number,outgoing_number,deadline,description,filename,stored_name,mime_type,status,completed_at,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                     ("01/2026", "", "2026-10-05", "Підготувати та надати узагальнену інформацію про стан виконання визначених завдань.", name, name, "text/plain", "progress", "", now, now))
        conn.commit()
    conn.close()


def rows():
    conn = db()
    data = conn.execute("SELECT * FROM orders ORDER BY deadline ASC, id DESC").fetchall()
    conn.close()
    return data


def days_left(deadline):
    return (date.fromisoformat(deadline) - date.today()).days


def calculated_status(row):
    if row["status"] == "done":
        return "done"
    return "overdue" if days_left(row["deadline"]) < 0 else "progress"


def status_text(status):
    return {"progress": "У роботі", "overdue": "Прострочено", "done": "Виконано"}[status]


def save_upload(uploaded):
    raw = uploaded.getvalue()
    digest = hashlib.sha256(raw).hexdigest()[:12]
    safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in uploaded.name)
    stored = f"{digest}_{safe}"
    (UPLOAD_DIR / stored).write_bytes(raw)
    return stored, uploaded.type or mimetypes.guess_type(uploaded.name)[0] or "application/octet-stream"


def add_order(number, outgoing_number, deadline, description, uploaded):
    stored, mime = save_upload(uploaded)
    now = datetime.now().isoformat(timespec="seconds")
    conn = db()
    conn.execute("INSERT INTO orders(number,outgoing_number,deadline,description,filename,stored_name,mime_type,status,completed_at,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                 (number.strip(), outgoing_number.strip(), deadline.isoformat(), description.strip(), uploaded.name, stored, mime, "progress", "", now, now))
    conn.commit(); conn.close()


def set_status(order_id, new_status):
    conn = db()
    completed_at = datetime.now().isoformat(timespec="seconds") if new_status == "done" else ""
    conn.execute("UPDATE orders SET status=?,completed_at=?,updated_at=? WHERE id=?",
                 (new_status, completed_at, datetime.now().isoformat(timespec="seconds"), order_id))
    conn.commit(); conn.close()


def delete_order(order):
    conn = db(); conn.execute("DELETE FROM orders WHERE id=?", (order["id"],)); conn.commit(); conn.close()
    try: (UPLOAD_DIR / order["stored_name"]).unlink(missing_ok=True)
    except Exception: pass


def preview_document(order):
    path = UPLOAD_DIR / order["stored_name"]
    if not path.exists():
        st.error("Файл документа не знайдено у сховищі."); return
    mime = order["mime_type"]; raw = path.read_bytes()
    if mime == "application/pdf" or path.suffix.lower() == ".pdf":
        b64 = base64.b64encode(raw).decode()
        st.components.v1.html(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="760" style="border:0;border-radius:10px;background:white"></iframe>', height=780)
    elif mime.startswith("image/"):
        st.image(raw, use_container_width=True)
    elif path.suffix.lower() == ".txt":
        st.code(raw.decode("utf-8", errors="replace"), language="text")
    elif path.suffix.lower() == ".docx" and Document:
        doc = Document(path)
        body = "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
        st.markdown(f'<div class="doc-preview">{html.escape(body).replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
    else:
        st.info("Для цього формату доступне завантаження оригіналу документа.")
    st.download_button("⬇ Завантажити оригінал", raw, file_name=order["filename"], mime=mime, key=f"download_{order['id']}")


seed_demo()

# ---------- Military visual design ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Oswald:wght@500;600&display=swap');
.stApp{background:linear-gradient(120deg,rgba(4,8,5,.96),rgba(7,13,9,.87)),url('https://images.unsplash.com/photo-1580137189272-c9379f8864fd?auto=format&fit=crop&w=2400&q=85') center/cover fixed;color:#edf2ec}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;background:linear-gradient(90deg,rgba(0,0,0,.18),transparent 45%,rgba(0,0,0,.28)),radial-gradient(circle at 70% 25%,rgba(91,119,77,.16),transparent 35%)}
.block-container{max-width:1450px;padding:2rem 3rem 2.5rem;position:relative}.brand{border-bottom:1px solid rgba(214,226,211,.13);padding:0 0 1.35rem;margin-bottom:2rem;display:flex;justify-content:space-between;align-items:center}.eyebrow,.kicker{font-size:.64rem;font-weight:800;letter-spacing:.2em;color:#a9bc91}.title{font-family:Oswald,sans-serif;font-size:1.25rem;letter-spacing:.08em}.title span,.hero em{color:#b7c7a6}.hero{margin-bottom:1.8rem}.hero h1{font-size:clamp(2rem,4vw,3.5rem);line-height:1.03;margin:.25rem 0}.hero em{font-style:normal}.hero p{color:#a5afa8;font-size:.9rem;max-width:760px}.metric{background:linear-gradient(145deg,rgba(25,36,29,.93),rgba(10,16,12,.84));border:1px solid rgba(214,226,211,.12);border-radius:12px;padding:1rem 1.15rem;box-shadow:0 18px 55px rgba(0,0,0,.22)}.metric .label{font-size:.62rem;letter-spacing:.15em;color:#7f8a82;font-weight:800}.metric .value{font-size:2rem;font-weight:700;margin-top:.2rem}.card{background:rgba(10,17,13,.87);border:1px solid rgba(214,226,211,.12);border-radius:13px;padding:1.05rem;margin-bottom:.72rem;box-shadow:0 14px 45px rgba(0,0,0,.18)}.overdue{border-left:5px solid #e17c73;background:linear-gradient(90deg,rgba(142,35,35,.21),rgba(10,17,13,.9) 48%)}.due-soon{border-left:5px solid #d0ae62;background:linear-gradient(90deg,rgba(181,143,46,.11),rgba(10,17,13,.9) 48%)}.done{border-left:5px solid #83b88e;background:linear-gradient(90deg,rgba(58,112,70,.10),rgba(10,17,13,.9) 48%)}.badge{display:inline-block;border-radius:999px;padding:.32rem .58rem;font-size:.61rem;font-weight:800;letter-spacing:.06em}.badge-progress{background:rgba(208,174,98,.1);color:#d0ae62}.badge-overdue{background:rgba(225,124,115,.1);color:#e17c73}.badge-done{background:rgba(131,184,142,.1);color:#83b88e}.order-number{font-size:1.05rem;font-weight:800}.desc{color:#bdc6be;font-size:.82rem;line-height:1.5;margin-top:.45rem}.deadline{font-weight:800}.red{color:#ff9b93}.gold{color:#e4c777}.small{color:#77827a;font-size:.65rem;letter-spacing:.08em}.doc-preview{background:#f6f6f2;color:#20231f;padding:2.5rem;min-height:500px;border-radius:8px;line-height:1.7;font-family:Georgia,serif}.notice{padding:.7rem .9rem;border:1px solid rgba(208,174,98,.18);border-radius:8px;background:rgba(208,174,98,.05);color:#b9aa82;font-size:.72rem}.footer{color:#606c63;font-size:.6rem;letter-spacing:.14em;text-align:center;padding:1.5rem}.stButton>button,.stDownloadButton>button{border-radius:7px;border:1px solid rgba(157,181,133,.24);background:rgba(126,151,104,.11);color:#c4d3b4;font-weight:700}.stButton>button:hover,.stDownloadButton>button:hover{border-color:rgba(183,203,161,.55);background:rgba(126,151,104,.18)}.stTextInput input,.stTextArea textarea,.stDateInput input,.stFileUploader{background:rgba(0,0,0,.2)!important;color:#edf2ec!important}.stExpander{background:rgba(8,14,10,.7);border:1px solid rgba(214,226,211,.1)}
</style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="brand"><div><div class="eyebrow">ЗБРОЙНІ СИЛИ УКРАЇНИ</div><div class="title">КОНТРОЛЬ ВИКОНАННЯ <span>РОЗПОРЯДЖЕНЬ</span></div></div><div class="small">● СИСТЕМА АКТИВНА &nbsp; • &nbsp; {date.today().strftime("%d.%m.%Y")}</div></div>', unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="kicker">ОПЕРАТИВНИЙ КОНТРОЛЬ</div><h1>Процес виконання <em>розпоряджень</em></h1><p>Єдиний реєстр документів, контроль термінів, вихідних номерів та швидкий доступ до самого розпорядження.</p></div>', unsafe_allow_html=True)

all_orders = rows(); counts = {"all":len(all_orders),"progress":0,"overdue":0,"done":0}
for r in all_orders: counts[calculated_status(r)] += 1
m1,m2,m3,m4 = st.columns(4)
for col,label,value in [(m1,"УСЬОГО",counts['all']),(m2,"У РОБОТІ",counts['progress']),(m3,"ПРОСТРОЧЕНО",counts['overdue']),(m4,"ВИКОНАНО",counts['done'])]:
    with col: st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div></div>', unsafe_allow_html=True)
st.write("")

left,right = st.columns([1,2.2])
with left:
    st.markdown('<div class="kicker">ДОДАТИ РОЗПОРЯДЖЕННЯ</div>', unsafe_allow_html=True)
    with st.form("add_order", clear_on_submit=True):
        number = st.text_input("№ розпорядження", placeholder="Наприклад: 27/2026")
        outgoing = st.text_input("Вихідний номер", placeholder="Необов’язково — якщо є")
        deadline = st.date_input("Кінцевий термін", value=date.today())
        description = st.text_area("Що потрібно виконати", height=110, placeholder="Коротко сформулюйте завдання...")
        uploaded = st.file_uploader("Файл розпорядження", type=["pdf","doc","docx","txt","png","jpg","jpeg"])
        submitted = st.form_submit_button("＋ ЗБЕРЕГТИ РОЗПОРЯДЖЕННЯ", use_container_width=True)
        if submitted:
            if not number or not description or not uploaded:
                st.error("Заповніть № розпорядження, завдання та прикріпіть документ.")
            else:
                add_order(number, outgoing, deadline, description, uploaded)
                st.success("Розпорядження додано до реєстру.")
                st.rerun()
    st.markdown('<div class="notice">Вихідний номер є необов’язковим. Якщо його немає — запис просто залишається без нього.</div>', unsafe_allow_html=True)

with right:
    search = st.text_input("Пошук", placeholder="№ розпорядження, вихідний номер або короткий опис...")
    filter_label = st.radio("Статус", ["Усі","У роботі","Прострочені","Виконані"], horizontal=True)
    filter_map = {"Усі":"all","У роботі":"progress","Прострочені":"overdue","Виконані":"done"}
    selected = filter_map[filter_label]
    filtered = []
    for r in all_orders:
        status = calculated_status(r)
        text = (r["number"] + " " + (r["outgoing_number"] or "") + " " + r["description"]).lower()
        if (selected == "all" or status == selected) and (not search or search.lower() in text): filtered.append(r)
    st.markdown(f'<div class="kicker" style="margin:.6rem 0 .7rem">РЕЄСТР • {len(filtered)} ЗАПИСІВ</div>', unsafe_allow_html=True)
    for r in filtered:
        status = calculated_status(r); days = days_left(r["deadline"])
        card_class = {"overdue":"overdue","done":"done"}.get(status, "due-soon" if days <= 2 else "")
        date_class = "red" if status == "overdue" else ("gold" if days <= 2 and status != "done" else "")
        outgoing_line = f' &nbsp; • &nbsp; ВИХ. № {html.escape(r["outgoing_number"])}' if r["outgoing_number"] else ''
        completed_line = f'<div class="small" style="margin-top:.45rem;color:#83b88e">ВИКОНАНО: {datetime.fromisoformat(r["completed_at"]).strftime("%d.%m.%Y %H:%M")}</div>' if status == "done" and r["completed_at"] else ''
        st.markdown(f'<div class="card {card_class}"><div style="display:flex;justify-content:space-between;gap:12px"><div class="order-number">№ {html.escape(r["number"])}{outgoing_line}</div><span class="badge badge-{status}">{status_text(status).upper()}</span></div><div class="desc">{html.escape(r["description"])}</div><div style="margin-top:.7rem" class="small">ТЕРМІН &nbsp; <span class="deadline {date_class}">{datetime.fromisoformat(r["deadline"]).strftime("%d.%m.%Y")}</span></div>{completed_line}</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns([1.25,1.15,1])
        with c1:
            if st.button("📄 Відкрити документ", key=f"open_{r['id']}", use_container_width=True): st.session_state["open_id"] = r["id"]
        with c2:
            if status != "done":
                if st.button("✓ Виконано", key=f"done_{r['id']}", use_container_width=True): set_status(r["id"], "done"); st.rerun()
            else:
                if st.button("↩ Повернути в роботу", key=f"progress_{r['id']}", use_container_width=True): set_status(r["id"], "progress"); st.rerun()
        with c3:
            if st.button("🗑 Видалити", key=f"delete_{r['id']}", use_container_width=True):
                st.session_state["confirm_delete"] = r["id"]
        if st.session_state.get("confirm_delete") == r["id"]:
            st.warning("Підтвердити видалення цього запису та прикріпленого документа?")
            y,n = st.columns(2)
            with y:
                if st.button("Так, видалити", key=f"yes_{r['id']}"): delete_order(r); st.session_state.pop("confirm_delete", None); st.rerun()
            with n:
                if st.button("Скасувати", key=f"no_{r['id']}"): st.session_state.pop("confirm_delete", None); st.rerun()

open_id = st.session_state.get("open_id")
if open_id:
    order = next((r for r in rows() if r["id"] == open_id), None)
    if order:
        st.divider()
        st.markdown(f'<div class="kicker">ПЕРЕГЛЯД ДОКУМЕНТА • № {html.escape(order["number"])}</div>', unsafe_allow_html=True)
        meta = f'Термін: {datetime.fromisoformat(order["deadline"]).strftime("%d.%m.%Y")} • Статус: {status_text(calculated_status(order))}'
        if order["outgoing_number"]: meta += f' • Вих. № {html.escape(order["outgoing_number"])}'
        st.caption(meta)
        if st.button("✕ Закрити перегляд", key="close_preview"): st.session_state.pop("open_id", None); st.rerun()
        preview_document(order)

st.markdown('<div class="footer">СИСТЕМА КОНТРОЛЮ ВИКОНАННЯ РОЗПОРЯДЖЕНЬ • ДЕМОНСТРАЦІЙНА ВЕРСІЯ</div>', unsafe_allow_html=True)
