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
DEFAULTS = {"workspace": str(DEFAULT_WORKSPACE), "add_open": False, "response_order": None, "language": "Українська", "language_popup": False, "just_added": False, "viewer_order": None, "viewer_response": None, "delete_order": None}
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

CSS = '''<style>
html,body,[class*=css]{font-family:Inter,"Segoe UI",Arial,sans-serif}.stApp{background:radial-gradient(circle at 80% 10%,#263c2b 0,transparent 28%),linear-gradient(135deg,#050a06,#142118 50%,#050806);color:#edf2ec}.block-container{max-width:1480px;padding:1.5rem 3rem 3rem}.hero h1{font-family:"Segoe UI",Inter,Arial,sans-serif;font-style:normal;font-weight:800;font-size:clamp(2.1rem,4vw,3.7rem);letter-spacing:-.045em;margin:.2rem 0 .3rem}.eyebrow{color:#b8cba9;font-weight:800;font-size:.66rem;letter-spacing:.20em}.version{text-align:right;color:#8e9a91;font-size:.68rem;letter-spacing:.12em;font-weight:800}.panel,.order,.metric{background:rgba(8,18,12,.93);border:1px solid #dce9d91c;border-radius:16px;padding:1rem}.metric{min-height:90px}.order{margin:.75rem 0 .25rem;border-left:5px solid #d0ae62;box-shadow:0 10px 30px #0003}.order.overdue{border-left-color:#e36e68}.order.done{border-left-color:#79b88a}.order.today{border-left-color:#e3c15c}.desc{color:#c3cdc6;margin:.55rem 0;line-height:1.55}.muted{color:#8c9a90;font-size:.70rem;letter-spacing:.06em}.badge{padding:.28rem .58rem;border-radius:999px;font-size:.62rem;font-weight:850}.work{color:#d0ae62;background:#d0ae6218}.late{color:#e36e68;background:#e36e6818}.finished{color:#79b88a;background:#79b88a18}.todaybadge{color:#e3c15c;background:#e3c15c18}.stButton>button{border-radius:9px;background:#78925f20;border:1px solid #a9bc9140;color:#dce7d8;font-weight:800;min-height:42px}.stButton>button:hover{border-color:#d0ae62aa;background:#d0ae6215}.successbox{padding:18px;border:1px solid #9ab58a55;border-radius:14px;background:#263d2a;margin:.5rem 0 1rem}.stTextInput input,.stTextArea textarea,.stDateInput input{background:#0005!important;color:#fff!important}
</style>'''
st.markdown(CSS, unsafe_allow_html=True)

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,number TEXT NOT NULL,deadline TEXT NOT NULL,description TEXT NOT NULL,folder TEXT NOT NULL,filename TEXT NOT NULL,path TEXT NOT NULL,mime TEXT NOT NULL,status TEXT DEFAULT 'progress',completion_outgoing TEXT DEFAULT '',created_at TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS responses(id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER NOT NULL,response_date TEXT NOT NULL,outgoing TEXT DEFAULT '',comment TEXT DEFAULT '',filename TEXT NOT NULL,path TEXT NOT NULL,mime TEXT NOT NULL,is_final INTEGER DEFAULT 0,created_at TEXT NOT NULL)")
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

def order_state(row):
    if row['status'] == 'done': return 'done'
    try:
        d = date.fromisoformat(row['deadline'])
        if d < date.today(): return 'overdue'
        if d == date.today(): return 'today'
    except Exception: pass
    return 'progress'

def days_text(deadline):
    try:
        delta = (date.fromisoformat(deadline) - date.today()).days
        if delta < 0: return f"ПРОСТРОЧЕНО НА {abs(delta)} ДНІВ"
        if delta == 0: return "ТЕРМІН СЬОГОДНІ"
        if delta == 1: return "ЗАЛИШИВСЯ 1 ДЕНЬ"
        return f"ЗАЛИШИЛОСЯ {delta} ДНІВ"
    except Exception: return ""

def add_order(number, deadline, description, upload):
    folder = ORDERS / safe_name(number)
    counter = 2
    while folder.exists():
        folder = ORDERS / f"{safe_name(number)}_{counter}"
        counter += 1
    p = save_upload(upload, folder)
    c = db()
    c.execute('INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,created_at) VALUES(?,?,?,?,?,?,?,?,?)', (number.strip(), deadline.isoformat(), description.strip(), folder.name, p.name, str(p.relative_to(WORK)), upload.type or mimetypes.guess_type(p.name)[0] or 'application/octet-stream', 'progress', datetime.now().isoformat()))
    c.commit(); c.close()

def add_response(row, response_date, outgoing, comment, upload, final):
    folder = ORDERS / row['folder'] / 'Відповіді'
    p = save_upload(upload, folder)
    c = db()
    c.execute('INSERT INTO responses(order_id,response_date,outgoing,comment,filename,path,mime,is_final,created_at) VALUES(?,?,?,?,?,?,?,?,?)', (row['id'], response_date.isoformat(), outgoing.strip(), comment.strip(), p.name, str(p.relative_to(WORK)), upload.type or mimetypes.guess_type(p.name)[0] or 'application/octet-stream', int(final), datetime.now().isoformat()))
    if final:
        c.execute("UPDATE orders SET status='done',completion_outgoing=? WHERE id=?", (outgoing.strip(), row['id']))
    c.commit(); c.close()

def get_responses(order_id):
    c = db(); rows = c.execute('SELECT * FROM responses WHERE order_id=? ORDER BY response_date DESC,id DESC', (order_id,)).fetchall(); c.close(); return rows

def delete_order(order_id):
    c = db(); row = c.execute('SELECT folder FROM orders WHERE id=?', (order_id,)).fetchone()
    if not row:
        c.close(); return False
    folder = (ORDERS / row['folder']).resolve()
    try: folder.relative_to(ORDERS.resolve())
    except ValueError:
        c.close(); raise RuntimeError('Небезпечний шлях папки розпорядження')
    c.execute('DELETE FROM responses WHERE order_id=?', (order_id,)); c.execute('DELETE FROM orders WHERE id=?', (order_id,)); c.commit(); c.close()
    if folder.exists(): shutil.rmtree(folder)
    return True

def make_backup():
    target = BACKUPS / f"Резервна_копія_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    target.mkdir(parents=True, exist_ok=True)
    if DB.exists(): shutil.copy2(DB, target / 'database.db')
    if ORDERS.exists(): shutil.copytree(ORDERS, target / 'Розпорядження', dirs_exist_ok=True)
    return target

def local_path(rel):
    p = (WORK / rel).resolve()
    try: p.relative_to(WORK.resolve())
    except ValueError: return None
    return p if p.exists() else None

def show_file_viewer(row, response=False):
    p = local_path(row['path'])
    if not p:
        st.error('Файл не знайдено у папці даних.'); return
    mime = row['mime'] or mimetypes.guess_type(p.name)[0] or 'application/octet-stream'; data = p.read_bytes()
    st.markdown(f"**{html.escape(p.name)}** · `{mime}`")
    st.download_button('⬇ ЗАВАНТАЖИТИ ФАЙЛ', data=data, file_name=p.name, mime=mime, key=f"download_{'r' if response else 'o'}_{row['id']}")
    if mime == 'application/pdf' or p.suffix.lower() == '.pdf':
        b64 = base64.b64encode(data).decode(); st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="760" style="border:1px solid #ffffff18;border-radius:12px"></iframe>', unsafe_allow_html=True)
    elif mime.startswith('image/'):
        st.image(data, use_container_width=True)
    elif mime.startswith('text/') or p.suffix.lower() in {'.txt','.csv','.log','.md'}:
        st.code(data.decode('utf-8', errors='replace'), language='text')
    else:
        st.info('Для цього формату використовуйте «Завантажити файл» або відкрийте його у програмі ОС.')
        if st.button('🖥 ВІДКРИТИ У ПРОГРАМІ ОС', key=f"os_{'r' if response else 'o'}_{row['id']}"):
            try:
                if sys.platform.startswith('win'): os.startfile(str(p))
                elif sys.platform == 'darwin': subprocess.Popen(['open', str(p)])
                else: subprocess.Popen(['xdg-open', str(p)])
            except Exception as exc: st.error(f'Не вдалося відкрити файл: {exc}')

def play_add_sound():
    audio_file = APP / 'sounds' / 'opiat-rabota.mp3'
    if not audio_file.exists(): return
    b64 = base64.b64encode(audio_file.read_bytes()).decode()
    st.markdown(f'<audio autoplay controls style="display:none"><source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg"></audio>', unsafe_allow_html=True)

# Initialize database and a single demo order only when database is empty.
c = db()
if c.execute('SELECT COUNT(*) FROM orders').fetchone()[0] == 0:
    folder = ORDERS / '01-2026'; folder.mkdir(exist_ok=True)
    p = folder / 'Розпорядження_01-2026.txt'
    p.write_text('ДЕМОНСТРАЦІЙНЕ РОЗПОРЯДЖЕННЯ\n\nПідготувати та надати узагальнену інформацію про стан виконання визначених завдань.', encoding='utf-8')
    c.execute('INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,created_at) VALUES(?,?,?,?,?,?,?,?,?)', ('01/2026','2026-10-05','Підготувати та надати узагальнену інформацію про стан виконання визначених завдань.',folder.name,p.name,str(p.relative_to(WORK)),'text/plain','progress',datetime.now().isoformat())); c.commit()
c.close()

left, right = st.columns([4,1])
with left:
    lang = st.selectbox('Мова інтерфейсу', ['Українська','Російська'], index=0 if st.session_state.language == 'Українська' else 1, label_visibility='collapsed')
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.session_state.language_popup = (lang == 'Російська')
        st.rerun()
    st.markdown(f'<div class="muted">Мова інтерфейсу — <b>{html.escape(lang)}</b></div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="version">ВЕРСІЯ 1.2</div>', unsafe_allow_html=True)

if st.session_state.language_popup and st.session_state.language == 'Російська':
    img = APP / 'language-russian.jpg'
    if img.exists():
        b64 = base64.b64encode(img.read_bytes()).decode()
        st.markdown(f'<div style="text-align:center;background:#050807;border:1px solid #d0ae6266;border-radius:18px;padding:16px;margin:.5rem 0 1rem"><div style="font-size:30px;font-weight:900;color:#f1df8d;margin-bottom:12px">Ти що москать?</div><img src="data:image/jpeg;base64,{b64}" style="width:min(760px,100%);border-radius:12px;display:block;margin:auto"></div>', unsafe_allow_html=True)
        time.sleep(3.5)
        st.session_state.language_popup = False
        st.rerun()
    else:
        st.warning('Файл language-russian.jpg не знайдено у папці програми.')
        st.session_state.language_popup = False

st.markdown('<div class="eyebrow">ЗБРОЙНІ СИЛИ УКРАЇНИ</div><div class="hero"><h1>Процес виконання розпоряджень</h1><p class="muted">Контроль термінів, документів та відповідей у єдиному робочому просторі.</p></div>', unsafe_allow_html=True)

if st.button('＋ ДОДАТИ РОЗПОРЯДЖЕННЯ'):
    st.session_state.add_open = not st.session_state.add_open; st.rerun()
if st.session_state.add_open:
    with st.form('new'):
        a, b = st.columns(2)
        with a:
            n = st.text_input('№ розпорядження'); d = st.date_input('Дата, до якої потрібно виконати', value=date.today())
        with b:
            desc = st.text_area('Короткий опис розпорядження', height=120); f = st.file_uploader('Файл розпорядження')
        x, y = st.columns(2)
        with x: save = st.form_submit_button('ЗБЕРЕГТИ РОЗПОРЯДЖЕННЯ')
        with y: cancel = st.form_submit_button('СКАСУВАТИ')
        if cancel: st.session_state.add_open = False; st.rerun()
        if save:
            if not n or not desc or not f: st.error('Заповніть №, короткий опис та додайте файл.')
            else: add_order(n,d,desc,f); st.session_state.add_open=False; st.session_state.just_added=True; st.rerun()
if st.session_state.pop('just_added', False):
    st.markdown('<div class="successbox"><b>РОЗПОРЯДЖЕННЯ ДОДАНО</b><br><span class="muted">Опять работа? 😄</span></div>', unsafe_allow_html=True); play_add_sound()

c = db(); rows = c.execute('SELECT * FROM orders ORDER BY deadline').fetchall(); c.close()
counts = {'progress':0,'today':0,'overdue':0,'done':0}
for r in rows: counts[order_state(r)] += 1
for col,label,val in zip(st.columns(4), ['УСЬОГО','У РОБОТІ','ТЕРМІН СЬОГОДНІ / ПРОСТРОЧЕНО','ВИКОНАНО'], [len(rows),counts['progress'],counts['today']+counts['overdue'],counts['done']]):
    with col: st.markdown(f'<div class="metric"><div class="muted">{label}</div><b style="font-size:1.8rem">{val}</b></div>', unsafe_allow_html=True)

q = st.text_input('🔎 Пошук за №, вихідним номером, описом або назвою файлу', placeholder='Введіть текст...')
filt = st.radio('ФІЛЬТР', ['Усі','У роботі','Термін сьогодні','Прострочені','Виконані'], horizontal=True)

for r in rows:
    s = order_state(r)
    responses = get_responses(r['id'])
    outs = ' '.join(x['outgoing'] for x in responses)
    hay = f'{r["number"]} {r["description"]} {r["filename"]} {outs}'.lower()
    if q.lower() not in hay: continue
    if filt == 'У роботі' and s != 'progress': continue
    if filt == 'Термін сьогодні' and s != 'today': continue
    if filt == 'Прострочені' and s != 'overdue': continue
    if filt == 'Виконані' and s != 'done': continue
    cls = 'overdue' if s == 'overdue' else ('done' if s == 'done' else ('today' if s == 'today' else ''))
    badge = 'late' if s == 'overdue' else ('finished' if s == 'done' else ('todaybadge' if s == 'today' else 'work'))
    label = {'overdue':'ПРОСТРОЧЕНО','done':'ВИКОНАНО','today':'ТЕРМІН СЬОГОДНІ','progress':'У РОБОТІ'}[s]
    st.markdown(f'<div class="order {cls}"><b>№ {html.escape(r["number"])}</b> <span class="badge {badge}">{label}</span><div class="desc">{html.escape(r["description"])}</div><div class="muted">ТЕРМІН: {r["deadline"]} · {days_text(r["deadline"])}</div></div>', unsafe_allow_html=True)
    a,b,c3,dcol = st.columns(4)
    with a:
        if st.button('📄 ПЕРЕГЛЯНУТИ', key=f'open{r["id"]}'): st.session_state.viewer_order = r['id']; st.rerun()
    with b:
        if st.button('↩ ДОДАТИ ВІДПОВІДЬ', key=f'res{r["id"]}'): st.session_state.response_order = r['id']; st.rerun()
    with c3:
        if s != 'done' and st.button('✓ ВИКОНАНО', key=f'done{r["id"]}'): st.session_state.response_order = r['id']; st.session_state.final_response = True; st.rerun()
    with dcol:
        if st.button('🗑 ВИДАЛИТИ', key=f'del{r["id"]}'): st.session_state.delete_order = r['id']; st.rerun()

    if st.session_state.delete_order == r['id']:
        st.warning(f'Видалити розпорядження № {r["number"]} разом із файлом та всіма відповідями?')
        y,nc = st.columns(2)
        with y:
            if st.button('ТАК, ВИДАЛИТИ', key=f'yes{r["id"]}'):
                delete_order(r['id']); st.session_state.delete_order = None; st.rerun()
        with nc:
            if st.button('СКАСУВАТИ', key=f'no{r["id"]}'):
                st.session_state.delete_order = None; st.rerun()

    if st.session_state.viewer_order == r['id']:
        st.markdown('<div class="panel"><b>ПЕРЕГЛЯД ДОКУМЕНТА</b></div>', unsafe_allow_html=True)
        show_file_viewer(r)
        if st.button('ЗАКРИТИ ПЕРЕГЛЯД', key=f'close{r["id"]}'): st.session_state.viewer_order = None; st.rerun()
        if responses:
            st.markdown('<div class="panel"><b>ВІДПОВІДІ НА ЦЕ РОЗПОРЯДЖЕННЯ</b></div>', unsafe_allow_html=True)
            for resp in responses:
                st.markdown(f'<div class="order"><b>Вих. № {html.escape(resp["outgoing"] or "—")}</b><div class="desc">{html.escape(resp["comment"] or "Без опису")}</div><div class="muted">ДАТА: {resp["response_date"]}</div></div>', unsafe_allow_html=True)
                if st.button(f'📎 ПЕРЕГЛЯНУТИ ВІДПОВІДЬ · {resp["filename"]}', key=f'vr{resp["id"]}'):
                    st.session_state.viewer_response = resp['id']; st.rerun()
                if st.session_state.viewer_response == resp['id']:
                    show_file_viewer(resp, response=True)

    if st.session_state.response_order == r['id']:
        st.markdown('<div class="panel"><b>ВІДПОВІДЬ НА РОЗПОРЯДЖЕННЯ</b></div>', unsafe_allow_html=True)
        with st.form(f'form{r["id"]}'):
            d = st.date_input('Дата відповіді', value=date.today(), key=f'date{r["id"]}')
            out = st.text_input('Вихідний номер відповіді', key=f'out{r["id"]}')
            comment = st.text_area('Короткий зміст відповіді', key=f'com{r["id"]}')
            rf = st.file_uploader('Файл відповіді / архів', key=f'file{r["id"]}')
            final = st.checkbox('Позначити розпорядження виконаним', value=st.session_state.pop('final_response', False), key=f'fin{r["id"]}')
            ok = st.form_submit_button('ЗБЕРЕГТИ ВІДПОВІДЬ')
            if ok:
                if not rf: st.error('Додайте файл відповіді або архів.')
                else: add_response(r,d,out,comment,rf,final); st.session_state.response_order=None; st.rerun()

st.markdown('<div class="muted" style="text-align:center;margin-top:3rem">СИСТЕМА КОНТРОЛЮ ВИКОНАННЯ • ЛОКАЛЬНИЙ РЕЖИМ • ВЕРСІЯ 1.2</div>', unsafe_allow_html=True)
