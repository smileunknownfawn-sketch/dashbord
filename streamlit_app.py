from __future__ import annotations
import base64, html, mimetypes, os, shutil, sqlite3, subprocess, sys
from datetime import date, datetime
from pathlib import Path
import streamlit as st
try:
    from docx import Document
except Exception:
    Document = None

APP=Path(__file__).resolve().parent
st.set_page_config(page_title='Контроль виконання розпоряджень',page_icon='🇺🇦',layout='wide')
if 'workspace' not in st.session_state: st.session_state.workspace=str(APP/'data')
if 'lang' not in st.session_state: st.session_state.lang='Українська'
WORK=Path(st.session_state.workspace).expanduser(); WORK.mkdir(parents=True,exist_ok=True)
ORDERS=WORK/'Розпорядження'; BACKUP=WORK/'Backup'; ORDERS.mkdir(exist_ok=True); BACKUP.mkdir(exist_ok=True); DB=WORK/'database.db'

def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON')
    c.execute('''CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,number TEXT NOT NULL,outgoing TEXT DEFAULT '',deadline TEXT NOT NULL,description TEXT NOT NULL,folder TEXT NOT NULL,filename TEXT NOT NULL,path TEXT NOT NULL,mime TEXT NOT NULL,status TEXT DEFAULT 'progress',completed_at TEXT DEFAULT '',completion_outgoing TEXT DEFAULT '',completion_comment TEXT DEFAULT '',created_at TEXT NOT NULL,updated_at TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS responses(id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER NOT NULL,response_date TEXT NOT NULL,outgoing TEXT DEFAULT '',comment TEXT DEFAULT '',filename TEXT NOT NULL,path TEXT NOT NULL,mime TEXT NOT NULL,is_final INTEGER DEFAULT 0,created_at TEXT NOT NULL,FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE)''')
    cols={x['name'] for x in c.execute('PRAGMA table_info(orders)').fetchall()}
    if 'outgoing' not in cols: c.execute("ALTER TABLE orders ADD COLUMN outgoing TEXT DEFAULT ''")
    if 'outgoing_number' in cols: c.execute("UPDATE orders SET outgoing=COALESCE(NULLIF(outgoing,''),outgoing_number)")
    for col in ['completed_at','completion_outgoing','completion_comment','updated_at']:
        if col not in cols: c.execute(f"ALTER TABLE orders ADD COLUMN {col} TEXT DEFAULT ''")
    c.commit(); return c

def seed():
    c=conn()
    if c.execute('SELECT COUNT(*) FROM orders').fetchone()[0]==0:
        folder=ORDERS/'01-2026'; folder.mkdir(parents=True,exist_ok=True); f=folder/'Розпорядження_01-2026.txt'
        f.write_text('ЗБРОЙНІ СИЛИ УКРАЇНИ\n\nНАВЧАЛЬНИЙ ПРИКЛАД\n№ 01/2026\n\nПідготувати та надати узагальнену інформацію про стан виконання визначених завдань.\n\nЦе демонстраційний документ.',encoding='utf-8')
        now=datetime.now().isoformat(timespec='seconds'); c.execute('INSERT INTO orders(number,outgoing,deadline,description,folder,filename,path,mime,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)',('01/2026','','2026-10-05','Підготувати та надати узагальнену інформацію про стан виконання визначених завдань.',folder.name,f.name,str(f.relative_to(WORK)),'text/plain','progress',now,now)); c.commit()
    c.close()

def orders():
    c=conn(); r=c.execute('SELECT * FROM orders ORDER BY deadline ASC,id DESC').fetchall(); c.close(); return r
def replies(order_id):
    c=conn(); r=c.execute('SELECT * FROM responses WHERE order_id=? ORDER BY response_date DESC,id DESC',(order_id,)).fetchall(); c.close(); return r
def stat(r):
    if r['status']=='done': return 'done'
    try: return 'overdue' if (date.fromisoformat(r['deadline'])-date.today()).days<0 else 'progress'
    except Exception: return 'progress'
def days(r):
    try: return (date.fromisoformat(r['deadline'])-date.today()).days
    except Exception: return 99999
def safe(s): return ''.join(ch if ch.isalnum() or ch in ' ._-()[]' else '_' for ch in str(s)).strip() or 'Документ'
def mime_of(p): return mimetypes.guess_type(str(p))[0] or 'application/octet-stream'
def unique_folder(number):
    p=ORDERS/safe(number); i=2
    while p.exists(): p=ORDERS/f'{safe(number)}_{i}'; i+=1
    return p
def copy_upload(upload,folder):
    folder.mkdir(parents=True,exist_ok=True); target=folder/safe(upload.name); stem,suf=target.stem,target.suffix; i=2
    while target.exists(): target=folder/f'{stem}_{i}{suf}'; i+=1
    target.write_bytes(upload.getvalue()); return target
def add_order(n,o,d,desc,f):
    folder=unique_folder(n); src=copy_upload(f,folder); now=datetime.now().isoformat(timespec='seconds'); c=conn(); c.execute('INSERT INTO orders(number,outgoing,deadline,description,folder,filename,path,mime,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(n.strip(),o.strip(),d.isoformat(),desc.strip(),folder.name,src.name,str(src.relative_to(WORK)),f.type or mime_of(src),'progress',now,now)); c.commit(); c.close()
def edit_order(r,n,o,d,desc):
    c=conn(); c.execute('UPDATE orders SET number=?,outgoing=?,deadline=?,description=?,updated_at=? WHERE id=?',(n.strip(),o.strip(),d.isoformat(),desc.strip(),datetime.now().isoformat(timespec='seconds'),r['id'])); c.commit(); c.close()
def complete(r,o,comment):
    now=datetime.now().isoformat(timespec='seconds'); c=conn(); c.execute("UPDATE orders SET status='done',completed_at=?,completion_outgoing=?,completion_comment=?,updated_at=? WHERE id=?",(now,o.strip(),comment.strip(),now,r['id'])); c.commit(); c.close()
def reopen(r):
    c=conn(); c.execute("UPDATE orders SET status='progress',completed_at='',completion_outgoing='',completion_comment='',updated_at=? WHERE id=?",(datetime.now().isoformat(timespec='seconds'),r['id'])); c.commit(); c.close()
def add_reply(r,d,o,comment,f,final):
    folder=ORDERS/r['folder']/'Відповіді'; src=copy_upload(f,folder); c=conn(); c.execute('INSERT INTO responses(order_id,response_date,outgoing,comment,filename,path,mime,is_final,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(r['id'],d.isoformat(),o.strip(),comment.strip(),src.name,str(src.relative_to(WORK)),f.type or mime_of(src),int(final),datetime.now().isoformat(timespec='seconds'))); c.commit(); c.close()
    if final: complete(r,o,comment)
def resolve_path(rel):
    p=Path(rel); return p if p.is_absolute() else WORK/p
def open_local(p):
    try:
        p=Path(p).resolve()
        if not p.exists(): st.error(f'Файл або папку не знайдено: {p}'); return
        if sys.platform.startswith('win'): os.startfile(str(p))
        elif sys.platform=='darwin': subprocess.Popen(['open',str(p)])
        else: subprocess.Popen(['xdg-open',str(p)])
    except Exception as e: st.error(f'Не вдалося відкрити: {e}')
def preview(p,mime,key):
    p=Path(p)
    if not p.exists(): st.error('Файл документа не знайдено. Перевірте робочу папку.'); return
    raw=p.read_bytes()
    if mime=='application/pdf' or p.suffix.lower()=='.pdf':
        b64=base64.b64encode(raw).decode(); st.components.v1.html(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="620" style="border:0;border-radius:8px"></iframe>',height=640)
    elif mime.startswith('image/'): st.image(raw,use_container_width=True)
    elif p.suffix.lower()=='.txt': st.code(raw.decode('utf-8',errors='replace'),language='text')
    elif p.suffix.lower()=='.docx' and Document:
        text='\n\n'.join(x.text for x in Document(p).paragraphs if x.text.strip()); st.markdown(f'<div class="doc">{html.escape(text).replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
    else: st.info('Для цього формату доступне відкриття оригінального файла.')
    st.download_button('⬇ Завантажити оригінал',raw,file_name=p.name,mime=mime,key=key)
def russian_joke():
    st.markdown('''<div class="ru-overlay"><div class="ru-title">Ти що, москаль? 😄</div><svg viewBox="0 0 720 300" class="ship-svg"><rect width="720" height="300" fill="#071016"/><circle cx="590" cy="58" r="30" fill="#d6d8b6"/><path d="M0 215 Q120 185 240 215 T480 215 T720 215 V300 H0Z" fill="#173447"/><path d="M120 185 L565 185 L625 215 L90 215Z" fill="#555a57"/><rect x="245" y="135" width="190" height="50" rx="4" fill="#69706a"/><rect x="315" y="108" width="45" height="27" fill="#737b73"/><path d="M337 108 V65" stroke="#a7afa6" stroke-width="5"/><path d="M337 70 L430 92 L337 98Z" fill="#d9d5bc"/><text x="360" y="80" fill="#171717" font-size="13" font-family="Arial">RU</text><text x="360" y="265" text-anchor="middle" fill="#f2f0df" font-size="28" font-family="Arial" font-weight="700">РУСЬКИЙ ВОЄННИЙ КОРАБЕЛЬ — ІДИ НА ЙУХ</text></svg></div>''',unsafe_allow_html=True)
    st.components.v1.html('<script>setTimeout(function(){window.parent.document.querySelectorAll(".ru-overlay").forEach(function(e){e.style.display="none"})},3500);</script>',height=1)

seed()
st.markdown('''<style>
.stApp{background:radial-gradient(circle at 20% 15%,#2b3b2a 0,#0a110c 42%,#050806 100%);color:#edf2ec}.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.12;background-image:repeating-linear-gradient(35deg,#a9bc91 0 1px,transparent 1px 45px),repeating-linear-gradient(-35deg,#64755d 0 1px,transparent 1px 70px)}.block-container{max-width:1500px;padding:2rem 3rem;position:relative}.brand{border-bottom:1px solid #ffffff1c;padding-bottom:1.2rem;margin-bottom:1.7rem;display:flex;justify-content:space-between}.eyebrow,.kicker{font-size:.64rem;font-weight:800;letter-spacing:.2em;color:#a9bc91}.title{font-size:1.2rem;font-weight:800;letter-spacing:.08em}.title span,.hero em{color:#b7c7a6}.hero h1{font-size:clamp(2rem,4vw,3.4rem);margin:.2rem 0}.hero p{color:#a5afa8}.metric{background:#101a14e8;border:1px solid #d6e2d31f;border-radius:12px;padding:1rem 1.15rem}.metric .label{font-size:.62rem;letter-spacing:.15em;color:#7f8a82;font-weight:800}.metric .value{font-size:2rem;font-weight:700}.card{background:#0a110de8;border:1px solid #d6e2d31f;border-radius:13px;padding:1rem;margin-bottom:.7rem}.overdue{border-left:5px solid #e17c73}.due{border-left:5px solid #d0ae62}.done{border-left:5px solid #83b88e}.badge{display:inline-block;border-radius:999px;padding:.32rem .58rem;font-size:.61rem;font-weight:800}.progress{background:#d0ae6219;color:#d0ae62}.overdue-b{background:#e17c7319;color:#e17c73}.done-b{background:#83b88e19;color:#83b88e}.small{color:#77827a;font-size:.65rem;letter-spacing:.08em}.desc{color:#bdc6be;font-size:.82rem;line-height:1.5;margin-top:.4rem}.doc{background:#f6f6f2;color:#20231f;padding:2.5rem;min-height:400px;border-radius:8px;line-height:1.7;font-family:Georgia,serif}.stButton>button,.stDownloadButton>button{border-radius:7px;border:1px solid #9db5853d;background:#7e97681c;color:#c4d3b4;font-weight:700}.stButton>button:hover{border-color:#b7cba1}.stTextInput input,.stTextArea textarea{background:#0003!important;color:#edf2ec!important}.ru-overlay{position:fixed;z-index:99999;left:50%;top:50%;transform:translate(-50%,-50%);width:min(760px,92vw);padding:18px;background:#050908f7;border:2px solid #a9bc91;border-radius:18px;box-shadow:0 25px 80px #000}.ru-title{text-align:center;color:#f2df8c;font-size:28px;font-weight:900;margin-bottom:8px}.ship-svg{width:100%;display:block;border-radius:10px}.langbox{font-size:.72rem;color:#9eaaa1;margin-top:.4rem}.response-box{padding:.7rem;border-left:3px solid #78906b;background:#ffffff06;border-radius:7px;margin:.4rem 0}
</style>''',unsafe_allow_html=True)

c1,c2=st.columns([1,4])
with c1:
    selected=st.selectbox('Мова інтерфейсу',['Українська','Російська'],index=0 if st.session_state.lang=='Українська' else 1,label_visibility='collapsed')
    if selected!=st.session_state.lang: st.session_state.lang=selected; st.rerun()
with c2: st.markdown(f'<div class="langbox">Мова інтерфейсу — <b>{st.session_state.lang.lower()}</b></div>',unsafe_allow_html=True)
if st.session_state.lang=='Російська': russian_joke()

st.markdown(f'<div class="brand"><div><div class="eyebrow">ЗБРОЙНІ СИЛИ УКРАЇНИ</div><div class="title">КОНТРОЛЬ ВИКОНАННЯ <span>РОЗПОРЯДЖЕНЬ</span></div></div><div class="small">● ЛОКАЛЬНИЙ РЕЖИМ • {date.today().strftime("%d.%m.%Y")}</div></div>',unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="kicker">ОПЕРАТИВНИЙ КОНТРОЛЬ</div><h1>Процес виконання <em>розпоряджень</em></h1><p>Документи, відповіді та додатки зберігаються локально у вибраній робочій папці.</p></div>',unsafe_allow_html=True)
with st.expander(f'📁 РОБОЧА ПАПКА — {WORK}',expanded=False):
    st.write('Структура: Робоча папка → Розпорядження → № розпорядження → Відповіді.')
    manual=st.text_input('Шлях до робочої папки',value=str(WORK),key='manual')
    if st.button('Застосувати робочу папку',key='apply') and manual.strip(): st.session_state.workspace=manual.strip(); st.rerun()

allr=orders(); counts={'all':len(allr),'progress':0,'overdue':0,'done':0}
for r in allr: counts[stat(r)]+=1
for col,label,val in zip(st.columns(4),['УСЬОГО','У РОБОТІ','ПРОСТРОЧЕНО','ВИКОНАНО'],[counts['all'],counts['progress'],counts['overdue'],counts['done']]):
    with col: st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{val}</div></div>',unsafe_allow_html=True)

left,right=st.columns([1,2.2])
with left:
    st.markdown('<div class="kicker">ДОДАТИ РОЗПОРЯДЖЕННЯ</div>',unsafe_allow_html=True)
    with st.form('add',clear_on_submit=True):
        n=st.text_input('№ розпорядження',placeholder='1111'); o=st.text_input('Вихідний номер',placeholder='Необов’язково'); d=st.date_input('Кінцевий термін',value=date.today()); desc=st.text_area('Короткий опис розпорядження',height=110,placeholder='Коротко опишіть, що передбачає розпорядження'); f=st.file_uploader('Файл розпорядження',type=['pdf','doc','docx','txt','png','jpg','jpeg','zip','rar','7z']); save=st.form_submit_button('＋ ЗБЕРЕГТИ РОЗПОРЯДЖЕННЯ',use_container_width=True)
        if save:
            if not n or not desc or not f: st.error('Заповніть №, короткий опис та прикріпіть документ.')
            else: add_order(n,o,d,desc,f); st.rerun()
with right:
    q=st.text_input('🔎 Пошук за №, вихідним номером або коротким описом',placeholder='Введіть текст для пошуку'); flt=st.radio('ФІЛЬТР',['Усі','У роботі','Прострочені','Виконані'],horizontal=True)
    for r in orders():
        s=stat(r); hay=f'{r["number"]} {r["outgoing"]} {r["description"]}'.lower()
        if q.lower() not in hay or (flt=='У роботі' and s!='progress') or (flt=='Прострочені' and s!='overdue') or (flt=='Виконані' and s!='done'): continue
        cls='done' if s=='done' else ('overdue' if s=='overdue' else ('due' if days(r)<=2 else '')); badge='done-b' if s=='done' else ('overdue-b' if s=='overdue' else 'progress'); label='ВИКОНАНО' if s=='done' else ('ПРОСТРОЧЕНО' if s=='overdue' else 'У РОБОТІ')
        st.markdown(f'<div class="card {cls}"><b>№ {html.escape(r["number"])}</b> <span class="badge {badge}">{label}</span><div class="desc">{html.escape(r["description"])}</div><div class="small">ТЕРМІН: {r["deadline"]}'+(f' • ВИХ. № {html.escape(r["outgoing"])}' if r['outgoing'] else '')+'</div></div>',unsafe_allow_html=True)
        b1,b2,b3,b4,b5=st.columns(5)
        with b1:
            if s!='done':
                if st.button('✓ Виконано',key=f'done_{r["id"]}',use_container_width=True): st.session_state[f'complete_{r["id"]}']=True; st.rerun()
            else:
                if st.button('↩ У роботу',key=f'undo_{r["id"]}',use_container_width=True): reopen(r); st.rerun()
        with b2:
            if st.button('↩ Відповідь',key=f'reply_{r["id"]}',use_container_width=True): st.session_state[f'reply_form_{r["id"]}']=True; st.rerun()
        with b3:
            if st.button('✎ Редагувати',key=f'edit_{r["id"]}',use_container_width=True): st.session_state[f'edit_{r["id"]}']=True; st.rerun()
        with b4:
            if st.button('📄 Відкрити',key=f'open_{r["id"]}',use_container_width=True): st.session_state[f'open_{r["id"]}']=True; st.rerun()
        with b5:
            if st.button('📂 Папка',key=f'folder_{r["id"]}',use_container_width=True): open_local(ORDERS/r['folder'])
        if st.session_state.get(f'complete_{r["id"]}'):
            with st.form(f'complete_form_{r["id"]}'):
                co=st.text_input('Вихідний номер документа про виконання',value=r['completion_outgoing']); cc=st.text_area('Коментар до виконання',value=r['completion_comment']); x1,x2=st.columns(2); ok=x1.form_submit_button('ПІДТВЕРДИТИ ВИКОНАННЯ',use_container_width=True); cancel=x2.form_submit_button('Скасувати',use_container_width=True)
                if ok: complete(r,co,cc); st.session_state.pop(f'complete_{r["id"]}',None); st.rerun()
                if cancel: st.session_state.pop(f'complete_{r["id"]}',None); st.rerun()
        if st.session_state.get(f'reply_form_{r["id"]}'):
            with st.form(f'reply_form_box_{r["id"]}'):
                st.markdown(f'### Відповідь на розпорядження № {r["number"]}'); rd=st.date_input('Дата відповіді',value=date.today()); ro=st.text_input('Вихідний номер відповіді',placeholder='Наприклад: 04/123'); rc=st.text_area('Короткий результат виконання',placeholder='Що зроблено у відповідь на розпорядження?'); rf=st.file_uploader('Файл відповіді або архів додатків',type=['pdf','doc','docx','txt','png','jpg','jpeg','zip','rar','7z'],key=f'rf_{r["id"]}'); final=st.checkbox('Це остаточна відповідь — позначити розпорядження як виконане'); x1,x2=st.columns(2); add=x1.form_submit_button('ЗБЕРЕГТИ ВІДПОВІДЬ',use_container_width=True); cancel=x2.form_submit_button('Скасувати',use_container_width=True)
                if add:
                    if not rf: st.error('Додайте файл відповіді або архів.')
                    else: add_reply(r,rd,ro,rc,rf,final); st.session_state.pop(f'reply_form_{r["id"]}',None); st.rerun()
                if cancel: st.session_state.pop(f'reply_form_{r["id"]}',None); st.rerun()
        if st.session_state.get(f'edit_{r["id"]}'):
            with st.form(f'edit_form_{r["id"]}'):
                en=st.text_input('№ розпорядження',value=r['number']); eo=st.text_input('Вихідний номер',value=r['outgoing']); ed=st.date_input('Кінцевий термін',value=date.fromisoformat(r['deadline'])); ee=st.text_area('Короткий опис розпорядження',value=r['description']); x1,x2=st.columns(2); save_edit=x1.form_submit_button('ЗБЕРЕГТИ ЗМІНИ',use_container_width=True); cancel=x2.form_submit_button('Скасувати',use_container_width=True)
                if save_edit: edit_order(r,en,eo,ed,ee); st.session_state.pop(f'edit_{r["id"]}',None); st.rerun()
                if cancel: st.session_state.pop(f'edit_{r["id"]}',None); st.rerun()
        if st.session_state.get(f'open_{r["id"]}'):
            st.markdown(f'### Розпорядження № {html.escape(r["number"])}'); preview(resolve_path(r['path']),r['mime'],f'order_dl_{r["id"]}')
            if st.button('Закрити документ',key=f'close_{r["id"]}'): st.session_state.pop(f'open_{r["id"]}',None); st.rerun()
        rr=replies(r['id'])
        if rr:
            with st.expander(f'↩ Відповіді — {len(rr)}',expanded=False):
                for rep in rr:
                    rp=resolve_path(rep['path']); st.markdown(f'<div class="response-box"><b>{rep["response_date"]}</b> • Вих. № {html.escape(rep["outgoing"]) if rep["outgoing"] else "—"} {"• ОСТАТОЧНА" if rep["is_final"] else ""}<br>{html.escape(rep["comment"]) if rep["comment"] else "Без коментаря"}<br><span class="small">{html.escape(rep["filename"])}</span></div>',unsafe_allow_html=True)
                    x1,x2=st.columns(2)
                    if x1.button('📄 Відкрити відповідь',key=f'openrep_{rep["id"]}'): st.session_state[f'viewrep_{rep["id"]}']=True
                    if x2.button('📂 Відкрити папку',key=f'folderrep_{rep["id"]}'): open_local(rp.parent)
                    if st.session_state.get(f'viewrep_{rep["id"]}'): preview(rp,rep['mime'],f'rep_dl_{rep["id"]}')

st.markdown('<div class="small" style="text-align:center;margin-top:2rem">СИСТЕМА КОНТРОЛЮ ВИКОНАННЯ • ЛОКАЛЬНЕ ЗБЕРІГАННЯ</div>',unsafe_allow_html=True)
