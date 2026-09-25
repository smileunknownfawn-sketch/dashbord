from __future__ import annotations

import base64
import html
import mimetypes
from calendar import monthrange
from datetime import date, datetime, timedelta
from pathlib import Path

import streamlit as st

from core.analytics import distribution, metrics, monthly, responsible_table, workload_index
from core.backup import BackupService
from core.config import APP_TITLE, APP_VERSION, CATEGORIES, MONTHS_UA, PRIORITIES, WEEKDAYS_UA, AppPaths
from core.database import Database
from core.exports import csv_bytes, filename, pdf_bytes, xlsx_bytes
from core.orders import OrderService
from core.storage import LocalStorage, StorageError


st.set_page_config(page_title=APP_TITLE, page_icon="🇺🇦", layout="wide", initial_sidebar_state="collapsed")

ROOT = Path(__file__).resolve().parent
DEFAULT_WORKSPACE = ROOT / "data"

CSS = """
<style>
:root{--bg:#050907;--panel:rgba(11,19,15,.94);--panel2:rgba(17,29,22,.92);--line:rgba(211,225,210,.13);--text:#eef5ef;--muted:#9eaca1;--gold:#d3b263;--green:#75bd8c;--red:#ef746d;--yellow:#e5c766;--blue:#77a8d8}
html,body,[class*=css]{font-family:"Segoe UI",Arial,sans-serif}
.stApp{background:radial-gradient(circle at 8% 7%,rgba(89,124,76,.23),transparent 25%),radial-gradient(circle at 90% 15%,rgba(211,178,99,.10),transparent 23%),linear-gradient(135deg,#020504 0%,#08130d 47%,#030605 100%);color:var(--text)}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.08;background-image:linear-gradient(rgba(200,220,200,.22) 1px,transparent 1px),linear-gradient(90deg,rgba(200,220,200,.22) 1px,transparent 1px);background-size:58px 58px}
.stApp:after{content:"";position:fixed;inset:0;pointer-events:none;opacity:.06;background:radial-gradient(ellipse at center,transparent 38%,#000 100%)}
.block-container{max-width:1600px;padding:1rem 2.4rem 5rem;position:relative;z-index:1}
.hero{padding:.4rem 0 1rem}.eyebrow{font-size:.64rem;letter-spacing:.26em;color:#b6c4b5;font-weight:900}.hero h1{font-size:clamp(2rem,4vw,4rem);line-height:.98;font-weight:950;letter-spacing:-.055em;margin:.18rem 0 .3rem}.subtitle{color:#aebbb0;font-size:.82rem;max-width:760px}.version{text-align:right;color:#8e9d91;font-size:.67rem;font-weight:900;letter-spacing:.16em;padding-top:.25rem}
.panel,.metric,.order-card,.focus,.notice,.calendar-card,.detail-card{background:var(--panel);border:1px solid var(--line);border-radius:18px;box-shadow:0 18px 50px rgba(0,0,0,.20)}.panel,.focus,.detail-card{padding:1rem}.metric{padding:1rem;min-height:112px}.metric .label{color:#9eaca1;font-size:.62rem;font-weight:950;letter-spacing:.12em}.metric .num{font-size:2.15rem;font-weight:950;margin:.15rem 0}.metric .hint{font-size:.68rem;color:#89988d}.metric.green{border-top:2px solid var(--green)}.metric.red{border-top:2px solid var(--red)}.metric.gold{border-top:2px solid var(--gold)}.metric.blue{border-top:2px solid var(--blue)}
.order-card{margin:.55rem 0;padding:1rem 1.1rem;border-left:5px solid var(--gold)}.order-card.overdue{border-left-color:var(--red)}.order-card.today{border-left-color:var(--yellow)}.order-card.done{border-left-color:var(--green)}.order-card:hover{border-color:#d3b26355}.order-title{font-size:1.05rem;font-weight:950}.desc{color:#c8d3ca;line-height:1.48;margin:.35rem 0}.muted{color:var(--muted);font-size:.72rem}.badge,.tag{display:inline-block;border-radius:999px;padding:.27rem .58rem;font-size:.59rem;font-weight:950;margin:.12rem}.badge.work{color:#d9bd6d;background:#d9bd6d18}.badge.late{color:#ef7770;background:#ef777018}.badge.today{color:#ead06b;background:#ead06b18}.badge.done{color:#79c995;background:#79c99518}.badge.blue{color:#80b4e8;background:#80b4e818}.tag{color:#c3cec5;background:#ffffff09;border:1px solid #ffffff12}.section-title{font-size:1.04rem;font-weight:950;letter-spacing:.03em;margin:1rem 0 .65rem}.small-title{font-size:.72rem;font-weight:950;letter-spacing:.13em;color:#9fac9f}.focus{border-color:#d3b26345;background:linear-gradient(135deg,rgba(211,178,99,.11),rgba(10,19,14,.95))}.notice{padding:.7rem .85rem;margin:.3rem 0;border-left:4px solid var(--yellow)}.notice.red{border-left-color:var(--red)}.notice.green{border-left-color:var(--green)}.timeline-item{padding:.65rem 0 .65rem 1rem;border-left:2px solid #63875a;margin-left:.3rem}.calendar-card{min-height:105px;padding:.7rem;text-align:center}.calendar-card.empty{opacity:.35}.calendar-day{font-size:.64rem;color:#8e9d91}.calendar-count{font-size:1.45rem;font-weight:950}.calendar-count.red{color:var(--red)}.calendar-count.green{color:var(--green)}.footer{padding-top:2rem;color:#69766d;text-align:center;font-size:.63rem;letter-spacing:.08em}.danger{border-color:#ef746655;background:#35171355}.stButton>button{border-radius:11px;background:rgba(120,146,95,.10);border:1px solid rgba(169,188,145,.23);color:#e4ece3;font-weight:900;min-height:41px}.stButton>button:hover{border-color:rgba(218,194,111,.8);background:rgba(208,174,98,.13)}.stTextInput input,.stTextArea textarea,.stDateInput input,.stNumberInput input{background:rgba(0,0,0,.40)!important;color:#fff!important;border-color:rgba(190,214,193,.15)!important}.stSelectbox div[data-baseweb="select"]>div,.stMultiSelect div[data-baseweb="select"]>div{background:rgba(0,0,0,.40)}.stFileUploader{background:rgba(0,0,0,.14);border-radius:14px}.stExpander{background:rgba(0,0,0,.13);border:1px solid #ffffff0c;border-radius:14px}.stDataFrame{border-radius:14px;overflow:hidden}.metric-grid{margin-bottom:.5rem}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


if "workspace" not in st.session_state:
    st.session_state.workspace = str(DEFAULT_WORKSPACE)
if "page" not in st.session_state:
    st.session_state.page = "Головна"
if "selected_order" not in st.session_state:
    st.session_state.selected_order = None
if "add_open" not in st.session_state:
    st.session_state.add_open = False
if "edit_open" not in st.session_state:
    st.session_state.edit_open = False
if "response_open" not in st.session_state:
    st.session_state.response_open = False
if "toast" not in st.session_state:
    st.session_state.toast = ""
if "compact" not in st.session_state:
    st.session_state.compact = False


@st.cache_resource(show_spinner=False)
def services(workspace: str):
    paths = AppPaths.from_root(Path(workspace))
    paths.ensure()
    db = Database(paths.database)
    storage = LocalStorage(paths)
    return paths, db, storage, OrderService(db, storage), BackupService(paths, db)


paths, db, storage, order_service, backup_service = services(st.session_state.workspace)


def set_page(name: str):
    st.session_state.page = name
    st.session_state.selected_order = None
    st.session_state.add_open = False
    st.session_state.edit_open = False
    st.session_state.response_open = False


def status_label(row):
    s = order_service.status(row)
    return {"progress": "У РОБОТІ", "today": "ТЕРМІН СЬОГОДНІ", "overdue": "ПРОСТРОЧЕНО", "done": "ВИКОНАНО"}[s]


def status_class(row):
    return order_service.status(row)


def toast(message: str):
    st.session_state.toast = message


def show_toast():
    if st.session_state.toast:
        st.success(st.session_state.toast)
        st.session_state.toast = ""


def play_added_sound():
    sound = ROOT / "sounds" / "opiat-rabota.mp3"
    if not sound.exists():
        return
    data = base64.b64encode(sound.read_bytes()).decode()
    st.markdown(f'<audio autoplay><source src="data:audio/mpeg;base64,{data}"></audio>', unsafe_allow_html=True)


def render_header():
    left, right = st.columns([5, 1])
    with left:
        st.markdown('<div class="eyebrow">🇺🇦 ЛОКАЛЬНИЙ ЦЕНТР КОНТРОЛЮ</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero"><h1>{APP_TITLE}</h1><div class="subtitle">Контроль отримання, виконання, відповідей, дедлайнів та документів — в одному автономному робочому середовищі.</div></div>', unsafe_allow_html=True)
    with right:
        st.markdown(f'<div class="version">ВЕРСІЯ {APP_VERSION}</div>', unsafe_allow_html=True)
        if st.button("⚙ Налаштування", use_container_width=True):
            set_page("Налаштування")
    nav = ["Головна", "Розпорядження", "Календар", "Аналітика", "Звіти", "Кошик", "Налаштування"]
    cols = st.columns(len(nav))
    for col, item in zip(cols, nav):
        with col:
            if st.button(item, use_container_width=True, type="primary" if st.session_state.page == item else "secondary"):
                set_page(item)


def render_metrics(rows):
    m = metrics(rows)
    values = [("УСЬОГО", m.total, "green", "зареєстровано"), ("У РОБОТІ", m.active, "gold", "активні"), ("СЬОГОДНІ", m.today, "blue", "термін сьогодні"), ("ПРОСТРОЧЕНО", m.overdue, "red", f"{m.overdue_rate}% від усіх"), ("ВИКОНАНО", m.completed, "green", f"{m.completion_rate}% виконання")]
    cols = st.columns(5)
    for col, (label, number, color, hint) in zip(cols, values):
        with col:
            st.markdown(f'<div class="metric {color}"><div class="label">{label}</div><div class="num">{number}</div><div class="hint">{hint}</div></div>', unsafe_allow_html=True)


def render_focus(rows):
    active = [r for r in rows if order_service.status(r) != "done"]
    overdue = [r for r in active if order_service.status(r) == "overdue"][:5]
    today = [r for r in active if order_service.status(r) == "today"][:5]
    soon = []
    for r in active:
        try:
            left = (date.fromisoformat(r["deadline"]) - date.today()).days
        except Exception:
            continue
        if 1 <= left <= 3:
            soon.append(r)
    soon = soon[:5]
    st.markdown('<div class="section-title">🎯 Фокус дня</div>', unsafe_allow_html=True)
    if not overdue and not today and not soon:
        st.markdown('<div class="focus"><b>Все спокійно.</b><br><span class="muted">Немає розпоряджень, які потребують термінової уваги.</span></div>', unsafe_allow_html=True)
        return
    cols = st.columns(3)
    for col, title, items, kind in [(cols[0], "🔴 ПРОСТРОЧЕНІ", overdue, "red"), (cols[1], "⚠️ СЬОГОДНІ", today, "yellow"), (cols[2], "🟡 НАЙБЛИЖЧІ", soon, "yellow")]:
        with col:
            st.markdown(f'<div class="small-title">{title}</div>', unsafe_allow_html=True)
            if not items:
                st.caption("Немає")
            for row in items:
                if st.button(f"№ {row['number']} · {order_service.remaining(row['deadline'])}", key=f"focus_{kind}_{row['id']}", use_container_width=True):
                    st.session_state.selected_order = row["id"]
                    set_page("Розпорядження")
                    st.rerun()


def render_month_chart(rows):
    import pandas as pd
    current_year = date.today().year
    data = monthly(rows, current_year)
    frame = pd.DataFrame(data)
    frame["Місяць"] = [MONTHS_UA[x - 1] for x in frame["month"]]
    frame = frame.set_index("Місяць")[["отримано", "виконано", "прострочено", "у_роботі"]]
    st.markdown(f'<div class="section-title">📈 Динаміка за {current_year} рік</div>', unsafe_allow_html=True)
    st.bar_chart(frame, height=330)


def order_card(row, compact: bool = False):
    state = status_class(row)
    tags = [x.strip() for x in str(row["tags"] or "").split(",") if x.strip()]
    badge_class = {"progress": "work", "today": "today", "overdue": "late", "done": "done"}[state]
    title = f"№ {html.escape(row['number'])}"
    if compact:
        st.markdown(f'<div class="order-card {state}"><div class="order-title">{title} <span class="badge {badge_class}">{status_label(row)}</span></div><div class="muted">{html.escape(str(row["description"])[:150])}</div></div>', unsafe_allow_html=True)
        return
    st.markdown(f'<div class="order-card {state}"><div class="order-title">{title} <span class="badge {badge_class}">{status_label(row)}</span> <span class="badge blue">{html.escape(row["priority"])}</span></div><div class="desc">{html.escape(row["description"])}</div><div class="muted">📅 {row["received_date"] or "дата не вказана"} → {row["deadline"]} · ⏱ {order_service.remaining(row["deadline"])} · 👤 {html.escape(row["responsible"] or "не призначено")} · 🗂 {html.escape(row["category"])}</div></div>', unsafe_allow_html=True)
    if tags:
        st.markdown(" ".join(f'<span class="tag">#{html.escape(x)}</span>' for x in tags), unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Відкрити", key=f"open_{row['id']}", use_container_width=True):
            st.session_state.selected_order = row["id"]
            st.rerun()
    with c2:
        if st.button("↩ Відповідь", key=f"resp_{row['id']}", use_container_width=True):
            st.session_state.selected_order = row["id"]
            st.session_state.response_open = True
            st.rerun()
    with c3:
        if state == "done":
            if st.button("↺ У роботу", key=f"reopen_{row['id']}", use_container_width=True):
                order_service.reopen(row["id"]); toast("Розпорядження повернуто в роботу"); st.rerun()
        else:
            if st.button("✓ Виконано", key=f"done_{row['id']}", use_container_width=True):
                order_service.mark_done(row["id"]); toast("Розпорядження позначено виконаним"); st.rerun()
    with c4:
        if st.button("🗑 Кошик", key=f"trash_{row['id']}", use_container_width=True):
            try:
                order_service.move_to_trash(row)
                toast("Розпорядження переміщено до кошика")
                st.rerun()
            except Exception as exc:
                st.error(f"Не вдалося перемістити: {exc}")


def add_form():
    st.markdown('<div class="section-title">＋ Нове розпорядження</div>', unsafe_allow_html=True)
    with st.form("add_order_form", clear_on_submit=True):
        c1, c2, c3 = st.columns([1.2, 1, 1])
        with c1:
            number = st.text_input("Номер розпорядження", placeholder="Наприклад: 1111/2026")
        with c2:
            received = st.date_input("Дата отримання", value=date.today())
        with c3:
            deadline = st.date_input("Виконати до", value=date.today())
        description = st.text_area("Короткий опис розпорядження", placeholder="Коротко опишіть, що саме необхідно виконати…", height=100)
        c1, c2, c3 = st.columns(3)
        with c1:
            priority = st.selectbox("Пріоритет", PRIORITIES, index=0)
        with c2:
            responsible = st.text_input("Відповідальний", placeholder="Підрозділ або прізвище")
        with c3:
            category = st.selectbox("Категорія", CATEGORIES, index=0)
        tags = st.text_input("Мітки", placeholder="Наприклад: термінове, контроль, навчання")
        upload = st.file_uploader("Файл розпорядження", type=None, help="Оберіть PDF, DOCX, XLSX, ZIP або інший файл")
        a, b = st.columns([1, 4])
        with a:
            submitted = st.form_submit_button("💾 ЗБЕРЕГТИ", use_container_width=True)
        if submitted:
            if upload is None:
                st.error("Додайте файл розпорядження.")
            elif deadline < received:
                st.error("Дата виконання не може бути раніше дати отримання.")
            else:
                try:
                    order_service.create(number=number, received=received, deadline=deadline, description=description, file_name=upload.name, file_bytes=upload.getvalue(), mime=upload.type or "", priority=priority, responsible=responsible, category=category, tags=tags)
                    play_added_sound(); toast("Розпорядження додано"); st.session_state.add_open = False; st.rerun()
                except Exception as exc:
                    st.error(str(exc))


def detail_view(order):
    st.markdown(f'<div class="detail-card"><div class="small-title">РОЗПОРЯДЖЕННЯ</div><h2>№ {html.escape(order["number"])}</h2><div class="desc">{html.escape(order["description"])}</div><div class="muted">Отримано: {order["received_date"] or "—"} · Виконати до: {order["deadline"]} · {status_label(order)} · {order_service.remaining(order["deadline"])}</div></div>', unsafe_allow_html=True)
    st.write("")
    top = st.columns(4)
    with top[0]:
        if st.button("← До списку", use_container_width=True):
            st.session_state.selected_order = None; st.rerun()
    with top[1]:
        if st.button("✎ Редагувати", use_container_width=True):
            st.session_state.edit_open = not st.session_state.edit_open
    with top[2]:
        if st.button("↩ Додати відповідь", use_container_width=True):
            st.session_state.response_open = not st.session_state.response_open
    with top[3]:
        if st.button("💾 Резервна копія", use_container_width=True):
            path = backup_service.create(True); st.success(f"Створено: {path.name}")
    if st.session_state.edit_open:
        with st.expander("✎ Редагування", expanded=True):
            with st.form(f"edit_{order['id']}"):
                c1, c2 = st.columns(2)
                with c1:
                    number = st.text_input("Номер розпорядження", value=order["number"])
                    deadline = st.date_input("Виконати до", value=date.fromisoformat(order["deadline"]))
                    priority = st.selectbox("Пріоритет", PRIORITIES, index=PRIORITIES.index(order["priority"]) if order["priority"] in PRIORITIES else 0)
                    category = st.selectbox("Категорія", CATEGORIES, index=CATEGORIES.index(order["category"]) if order["category"] in CATEGORIES else 0)
                with c2:
                    description = st.text_area("Короткий опис", value=order["description"], height=120)
                    responsible = st.text_input("Відповідальний", value=order["responsible"] or "")
                    tags = st.text_input("Мітки", value=order["tags"] or "")
                if st.form_submit_button("ЗБЕРЕГТИ ЗМІНИ", use_container_width=True):
                    try:
                        order_service.update(order["id"], number=number, deadline=deadline, description=description, priority=priority, responsible=responsible, category=category, tags=tags)
                        st.session_state.edit_open = False; toast("Зміни збережено"); st.rerun()
                    except Exception as exc:
                        st.error(str(exc))
    if st.session_state.response_open:
        with st.expander("↩ Нова відповідь", expanded=True):
            with st.form(f"response_{order['id']}"):
                c1, c2 = st.columns(2)
                with c1:
                    response_date = st.date_input("Дата відповіді", value=date.today())
                    outgoing = st.text_input("Вихідний номер", placeholder="Наприклад: 123/45-26")
                with c2:
                    final = st.checkbox("Вважати розпорядження виконаним")
                    comment = st.text_area("Короткий зміст відповіді", placeholder="Що було зроблено у відповідь на розпорядження…", height=90)
                upload = st.file_uploader("Файл або архів відповіді", type=None, key=f"response_upload_{order['id']}")
                if st.form_submit_button("ЗБЕРЕГТИ ВІДПОВІДЬ", use_container_width=True):
                    if upload is None:
                        st.error("Додайте файл відповіді або архів.")
                    else:
                        try:
                            order_service.add_response(order, response_date=response_date, outgoing=outgoing, comment=comment, file_name=upload.name, file_bytes=upload.getvalue(), mime=upload.type or "", final=final)
                            st.session_state.response_open = False; toast("Відповідь збережено"); st.rerun()
                        except Exception as exc:
                            st.error(str(exc))
    tabs = st.tabs(["📄 Документ", "↩ Відповіді", "🕒 Історія", "ℹ Реквізити"])
    with tabs[0]:
        p = storage.safe(order["path"])
        if p.exists():
            data = p.read_bytes(); mime = order["mime"] or mimetypes.guess_type(p.name)[0] or "application/octet-stream"
            st.download_button("⬇ Завантажити оригінал", data=data, file_name=p.name, mime=mime, key=f"doc_{order['id']}")
            if mime == "application/pdf" or p.suffix.lower() == ".pdf":
                encoded = base64.b64encode(data).decode(); st.markdown(f'<iframe src="data:application/pdf;base64,{encoded}" width="100%" height="720" style="border:1px solid #ffffff18;border-radius:12px"></iframe>', unsafe_allow_html=True)
            elif mime.startswith("image/"):
                st.image(data, use_container_width=True)
            else:
                st.info("Попередній перегляд для цього формату недоступний. Використайте кнопку завантаження.")
        else:
            st.error("Оригінальний файл не знайдено у локальному сховищі.")
    with tabs[1]:
        responses = db.get_responses(order["id"])
        if not responses:
            st.info("Відповідей ще немає.")
        for response in responses:
            with st.expander(f"{response['response_date']} · {response['outgoing'] or 'Без вихідного номера'} {'· ВИКОНАНО' if response['is_final'] else ''}", expanded=False):
                st.write(response["comment"] or "Без опису")
                rp = storage.safe(response["path"])
                if rp.exists():
                    st.download_button("⬇ Завантажити відповідь", data=rp.read_bytes(), file_name=rp.name, mime=response["mime"], key=f"response_file_{response['id']}")
    with tabs[2]:
        events = db.get_events(order["id"])
        if not events:
            st.info("Історія поки порожня.")
        for item in events:
            st.markdown(f'<div class="timeline-item"><b>{html.escape(item["event_type"])}</b><br><span class="muted">{item["created_at"]}</span><br>{html.escape(item["details"] or "")}</div>', unsafe_allow_html=True)
    with tabs[3]:
        st.json({"№": order["number"], "статус": status_label(order), "пріоритет": order["priority"], "категорія": order["category"], "відповідальний": order["responsible"], "мітки": order["tags"], "папка": order["folder"], "файл": order["filename"]})


def orders_page():
    if st.session_state.selected_order:
        order = db.get_order(st.session_state.selected_order)
        if order:
            detail_view(order)
            return
        st.session_state.selected_order = None
    st.markdown('<div class="section-title">📋 Реєстр розпоряджень</div>', unsafe_allow_html=True)
    if st.button("＋ ДОДАТИ РОЗПОРЯДЖЕННЯ", use_container_width=False):
        st.session_state.add_open = not st.session_state.add_open
    if st.session_state.add_open:
        with st.expander("Нове розпорядження", expanded=True):
            add_form()
    rows = db.get_orders()
    c1, c2, c3, c4 = st.columns([2.2, 1, 1, 1])
    with c1:
        query = st.text_input("Пошук", placeholder="Номер, вихідний номер, опис, відповідальний…", label_visibility="collapsed")
    with c2:
        status_filter = st.selectbox("Статус", ["Усі", "У РОБОТІ", "ТЕРМІН СЬОГОДНІ", "ПРОСТРОЧЕНО", "ВИКОНАНО"], label_visibility="collapsed")
    with c3:
        priority_filter = st.selectbox("Пріоритет", ["Усі"] + PRIORITIES, label_visibility="collapsed")
    with c4:
        category_filter = st.selectbox("Категорія", ["Усі"] + CATEGORIES, label_visibility="collapsed")
    filtered = []
    q = query.strip().lower()
    for row in rows:
        hay = f"{row['number']} {row['completion_outgoing']} {row['description']} {row['responsible']} {row['tags']}".lower()
        if q and q not in hay: continue
        if status_filter != "Усі" and status_label(row) != status_filter: continue
        if priority_filter != "Усі" and row["priority"] != priority_filter: continue
        if category_filter != "Усі" and row["category"] != category_filter: continue
        filtered.append(row)
    st.caption(f"Показано {len(filtered)} з {len(rows)} розпоряджень")
    for row in filtered:
        order_card(row, compact=st.session_state.compact)


def home_page(rows):
    render_metrics(rows)
    render_focus(rows)
    c1, c2 = st.columns([1.6, 1])
    with c1:
        render_month_chart(rows)
    with c2:
        st.markdown('<div class="section-title">🕒 Останні дії</div>', unsafe_allow_html=True)
        recent = db.fetchall("SELECT e.*,o.number FROM events e LEFT JOIN orders o ON o.id=e.order_id ORDER BY e.created_at DESC LIMIT 9")
        if not recent:
            st.caption("Поки немає подій")
        for item in recent:
            st.markdown(f'<div class="timeline-item"><b>№ {html.escape(str(item["number"] or "—"))}</b> · {html.escape(item["event_type"])}<br><span class="muted">{item["created_at"]}</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📌 Останні розпорядження</div>', unsafe_allow_html=True)
    for row in rows[:6]:
        order_card(row, compact=st.session_state.compact)


def calendar_page(rows):
    st.markdown('<div class="section-title">🗓 Календар дедлайнів</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: year = st.number_input("Рік", min_value=2020, max_value=2100, value=date.today().year, step=1)
    with c2: month = st.selectbox("Місяць", range(1, 13), index=date.today().month - 1, format_func=lambda x: MONTHS_UA[x - 1])
    first = date(year, month, 1); start_weekday = first.weekday(); total = monthrange(year, month)[1]
    cells = [None] * start_weekday + [date(year, month, day) for day in range(1, total + 1)]
    while len(cells) % 7: cells.append(None)
    head = st.columns(7)
    for col, wd in zip(head, WEEKDAYS_UA):
        col.markdown(f'<div class="small-title" style="text-align:center">{wd}</div>', unsafe_allow_html=True)
    for i in range(0, len(cells), 7):
        cols = st.columns(7)
        for col, day in zip(cols, cells[i:i+7]):
            with col:
                if day is None:
                    st.markdown('<div class="calendar-card empty">&nbsp;</div>', unsafe_allow_html=True); continue
                day_rows = []
                for row in rows:
                    try:
                        if date.fromisoformat(row["deadline"]) == day: day_rows.append(row)
                    except Exception: pass
                done = sum(order_service.status(r) == "done" for r in day_rows)
                late = sum(order_service.status(r) == "overdue" for r in day_rows)
                color = "red" if late else "green" if done and day_rows else ""
                st.markdown(f'<div class="calendar-card"><div class="calendar-day">{day.day}</div><div class="calendar-count {color}">{len(day_rows)}</div><div class="muted">{("виконано " + str(done)) if done else ""}</div></div>', unsafe_allow_html=True)
                if day_rows:
                    for row in day_rows[:3]:
                        if st.button(f"№ {row['number']}", key=f"cal_{day}_{row['id']}", use_container_width=True):
                            st.session_state.selected_order = row["id"]; set_page("Розпорядження"); st.rerun()


def analytics_page(rows):
    import pandas as pd
    st.markdown('<div class="section-title">📊 Розширена аналітика</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: year = st.number_input("Рік аналізу", min_value=2020, max_value=2100, value=date.today().year, step=1)
    with c2: month = st.selectbox("Місяць для деталізації", range(0, 13), format_func=lambda x: "Увесь рік" if x == 0 else MONTHS_UA[x - 1])
    m = metrics(rows)
    k = st.columns(4)
    for col, label, value in zip(k, ["Виконання", "Прострочення", "Навантаження", "Термінові"], [f"{m.completion_rate}%", f"{m.overdue_rate}%", f"{workload_index(rows)}", m.urgent]):
        with col:
            st.metric(label, value)
    frame = pd.DataFrame(monthly(rows, int(year)))
    frame["Місяць"] = [MONTHS_UA[x - 1] for x in frame["month"]]
    frame = frame.set_index("Місяць")[["отримано", "виконано", "прострочено", "у_роботі"]]
    st.markdown('<div class="section-title">Динаміка за місяцями</div>', unsafe_allow_html=True)
    st.bar_chart(frame, height=360)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">За категоріями</div>', unsafe_allow_html=True)
        st.bar_chart(pd.DataFrame.from_dict(distribution(rows, "category"), orient="index", columns=["Кількість"]))
    with c2:
        st.markdown('<div class="section-title">За пріоритетами</div>', unsafe_allow_html=True)
        st.bar_chart(pd.DataFrame.from_dict(distribution(rows, "priority"), orient="index", columns=["Кількість"]))
    st.markdown('<div class="section-title">👤 Відповідальні</div>', unsafe_allow_html=True)
    table = responsible_table(rows)
    if table: st.dataframe(pd.DataFrame(table), use_container_width=True, hide_index=True)
    else: st.info("Немає даних для аналізу.")
    if month:
        selected = [r for r in rows if str(r["received_date"]).startswith(f"{int(year):04d}-{int(month):02d}")]
        st.markdown(f'<div class="section-title">Розпорядження за {MONTHS_UA[month-1].lower()} {year}</div>', unsafe_allow_html=True)
        for row in selected: order_card(row, compact=True)


def reports_page(rows):
    st.markdown('<div class="section-title">📑 Звіти та експорт</div>', unsafe_allow_html=True)
    data = [dict(row) for row in rows]
    columns = [("№", "number"), ("Дата отримання", "received_date"), ("Термін", "deadline"), ("Статус", "status"), ("Пріоритет", "priority"), ("Відповідальний", "responsible"), ("Категорія", "category"), ("Вихідний №", "completion_outgoing")]
    c1, c2, c3 = st.columns(3)
    with c1: st.download_button("⬇ CSV", csv_bytes(data, columns), file_name=filename("Звіт", "csv"), mime="text/csv", use_container_width=True)
    with c2: st.download_button("⬇ Excel", xlsx_bytes(data, columns), file_name=filename("Звіт", "xlsx"), mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with c3: st.download_button("⬇ PDF", pdf_bytes(data, columns, "Звіт про виконання розпоряджень"), file_name=filename("Звіт", "pdf"), mime="application/pdf", use_container_width=True)
    st.dataframe(data, use_container_width=True, hide_index=True)
    st.markdown('<div class="section-title">💾 Резервні копії</div>', unsafe_allow_html=True)
    if st.button("СТВОРИТИ РЕЗЕРВНУ КОПІЮ", use_container_width=False):
        archive = backup_service.create(True); st.success(f"Резервну копію створено: {archive.name}")
    for backup in backup_service.list_backups()[:10]:
        st.write(f"📦 {backup.name}")
        st.download_button("Завантажити", backup.read_bytes(), file_name=backup.name, mime="application/zip", key=f"backup_{backup.name}")


def trash_page():
    st.markdown('<div class="section-title">🗑 Кошик</div>', unsafe_allow_html=True)
    items = db.get_trash()
    if not items:
        st.info("Кошик порожній.")
        return
    for item in items:
        with st.expander(f"№ {item['number']} · видалено {item['deleted_at']}"):
            path = storage.safe(item["trash_path"])
            st.caption(f"Папка: {item['folder']}")
            if path.exists():
                st.info("Файли зберігаються у кошику та можуть бути відновлені вручну після резервної копії. Повне відновлення бази виконується через backup.")
            else:
                st.warning("Файли кошика більше не знайдено.")
            if st.button("Видалити назавжди", key=f"purge_{item['id']}"):
                if path.exists():
                    import shutil; shutil.rmtree(path)
                db.remove_trash_record(item["id"]); st.rerun()


def settings_page():
    st.markdown('<div class="section-title">⚙ Налаштування та стан системи</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><b>Мова інтерфейсу</b></div>', unsafe_allow_html=True)
    language = st.selectbox("Мова інтерфейсу", ["Українська", "Російська"], label_visibility="collapsed")
    if language == "Російська":
        st.markdown("### Ти що москаль?")
        image = ROOT / "language-russian.jpg"
        if image.exists(): st.image(image, width=280)
    st.session_state.compact = st.checkbox("Компактний режим списків", value=st.session_state.compact)
    st.markdown('<div class="section-title">📁 Локальне сховище</div>', unsafe_allow_html=True)
    new_workspace = st.text_input("Папка даних", value=st.session_state.workspace, placeholder="Наприклад: D:/Дашборд")
    if st.button("ЗБЕРЕГТИ ПАПКУ ДАНИХ"):
        try:
            st.session_state.workspace = str(Path(new_workspace).expanduser().resolve())
            services.clear(); st.rerun()
        except Exception as exc: st.error(f"Не вдалося змінити папку: {exc}")
    inventory = storage.inventory()
    problems = storage.validate()
    cols = st.columns(4)
    for col, label, value in zip(cols, ["Файлів", "Папок", "Обсяг", "База"], [inventory["files"], inventory["folders"], f"{inventory['mb']} МБ", "OK" if paths.database.exists() else "ПОМИЛКА"]):
        with col: st.metric(label, value)
    if problems:
        for problem in problems: st.error(problem)
    else:
        st.success("Стан локального сховища: OK")
    st.caption("Програма не використовує зовнішні API для зберігання даних. Усі документи та база зберігаються у вибраній локальній папці.")
    if st.button("СТВОРИТИ РЕЗЕРВНУ КОПІЮ ЗАРАЗ"):
        archive = backup_service.create(True); st.success(f"Готово: {archive.name}")


def main():
    show_toast()
    render_header()
    rows = db.get_orders()
    page = st.session_state.page
    if page == "Головна": home_page(rows)
    elif page == "Розпорядження": orders_page()
    elif page == "Календар": calendar_page(rows)
    elif page == "Аналітика": analytics_page(rows)
    elif page == "Звіти": reports_page(rows)
    elif page == "Кошик": trash_page()
    else: settings_page()
    st.markdown(f'<div class="footer">{APP_TITLE} · {APP_VERSION} · ЛОКАЛЬНИЙ РЕЖИМ · {datetime.now():%d.%m.%Y %H:%M}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
