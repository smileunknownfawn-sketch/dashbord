from __future__ import annotations
import base64, hashlib, html, mimetypes, sqlite3
from datetime import date, datetime
from pathlib import Path
import streamlit as st
try:
    from docx import Document
except Exception:
    Document = None

APP_DIR=Path(__file__).resolve().parent
DATA_DIR=APP_DIR/'data'; UPLOAD_DIR=DATA_DIR/'documents'; DB_PATH=DATA_DIR/'orders.db'
DATA_DIR.mkdir(exist_ok=True); UPLOAD_DIR.mkdir(exist_ok=True)
st.set_page_config(page_title='Контроль виконання розпоряджень',page_icon='🇺🇦',layout='wide',initial_sidebar_state='collapsed')

def db():
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row
    c.execute('''CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,number TEXT NOT NULL,outgoing_number TEXT DEFAULT '',deadline TEXT NOT NULL,description TEXT NOT NULL,filename TEXT NOT NULL,stored_name TEXT NOT NULL,mime_type TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'progress',completed_at TEXT DEFAULT '',completion_outgoing TEXT DEFAULT '',completion_comment TEXT DEFAULT '',created_at TEXT NOT NULL,updated_at TEXT NOT NULL)''')
    cols={r[1] for r in c.execute('PRAGMA table_info(orders)').fetchall()}
    for col in ['outgoing_number','completed_at','completion_outgoing','completion_comment']:
        if col not in cols:c.execute(f'ALTER TABLE orders ADD COLUMN {col} TEXT DEFAULT \'\'')
    c.commit();return c

def seed_demo():
    c=db()
    if c.execute('SELECT COUNT(*) FROM orders').fetchone()[0]==0:
        name='demo_order_01_2026.txt'; text='ЗБРОЙНІ СИЛИ УКРАЇНИ\n\nНАВЧАЛЬНИЙ ПРИКЛАД РОЗПОРЯДЖЕННЯ\n№ 01/2026\n\nТермін виконання: 05 жовтня 2026 року\n\nЗАВДАННЯ\nПідготувати та надати узагальнену інформацію про стан виконання визначених завдань.\n\nПРИМІТКА\nЦей документ є демонстраційним прикладом. Не є службовим документом.'
        (UPLOAD_DIR/name).write_text(text,encoding='utf-8'); now=datetime.now().isoformat(timespec='seconds')
        c.execute('INSERT INTO orders(number,deadline,description,filename,stored_name,mime_type,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)',('01/2026','2026-10-05','Підготувати та надати узагальнену інформацію про стан виконання визначених завдань.',name,name,'text/plain','progress',now,now));c.commit()
    c.close()

def rows():
    c=db(); r=c.execute('SELECT * FROM orders ORDER BY deadline ASC,id DESC').fetchall();c.close();return r
def days_left(d):return(date.fromisoformat(d)-date.today()).days
def status(r):return 'done' if r['status']=='done' else ('overdue' if days_left(r['deadline'])<0 else 'progress')
def status_text(s):return {'progress':'У роботі','overdue':'Прострочено','done':'Виконано'}[s]
def save_file(f):
    raw=f.getvalue(); safe=''.join(x if x.isalnum() or x in '._-' else '_' for x in f.name); stored=f'{hashlib.sha256(raw).hexdigest()[:12]}_{safe}';(UPLOAD_DIR/stored).write_bytes(raw);return stored,f.type or mimetypes.guess_type(f.name)[0] or 'application/octet-stream'
def add_order(n,o,d,desc,f):
    stored,mime=save_file(f);now=datetime.now().isoformat(timespec='seconds');c=db();c.execute('INSERT INTO orders(number,outgoing_number,deadline,description,filename,stored_name,mime_type,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)',(n.strip(),o.strip(),d.isoformat(),desc.strip(),f.name,stored,mime,'progress',now,now));c.commit();c.close()
def edit_order(r,n,o,d,desc):
    c=db();c.execute('UPDATE orders SET number=?,outgoing_number=?,deadline=?,description=?,updated_at=? WHERE id=?',(n.strip(),o.strip(),d.isoformat(),desc.strip(),datetime.now().isoformat(timespec='seconds'),r['id']));c.commit();c.close()
def complete(r,outgoing,comment):
    now=datetime.now().isoformat(timespec='seconds');c=db();c.execute('UPDATE orders SET status=?,completed_at=?,completion_outgoing=?,completion_comment=?,updated_at=? WHERE id=?',('done',now,outgoing.strip(),comment.strip(),now,r['id']));c.commit();c.close()
def reopen(r):
    c=db();c.execute('UPDATE orders SET status=?,completed_at="",completion_outgoing="",completion_comment="",updated_at=? WHERE id=?',('progress',datetime.now().isoformat(timespec='seconds'),r['id']));c.commit();c.close()
def delete_order(r):
    c=db();c.execute('DELETE FROM orders WHERE id=?',(r['id'],));c.commit();c.close();
    try:(UPLOAD_DIR/r['stored_name']).unlink(missing_ok=True)
    except:pass
def preview(r):
    p=UPLOAD_DIR/r['stored_name']
    if not p.exists():st.error('Файл документа не знайдено.');return
    raw=p.read_bytes();mime=r['mime_type']
    if mime=='application/pdf' or p.suffix.lower()=='.pdf':
        b64=base64.b64encode(raw).decode();st.components.v1.html(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="680" style="border:0"></iframe>',height=700)
    elif mime.startswith('image/'):st.image(raw,use_container_width=True)
    elif p.suffix.lower()=='.txt':st.code(raw.decode('utf-8',errors='replace'),language='text')
    elif p.suffix.lower()=='.docx' and Document:
        doc=Document(p);text='\n\n'.join(x.text for x in doc.paragraphs if x.text.strip());st.markdown(f'<div class="doc">{html.escape(text).replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
    else:st.info('Для цього формату доступне завантаження оригіналу.')
    st.download_button('⬇ Завантажити оригінал',raw,file_name=r['filename'],mime=mime,key=f'dl{r["id"]}')

seed_demo()
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Oswald:wght@500;600&display=swap');
.stApp{background:linear-gradient(120deg,rgba(4,8,5,.96),rgba(7,13,9,.87)),url('https://images.unsplash.com/photo-1580137189272-c9379f8864fd?auto=format&fit=crop&w=2400&q=85') center/cover fixed;color:#edf2ec}.block-container{max-width:1450px;padding:2rem 3rem}.brand{border-bottom:1px solid #ffffff1c;padding-bottom:1.3rem;margin-bottom:2rem;display:flex;justify-content:space-between}.eyebrow,.kicker{font-size:.64rem;font-weight:800;letter-spacing:.2em;color:#a9bc91}.title{font-family:Oswald,sans-serif;font-size:1.25rem;letter-spacing:.08em}.title span,.hero em{color:#b7c7a6}.hero h1{font-size:clamp(2rem,4vw,3.5rem);margin:.25rem 0}.hero p{color:#a5afa8}.metric{background:#101a14e8;border:1px solid #d6e2d31f;border-radius:12px;padding:1rem 1.15rem}.metric .label{font-size:.62rem;letter-spacing:.15em;color:#7f8a82;font-weight:800}.metric .value{font-size:2rem;font-weight:700}.card{background:#0a110de8;border:1px solid #d6e2d31f;border-radius:13px;padding:1rem;margin-bottom:.7rem}.overdue{border-left:5px solid #e17c73;background:linear-gradient(90deg,#8e232335,#0a110de8 50%)}.due{border-left:5px solid #d0ae62}.done{border-left:5px solid #83b88e;background:linear-gradient(90deg,#3a704614,#0a110de8 50%)}.badge{display:inline-block;border-radius:999px;padding:.32rem .58rem;font-size:.61rem;font-weight:800}.progress{background:#d0ae6219;color:#d0ae62}.overdue-b{background:#e17c7319;color:#e17c73}.done-b{background:#83b88e19;color:#83b88e}.small{color:#77827a;font-size:.65rem;letter-spacing:.08em}.desc{color:#bdc6be;font-size:.82rem;line-height:1.5;margin-top:.4rem}.red{color:#ff9b93}.gold{color:#e4c777}.doc{background:#f6f6f2;color:#20231f;padding:2.5rem;min-height:400px;border-radius:8px;line-height:1.7;font-family:Georgia,serif}.stButton>button,.stDownloadButton>button{border-radius:7px;border:1px solid #9db5853d;background:#7e97681c;color:#c4d3b4;font-weight:700}
</style>''',unsafe_allow_html=True)
st.markdown(f'<div class="brand"><div><div class="eyebrow">ЗБРОЙНІ СИЛИ УКРАЇНИ</div><div class="title">КОНТРОЛЬ ВИКОНАННЯ <span>РОЗПОРЯДЖЕНЬ</span></div></div><div class="small">● СИСТЕМА АКТИВНА • {date.today().strftime("%d.%m.%Y")}</div></div>',unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="kicker">ОПЕРАТИВНИЙ КОНТРОЛЬ</div><h1>Процес виконання <em>розпоряджень</em></h1><p>Єдиний реєстр документів, контроль термінів, вихідних номерів та результатів виконання.</p></div>',unsafe_allow_html=True)
all_orders=rows();counts={'all':len(all_orders),'progress':0,'overdue':0,'done':0}
for r in all_orders:counts[status(r)]+=1
for col,label,val in zip(st.columns(4),['УСЬОГО','У РОБОТІ','ПРОСТРОЧЕНО','ВИКОНАНО'],[counts['all'],counts['progress'],counts['overdue'],counts['done']]):
    with col:st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{val}</div></div>',unsafe_allow_html=True)
st.write('')
left,right=st.columns([1,2.2])
with left:
    st.markdown('<div class="kicker">ДОДАТИ РОЗПОРЯДЖЕННЯ</div>',unsafe_allow_html=True)
    with st.form('add',clear_on_submit=True):
        n=st.text_input('№ розпорядження',placeholder='27/2026');o=st.text_input('Вихідний номер',placeholder='Необов’язково');d=st.date_input('Кінцевий термін',value=date.today());desc=st.text_area('Що потрібно виконати',height=110);f=st.file_uploader('Файл розпорядження',type=['pdf','doc','docx','txt','png','jpg','jpeg']);ok=st.form_submit_button('＋ ЗБЕРЕГТИ',use_container_width=True)
        if ok:
            if not n or not desc or not f:st.error('Заповніть №, завдання та прикріпіть документ.')
            else:add_order(n,o,d,desc,f);st.success('Розпорядження додано.');st.rerun()
with right:
    q=st.text_input('🔎 Пошук за №, вихідним номером або описом');filt=st.radio('ФІЛЬТР',['Усі','У роботі','Прострочені','Виконані'],horizontal=True)
    for r in rows():
        s=status(r);text=f'{r["number"]} {r["outgoing_number"]} {r["description"]}'.lower()
        if q.lower() not in text:continue
        if filt=='У роботі' and s!='progress':continue
        if filt=='Прострочені' and s!='overdue':continue
        if filt=='Виконані' and s!='done':continue
        cls='done' if s=='done' else ('overdue' if s=='overdue' else ('due' if days_left(r['deadline'])<=2 else ''))
        badge='done-b' if s=='done' else ('overdue-b' if s=='overdue' else 'progress')
        out=f' • Вих. № {html.escape(r["outgoing_number"])}' if r['outgoing_number'] else ''
        st.markdown(f'<div class="card {cls}"><b>№ {html.escape(r["number"])}</b><span class="small">{out}</span> <span class="badge {badge}">{status_text(s).upper()}</span><div class="desc">{html.escape(r["description"])}</div><div class="small">ТЕРМІН: <span class="{"red" if s=="overdue" else "gold" if days_left(r["deadline"])<=2 and s!="done" else ""}">{r["deadline"]}</span>{f" • ВИКОНАНО: {r['completed_at']}" if s=='done' else ''}</div></div>',unsafe_allow_html=True)
        b1,b2,b3,b4=st.columns(4)
        with b1:
            if s!='done':
                if st.button('✓ Виконано',key=f'done{r["id"]}',use_container_width=True):st.session_state[f'complete{r["id"]}']=True;st.rerun()
            else:
                if st.button('↩ Повернути',key=f'undo{r["id"]}',use_container_width=True):reopen(r);st.rerun()
        with b2:
            if st.button('✎ Редагувати',key=f'edit{r["id"]}',use_container_width=True):st.session_state[f'edit{r["id"]}']=True;st.rerun()
        with b3:
            if st.button('📄 Відкрити',key=f'open{r["id"]}',use_container_width=True):st.session_state[f'open{r["id"]}']=True;st.rerun()
        with b4:
            if st.button('🗑 Видалити',key=f'del{r["id"]}',use_container_width=True):st.session_state[f'del{r["id"]}']=True;st.rerun()
        if st.session_state.get(f'complete{r["id"]}'):
            with st.form(f'complete_form{r["id"]}'):
                co=st.text_input('Вихідний номер документа про виконання',value=r['completion_outgoing']);cc=st.text_area('Коментар до виконання',value=r['completion_comment']);c1,c2=st.columns(2)
                with c1:save=st.form_submit_button('ПІДТВЕРДИТИ ВИКОНАННЯ',use_container_width=True)
                with c2:cancel=st.form_submit_button('Скасувати',use_container_width=True)
                if save:complete(r,co,cc);st.session_state.pop(f'complete{r["id"]}',None);st.rerun()
                if cancel:st.session_state.pop(f'complete{r["id"]}',None);st.rerun()
        if st.session_state.get(f'edit{r["id"]}'):
            with st.form(f'edit_form{r["id"]}'):
                en=st.text_input('№',value=r['number']);eo=st.text_input('Вихідний №',value=r['outgoing_number']);ed=st.date_input('Термін',value=date.fromisoformat(r['deadline']));ee=st.text_area('Опис',value=r['description']);c1,c2=st.columns(2)
                with c1:save=st.form_submit_button('ЗБЕРЕГТИ ЗМІНИ',use_container_width=True)
                with c2:cancel=st.form_submit_button('Скасувати',use_container_width=True)
                if save:edit_order(r,en,eo,ed,ee);st.session_state.pop(f'edit{r["id"]}',None);st.rerun()
                if cancel:st.session_state.pop(f'edit{r["id"]}',None);st.rerun()
        if st.session_state.get(f'open{r["id"]}'):
            st.markdown(f'**Розпорядження № {r["number"]}**');preview(r)
            if st.button('Закрити документ',key=f'close{r["id"]}'):st.session_state.pop(f'open{r["id"]}',None);st.rerun()
        if st.session_state.get(f'del{r["id"]}'):
            st.warning('Видалити запис і прикріплений файл?')
            c1,c2=st.columns(2)
            with c1:
                if st.button('Так, видалити',key=f'yes{r["id"]}'):delete_order(r);st.session_state.pop(f'del{r["id"]}',None);st.rerun()
            with c2:
                if st.button('Скасувати',key=f'no{r["id"]}'):st.session_state.pop(f'del{r["id"]}',None);st.rerun()
st.markdown('<div class="small" style="text-align:center;padding:25px">СИСТЕМА КОНТРОЛЮ ВИКОНАННЯ • СЛУЖБОВИЙ ІНТЕРФЕЙС</div>',unsafe_allow_html=True)
