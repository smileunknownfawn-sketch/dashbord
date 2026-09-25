from datetime import date
from pathlib import Path
import sqlite3
import streamlit as st

try:
    import dashboard_engine as engine
except Exception:
    engine = None

st.set_page_config(page_title="Розширена аналітика", page_icon="📊", layout="wide")

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "data"
DB = WORK / "database.db"

st.markdown("""
<style>
.stApp{background:radial-gradient(circle at 15% 10%,#21372844,transparent 28%),linear-gradient(135deg,#030705,#09150e 55%,#030504);color:#eef5ef}
.block-container{max-width:1550px;padding:1.4rem 2.4rem 4rem}
.hero{border:1px solid #ffffff12;background:#0a130ef0;border-radius:24px;padding:1.4rem 1.6rem;box-shadow:0 20px 60px #0007}
.card{border:1px solid #ffffff12;background:#0b160ff2;border-radius:18px;padding:1rem;min-height:105px}
.big{font-size:2.2rem;font-weight:900}.muted{color:#98a79b;font-size:.78rem}.gold{color:#d8bb70}.red{color:#ef7770}.green{color:#7bcf97}.yellow{color:#e6cc70}
</style>
""", unsafe_allow_html=True)


def connect():
    if not DB.exists():
        return None
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def rows():
    c = connect()
    if not c:
        return []
    data = c.execute("SELECT * FROM orders ORDER BY deadline ASC,id DESC").fetchall()
    c.close()
    return data


def as_dict(r):
    return dict(r)


def d(v):
    try:
        return date.fromisoformat(str(v)[:10])
    except Exception:
        return None


def status(r):
    if r.get("status") == "done":
        return "Виконано"
    deadline = d(r.get("deadline"))
    if deadline and deadline < date.today():
        return "Прострочено"
    if deadline == date.today():
        return "Сьогодні"
    return "У роботі"


items = [as_dict(r) for r in rows()]
st.markdown('<div class="hero"><div class="muted">ПРОЦЕС ВИКОНАННЯ РОЗПОРЯДЖЕНЬ · V3</div><h1>📊 Розширена аналітика</h1><div class="muted">Локальні розрахунки без мережевих запитів</div></div>', unsafe_allow_html=True)
st.write("")

col1, col2, col3, col4 = st.columns(4)
total = len(items)
done = sum(status(r) == "Виконано" for r in items)
over = sum(status(r) == "Прострочено" for r in items)
today = sum(status(r) == "Сьогодні" for r in items)
with col1: st.markdown(f'<div class="card"><div class="muted">УСЬОГО</div><div class="big">{total}</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="card"><div class="muted">ВИКОНАНО</div><div class="big green">{done}</div></div>', unsafe_allow_html=True)
with col3: st.markdown(f'<div class="card"><div class="muted">ПРОСТРОЧЕНО</div><div class="big red">{over}</div></div>', unsafe_allow_html=True)
with col4: st.markdown(f'<div class="card"><div class="muted">ТЕРМІН СЬОГОДНІ</div><div class="big yellow">{today}</div></div>', unsafe_allow_html=True)

st.markdown("### 🎛️ Період аналізу")
period = st.radio("Режим", ["Рік", "Місяць", "Власний період"], horizontal=True, label_visibility="collapsed")
year = st.number_input("Рік", min_value=2020, max_value=2100, value=date.today().year, step=1)
month = st.selectbox("Місяць", list(range(1, 13)), index=date.today().month - 1, format_func=lambda x: date(2000, x, 1).strftime("%B"))

filtered = items
if period == "Рік":
    filtered = [r for r in items if (d(r.get("received_date")) or d(r.get("created_at"))) and (d(r.get("received_date")) or d(r.get("created_at"))).year == year]
elif period == "Місяць":
    filtered = [r for r in items if (d(r.get("received_date")) or d(r.get("created_at"))) and (d(r.get("received_date")) or d(r.get("created_at"))).year == year and (d(r.get("received_date")) or d(r.get("created_at"))).month == month]
else:
    c1, c2 = st.columns(2)
    start = c1.date_input("Початок", date(year, 1, 1))
    end = c2.date_input("Кінець", date(year, 12, 31))
    filtered = [r for r in items if (d(r.get("received_date")) or d(r.get("created_at"))) and start <= (d(r.get("received_date")) or d(r.get("created_at"))) <= end]

if engine:
    snapshot = engine.dashboard_snapshot(filtered)
    st.caption(f"Індекс навантаження: **{snapshot['workload']}** · SLA: **{snapshot['sla_rate']}%** · Виконання: **{snapshot['completion_rate']}%**")

st.markdown("### 📈 Порівняння по місяцях")
monthly = {i: {"Отримано": 0, "Виконано": 0, "Прострочено": 0} for i in range(1, 13)}
for r in items:
    dt = d(r.get("received_date")) or d(r.get("created_at"))
    if not dt or dt.year != year:
        continue
    monthly[dt.month]["Отримано"] += 1
    if status(r) == "Виконано":
        monthly[dt.month]["Виконано"] += 1
    elif status(r) == "Прострочено":
        monthly[dt.month]["Прострочено"] += 1

import pandas as pd
chart = pd.DataFrame.from_dict(monthly, orient="index")
chart.index = [f"{i:02d}" for i in chart.index]
st.line_chart(chart)

left, right = st.columns(2)
with left:
    st.markdown("### 🎯 За пріоритетом")
    priorities = {"Звичайний": 0, "Важливий": 0, "Терміновий": 0, "Критичний": 0}
    for r in filtered:
        priorities[r.get("priority", "Звичайний")] = priorities.get(r.get("priority", "Звичайний"), 0) + 1
    st.bar_chart(priorities)
with right:
    st.markdown("### 🗂️ За категоріями")
    categories = {}
    for r in filtered:
        key = r.get("category", "Інше") or "Інше"
        categories[key] = categories.get(key, 0) + 1
    st.bar_chart(categories)

with st.expander("👤 Навантаження по відповідальних", expanded=True):
    responsible = {}
    for r in filtered:
        key = r.get("responsible", "Не призначено") or "Не призначено"
        responsible.setdefault(key, {"Усього": 0, "Виконано": 0, "Прострочено": 0})
        responsible[key]["Усього"] += 1
        responsible[key]["Виконано"] += status(r) == "Виконано"
        responsible[key]["Прострочено"] += status(r) == "Прострочено"
    if responsible:
        st.dataframe(pd.DataFrame.from_dict(responsible, orient="index"), use_container_width=True)
    else:
        st.info("Немає даних за обраний період.")

with st.expander("📎 Документне навантаження"):
    response_count = 0
    event_count = 0
    c = connect()
    if c:
        ids = [r["id"] for r in filtered]
        if ids:
            marks = ",".join("?" for _ in ids)
            response_count = c.execute(f"SELECT COUNT(*) FROM responses WHERE order_id IN ({marks})", ids).fetchone()[0]
            event_count = c.execute(f"SELECT COUNT(*) FROM events WHERE order_id IN ({marks})", ids).fetchone()[0]
        c.close()
    a, b = st.columns(2)
    a.metric("Відповідей", response_count)
    b.metric("Подій в історії", event_count)

with st.expander("🧮 Розрахункові показники"):
    if engine:
        st.write({
            "Середній час виконання, днів": engine.average_completion_days(filtered),
            "SLA, %": engine.sla_rate(filtered),
            "Покриття відповідями, %": engine.response_statistics(filtered)["coverage"],
            "Індекс навантаження": engine.workload_index(filtered),
        })
    st.caption("Показники обчислюються локально з поточної SQLite-бази.")
