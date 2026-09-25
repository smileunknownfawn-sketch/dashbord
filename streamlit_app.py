from __future__ import annotations

import base64
import html
import mimetypes
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

import streamlit as st

try:
    from docx import Document
except Exception:
    Document = None

APP_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = APP_DIR / "data"

st.set_page_config(
    page_title="Контроль виконання розпоряджень",
    page_icon="🇺🇦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------- LOCAL WORKSPACE ----------
def choose_folder() -> str | None:
    """Open a native Windows folder picker when the app runs locally."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder = filedialog.askdirectory(title="Оберіть робочу папку дашборда")
        root.destroy()
        return folder or None
    except Exception:
        return None


def get_workspace() -> Path:
    raw = st.session_state.get("workspace")
    if raw:
        p = Path(raw).expanduser()
    else:
        p = DEFAULT_ROOT
    p.mkdir(parents=True, exist_ok=True)
    (p / "Розпорядження").mkdir(exist_ok=True)
    (p / "Backup").mkdir(exist_ok=True)
    return p


if "workspace" not in st.session_state:
    st.session_state.workspace = str(DEFAULT_ROOT)

WORKSPACE = get_workspace()
ORDERS_DIR = WORKSPACE / "Розпорядження"
DB_PATH = WORKSPACE / "database.db"


# ---------- DATABASE ----------
def db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute(
        """CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            outgoing_number TEXT DEFAULT '',
            deadline TEXT NOT NULL,
            description TEXT NOT NULL,
            folder_name TEXT NOT NULL,
            filename TEXT NOT NULL,
            stored_path TEXT NOT NULL,
            mime_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'progress',
            completed_at TEXT DEFAULT '',
            completion_outgoing TEXT DEFAULT '',
            completion_comment TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS responses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            response_date TEXT NOT NULL,
            outgoing_number TEXT DEFAULT '',
            comment TEXT DEFAULT '',
            filename TEXT NOT NULL,
            stored_path TEXT NOT NULL,
            mime_type TEXT NOT NULL,
            is_final INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
        )"""
    )
    c.execute("PRAGMA foreign_keys=ON")
    c.commit()
    return c


def seed_demo():
    c = db()
    if c.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
        folder = ORDERS_DIR / "01-2026"
        folder.mkdir(parents=True, exist_ok=True)
        document = folder / "Розпорядження_01-2026.txt"
        document.write_text(
            "ЗБРОЙНІ СИЛИ УКРАЇНИ\n\nНАВЧАЛЬНИЙ ПРИКЛАД РОЗПОРЯДЖЕННЯ\n№ 01/2026\n\n"
            "Термін виконання: 05 жовтня 2026 року\n\nЗАВДАННЯ\n"
            "Підготувати та надати узагальнену інформацію про стан виконання визначених завдань.\n\n"
            "Цей файл є демонстраційним прикладом і не є службовим документом.",
            encoding="utf-8",
        )
        now = datetime.now().isoformat(timespec="seconds")
        c.execute(
            """INSERT INTO orders(number,deadline,description,folder_name,filename,stored_path,mime_type,status,created_at,updated_at)
               VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (
                "01/2026",
                "2026-10-05",
                "Підготувати та надати узагальнену інформацію про стан виконання визначених завдань.",
                folder.name,
                document.name,
                str(document.relative_to(WORKSPACE)),
                "text/plain",
                "progress",
                now,
                now,
            ),
        )
        c.commit()
    c.close()


def rows():
    c = db()
    result = c.execute("SELECT * FROM orders ORDER BY deadline ASC, id DESC").fetchall()
    c.close()
    return result


def responses(order_id: int):
    c = db()
    result = c.execute(
        "SELECT * FROM responses WHERE order_id=? ORDER BY response_date DESC, id DESC", (order_id,)
    ).fetchall()
    c.close()
    return result


def days_left(deadline: str) -> int:
    return (date.fromisoformat(deadline) - date.today()).days


def status(row) -> str:
    if row["status"] == "done":
        return "done"
    return "overdue" if days_left(row["deadline"]) < 0 else "progress"


def status_text(value: str) -> str:
    return {"progress": "У роботі", "overdue": "Прострочено", "done": "Виконано"}[value]


def safe_name(value: str) -> str:
    value = "".join(ch if ch.isalnum() or ch in " ._-()[]" else "_" for ch in value).strip()
    return value or "Документ"


def unique_order_folder(number: str) -> Path:
    base = safe_name(number)
    folder = ORDERS_DIR / base
    if not folder.exists():
        return folder
    i = 2
    while (ORDERS_DIR / f"{base}_{i}").exists():
        i += 1
    return ORDERS_DIR / f"{base}_{i}"


def copy_uploaded(uploaded, destination: Path) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / safe_name(uploaded.name)
    stem, suffix = target.stem, target.suffix
    i = 2
    while target.exists():
        target = destination / f"{stem}_{i}{suffix}"
        i += 1
    target.write_bytes(uploaded.getvalue())
    return target


def add_order(number, outgoing, deadline, description, uploaded):
    folder = unique_order_folder(number)
    folder.mkdir(parents=True, exist_ok=True)
    source = copy_uploaded(uploaded, folder)
    now = datetime.now().isoformat(timespec="seconds")
    c = db()
    c.execute(
        """INSERT INTO orders(number,outgoing_number,deadline,description,folder_name,filename,stored_path,mime_type,status,created_at,updated_at)
           VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
        (
            number.strip(), outgoing.strip(), deadline.isoformat(), description.strip(), folder.name,
            source.name, str(source.relative_to(WORKSPACE)), uploaded.type or mimetypes.guess_type(source.name)[0] or "application/octet-stream",
            "progress", now, now,
        ),
    )
    c.commit(); c.close()


def edit_order(row, number, outgoing, deadline, description):
    c = db()
    c.execute(
        "UPDATE orders SET number=?,outgoing_number=?,deadline=?,description=?,updated_at=? WHERE id=?",
        (number.strip(), outgoing.strip(), deadline.isoformat(), description.strip(), datetime.now().isoformat(timespec="seconds"), row["id"]),
    )
    c.commit(); c.close()


def complete(row, outgoing, comment):
    now = datetime.now().isoformat(timespec="seconds")
    c = db()
    c.execute(
        "UPDATE orders SET status='done',completed_at=?,completion_outgoing=?,completion_comment=?,updated_at=? WHERE id=?",
        (now, outgoing.strip(), comment.strip(), now, row["id"]),
    )
    c.commit(); c.close()


def reopen(row):
    c = db()
    c.execute(
        "UPDATE orders SET status='progress',completed_at='',completion_outgoing='',completion_comment='',updated_at=? WHERE id=?",
        (datetime.now().isoformat(timespec="seconds"), row["id"]),
    )
    c.commit(); c.close()


def add_response(row, response_date, outgoing, comment, uploaded, is_final):
    folder = WORKSPACE / row["stored_path"].split(os.sep)[0] if os.sep in row["stored_path"] else ORDERS_DIR / row["folder_name"]
    # Always use the order folder recorded in the database.
    folder = ORDERS_DIR / row["folder_name"]
    response_dir = folder / "Відповіді"
    target = copy_uploaded(uploaded, response_dir)
    c = db()
    c.execute(
        """INSERT INTO responses(order_id,response_date,outgoing_number,comment,filename,stored_path,mime_type,is_final,created_at)
           VALUES(?,?,?,?,?,?,?,?,?)""",
        (
            row["id"], response_date.isoformat(), outgoing.strip(), comment.strip(), target.name,
            str(target.relative_to(WORKSPACE)), uploaded.type or mimetypes.guess_type(target.name)[0] or "application/octet-stream",
            int(is_final), datetime.now().isoformat(timespec="seconds"),
        ),
    )
    c.commit(); c.close()
    if is_final:
        complete(row, outgoing, comment)


def delete_order(row):
    c = db(); c.execute("DELETE FROM responses WHERE order_id=?", (row["id"],)); c.execute("DELETE FROM orders WHERE id=?", (row["id"],)); c.commit(); c.close()
    folder = ORDERS_DIR / row["folder_name"]
    if folder.exists():
        shutil.rmtree(folder, ignore_errors=True)


def open_path(path: Path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(path))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except Exception as exc:
        st.error(f"Не вдалося відкрити файл: {exc}")


def file_preview(path: Path, mime: str, key: str):
    if not path.exists():
        st.error("Файл не знайдено у робочій папці.")
        return
    raw = path.read_bytes()
    if mime == "application/pdf" or path.suffix.lower() == ".pdf":
        b64 = base64.b64encode(raw).decode()
        st.components.v1.html(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="680" style="border:0"></iframe>', height=700)
    elif mime.startswith("image/"):
        st.image(raw, use_container_width=True)
    elif path.suffix.lower() == ".txt":
        st.code(raw.decode("utf-8", errors="replace"), language="text")
    elif path.suffix.lower() == ".docx" and Document:
        doc = Document(path)
        text = "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
        st.markdown(f'<div class="doc">{html.escape(text).replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
    else:
        st.info("Для цього формату доступне відкриття локального оригіналу або завантаження.")
    st.download_button("⬇ Копіювати файл", raw, file_name=path.name, mime=mime, key=key)


seed_demo()

# ---------- STYLE: NO EXTERNAL RESOURCES ----------
st.markdown(
    """<style>
    .stApp{background:radial-gradient(circle at 15% 20%,#263526 0,#0a110c 38%,#050806 100%);color:#edf2ec}
    .stApp:before{content:'';position:fixed;inset:0;pointer-events:none;opacity:.12;background-image:repeating-linear-gradient(35deg,#9caf86 0 1px,transparent 1px 45px),repeating-linear-gradient(-35deg,#65755c 0 1px,transparent 1px 70px)}
    .block-container{max-width:1500px;padding:2rem 3rem;position:relative}
    .brand{border-bottom:1px solid #ffffff1c;padding-bottom:1.2rem;margin-bottom:1.7rem;display:flex;justify-content:space-between}.eyebrow,.kicker{font-size:.64rem;font-weight:800;letter-spacing:.2em;color:#a9bc91}.title{font-size:1.2rem;font-weight:800;letter-spacing:.08em}.title span,.hero em{color:#b7c7a6}.hero h1{font-size:clamp(2rem,4vw,3.4rem);margin:.2rem 0}.hero p{color:#a5afa8}.metric{background:#101a14e8;border:1px solid #d6e2d31f;border-radius:12px;padding:1rem 1.15rem}.metric .label{font-size:.62rem;letter-spacing:.15em;color:#7f8a82;font-weight:800}.metric .value{font-size:2rem;font-weight:700}.card{background:#0a110de8;border:1px solid #d6e2d31f;border-radius:13px;padding:1rem;margin-bottom:.7rem}.overdue{border-left:5px solid #e17c73}.due{border-left:5px solid #d0ae62}.done{border-left:5px solid #83b88e}.badge{display:inline-block;border-radius:999px;padding:.32rem .58rem;font-size:.61rem;font-weight:800}.progress{background:#d0ae6219;color:#d0ae62}.overdue-b{background:#e17c7319;color:#e17c73}.done-b{background:#83b88e19;color:#83b88e}.small{color:#77827a;font-size:.65rem;letter-spacing:.08em}.desc{color:#bdc6be;font-size:.82rem;line-height:1.5;margin-top:.4rem}.red{color:#ff9b93}.gold{color:#e4c777}.doc{background:#f6f6f2;color:#20231f;padding:2.5rem;min-height:400px;border-radius:8px;line-height:1.7;font-family:Georgia,serif}.stButton>button,.stDownloadButton>button{border-radius:7px;border:1px solid #9db5853d;background:#7e97681c;color:#c4d3b4;font-weight:700}.stButton>button:hover{border-color:#b7cba1}.stTextInput input,.stTextArea textarea{background:#0003!important;color:#edf2ec!important}
    </style>""",
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
st.markdown(
    f'<div class="brand"><div><div class="eyebrow">ЗБРОЙНІ СИЛИ УКРАЇНИ</div><div class="title">КОНТРОЛЬ ВИКОНАННЯ <span>РОЗПОРЯДЖЕНЬ</span></div></div><div class="small">● ЛОКАЛЬНИЙ РЕЖИМ • {date.today().strftime("%d.%m.%Y")}</div></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="hero"><div class="kicker">ОПЕРАТИВНИЙ КОНТРОЛЬ</div><h1>Процес виконання <em>розпоряджень</em></h1><p>Локальний реєстр: документи та відповіді зберігаються у вибраній папці на цьому ПК.</p></div>', unsafe_allow_html=True)

# ---------- WORKSPACE ----------
with st.expander(f"📁 РОБОЧА ПАПКА — {WORKSPACE}", expanded=False):
    st.write("Усі розпорядження, відповіді, додатки та база даних зберігаються тут.")
    if st.button("Обрати іншу папку", key="choose_workspace"):
        picked = choose_folder()
        if picked:
            st.session_state.workspace = picked
            st.rerun()
    manual = st.text_input("Або вкажіть шлях вручну", value=str(WORKSPACE), key="manual_workspace")
    if st.button("Застосувати шлях", key="apply_workspace"):
        if manual.strip():
            st.session_state.workspace = manual.strip()
            st.rerun()

# ---------- METRICS ----------
all_orders = rows()
counts = {"all": len(all_orders), "progress": 0, "overdue": 0, "done": 0}
for r in all_orders:
    counts[status(r)] += 1
for col, label, value in zip(st.columns(4), ["УСЬОГО", "У РОБОТІ", "ПРОСТРОЧЕНО", "ВИКОНАНО"], [counts["all"], counts["progress"], counts["overdue"], counts["done"]]):
    with col:
        st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div></div>', unsafe_allow_html=True)

st.write("")
left, right = st.columns([1, 2.2])

# ---------- ADD ORDER ----------
with left:
    st.markdown('<div class="kicker">ДОДАТИ РОЗПОРЯДЖЕННЯ</div>', unsafe_allow_html=True)
    with st.form("add_order", clear_on_submit=True):
        number = st.text_input("№ розпорядження", placeholder="1111")
        outgoing = st.text_input("Вихідний номер", placeholder="Необов’язково")
        deadline = st.date_input("Кінцевий термін", value=date.today())
        description = st.text_area("Що потрібно виконати", height=110)
        uploaded = st.file_uploader("Файл розпорядження", type=["pdf", "doc", "docx", "txt", "png", "jpg", "jpeg", "zip", "rar", "7z"])
        save = st.form_submit_button("＋ ЗБЕРЕГТИ РОЗПОРЯДЖЕННЯ", use_container_width=True)
        if save:
            if not number or not description or not uploaded:
                st.error("Заповніть №, завдання та прикріпіть документ.")
            else:
                add_order(number, outgoing, deadline, description, uploaded)
                st.success(f"Розпорядження № {number} додано у власну папку.")
                st.rerun()

# ---------- LIST ----------
with right:
    query = st.text_input("🔎 Пошук за №, вихідним номером або описом")
    filter_value = st.radio("ФІЛЬТР", ["Усі", "У роботі", "Прострочені", "Виконані"], horizontal=True)

    for row in rows():
        s = status(row)
        haystack = f'{row["number"]} {row["outgoing_number"]} {row["description"]}'.lower()
        if query.lower() not in haystack:
            continue
        if filter_value == "У роботі" and s != "progress":
            continue
        if filter_value == "Прострочені" and s != "overdue":
            continue
        if filter_value == "Виконані" and s != "done":
            continue

        cls = "done" if s == "done" else ("overdue" if s == "overdue" else ("due" if days_left(row["deadline"]) <= 2 else ""))
        badge = "done-b" if s == "done" else ("overdue-b" if s == "overdue" else "progress")
        out = f' • Вих. № {html.escape(row["outgoing_number"])}' if row["outgoing_number"] else ""
        completed = f' • ВИКОНАНО: {row["completed_at"]}' if s == "done" else ""
        st.markdown(
            f'<div class="card {cls}"><b>№ {html.escape(row["number"])}</b><span class="small">{out}</span> '
            f'<span class="badge {badge}">{status_text(s).upper()}</span><div class="desc">{html.escape(row["description"])}</div>'
            f'<div class="small">ТЕРМІН: {row["deadline"]}{completed}</div></div>',
            unsafe_allow_html=True,
        )

        b1, b2, b3, b4, b5 = st.columns(5)
        with b1:
            if st.button("↩ Відповідь", key=f"response{row['id']}", use_container_width=True):
                st.session_state[f"response_{row['id']}"] = True; st.rerun()
        with b2:
            if s != "done":
                if st.button("✓ Виконано", key=f"done{row['id']}", use_container_width=True):
                    st.session_state[f"complete_{row['id']}"] = True; st.rerun()
            else:
                if st.button("↩ Повернути", key=f"undo{row['id']}", use_container_width=True):
                    reopen(row); st.rerun()
        with b3:
            if st.button("✎ Редагувати", key=f"edit{row['id']}", use_container_width=True):
                st.session_state[f"edit_{row['id']}"] = True; st.rerun()
        with b4:
            if st.button("📄 Відкрити", key=f"open{row['id']}", use_container_width=True):
                st.session_state[f"open_{row['id']}"] = True; st.rerun()
        with b5:
            if st.button("📂 Папка", key=f"folder{row['id']}", use_container_width=True):
                open_path(ORDERS_DIR / row["folder_name"])

        # Response form
        if st.session_state.get(f"response_{row['id']}"):
            with st.form(f"response_form_{row['id']}"):
                st.markdown(f"**ВІДПОВІДЬ НА РОЗПОРЯДЖЕННЯ № {row['number']}**")
                response_date = st.date_input("Дата відповіді", value=date.today())
                response_outgoing = st.text_input("Вихідний номер відповіді", placeholder="04/123")
                response_comment = st.text_area("Короткий результат / коментар", height=90)
                response_file = st.file_uploader("Файл відповіді або архів з додатками", type=["pdf", "doc", "docx", "txt", "png", "jpg", "jpeg", "zip", "rar", "7z"], key=f"rf{row['id']}")
                final = st.checkbox("Це остаточна відповідь — позначити розпорядження як виконане")
                r1, r2 = st.columns(2)
                with r1: response_save = st.form_submit_button("ЗБЕРЕГТИ ВІДПОВІДЬ", use_container_width=True)
                with r2: response_cancel = st.form_submit_button("Скасувати", use_container_width=True)
                if response_save:
                    if not response_file:
                        st.error("Додайте файл відповіді або архів.")
                    else:
                        add_response(row, response_date, response_outgoing, response_comment, response_file, final)
                        st.session_state.pop(f"response_{row['id']}", None); st.rerun()
                if response_cancel:
                    st.session_state.pop(f"response_{row['id']}", None); st.rerun()

        # Existing responses
        existing = responses(row["id"])
        if existing:
            with st.expander(f"↩ ВІДПОВІДІ ({len(existing)})", expanded=False):
                for resp in existing:
                    st.markdown(
                        f'**{resp["response_date"]}** • Вих. № **{html.escape(resp["outgoing_number"]) or "—"}** '
                        f'{'🟢 ОСТАТОЧНА' if resp["is_final"] else ""}\n\n{html.escape(resp["comment"]) or "Без коментаря"}'
                    )
                    response_path = WORKSPACE / resp["stored_path"]
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("📄 Відкрити файл", key=f"openresp{resp['id']}", use_container_width=True):
                            st.session_state[f"preview_response_{resp['id']}"] = True; st.rerun()
                    with c2:
                        if st.button("📂 Відкрити папку", key=f"folderresp{resp['id']}", use_container_width=True):
                            open_path(response_path.parent)
                    if st.session_state.get(f"preview_response_{resp['id']}"):
                        file_preview(response_path, resp["mime_type"], f"respdl{resp['id']}")

        if row["status"] == "done" and (row["completion_outgoing"] or row["completion_comment"]):
            with st.expander("✓ РЕЗУЛЬТАТ ВИКОНАННЯ", expanded=False):
                st.write(f"**Вихідний №:** {row['completion_outgoing'] or '—'}")
                st.write(f"**Дата:** {row['completed_at'] or '—'}")
                st.write(row["completion_comment"] or "Коментар не додано.")

        # Completion form
        if st.session_state.get(f"complete_{row['id']}"):
            with st.form(f"complete_form_{row['id']}"):
                st.markdown("**Підтвердити виконання**")
                co = st.text_input("Вихідний номер документа про виконання", value=row["completion_outgoing"])
                cc = st.text_area("Коментар до виконання", value=row["completion_comment"])
                c1, c2 = st.columns(2)
                with c1: confirm = st.form_submit_button("ПІДТВЕРДИТИ", use_container_width=True)
                with c2: cancel = st.form_submit_button("Скасувати", use_container_width=True)
                if confirm:
                    complete(row, co, cc); st.session_state.pop(f"complete_{row['id']}", None); st.rerun()
                if cancel:
                    st.session_state.pop(f"complete_{row['id']}", None); st.rerun()

        # Edit form
        if st.session_state.get(f"edit_{row['id']}"):
            with st.form(f"edit_form_{row['id']}"):
                en = st.text_input("№", value=row["number"]); eo = st.text_input("Вихідний №", value=row["outgoing_number"])
                ed = st.date_input("Термін", value=date.fromisoformat(row["deadline"])); desc = st.text_area("Опис", value=row["description"])
                c1, c2 = st.columns(2)
                with c1: save_edit = st.form_submit_button("ЗБЕРЕГТИ ЗМІНИ", use_container_width=True)
                with c2: cancel_edit = st.form_submit_button("Скасувати", use_container_width=True)
                if save_edit:
                    edit_order(row, en, eo, ed, desc); st.session_state.pop(f"edit_{row['id']}", None); st.rerun()
                if cancel_edit:
                    st.session_state.pop(f"edit_{row['id']}", None); st.rerun()

        # Original document
        if st.session_state.get(f"open_{row['id']}"):
            path = WORKSPACE / row["stored_path"]
            st.markdown(f"**РОЗПОРЯДЖЕННЯ № {row['number']}**")
            file_preview(path, row["mime_type"], f"orderdl{row['id']}")
            if st.button("Закрити перегляд", key=f"close{row['id']}"):
                st.session_state.pop(f"open_{row['id']}", None); st.rerun()

st.markdown('<div class="small">ЛОКАЛЬНИЙ РЕЖИМ • Дані та файли зберігаються у вибраній робочій папці</div>', unsafe_allow_html=True)
