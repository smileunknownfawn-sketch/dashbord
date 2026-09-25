from __future__ import annotations
import html, mimetypes, os, sqlite3, subprocess, sys
from datetime import date, datetime
from pathlib import Path
import streamlit as st

st.set_page_config(page_title='Процес виконання розпоряджень', page_icon='🇺🇦', layout='wide')
APP=Path(__file__).resolve().parent
if 'workspace' not in st.session_state: st.session_state.workspace=str(APP/'data')
if 'add_open' not in st.session_state: st.session_state.add_open=False
if 'response_order' not in st.session_state: st.session_state.response_order=None
if 'lang' not in st.session_state: st.session_state.lang='Українська'
WORK=Path(st.session_state.workspace); WORK.mkdir(parents=True,exist_ok=True)
ORDERS=WORK/'Розпорядження'; ORDERS.mkdir(exist_ok=True)
DB=WORK/'database.db'
CSS='''<style>@import url(https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap);html,body,[class*=css]{font-family:Inter,sans-serif}.stApp{background:linear-gradient(135deg,#07100a,#1b291d 48%,#060906);color:#edf2ec}.block-container{max-width:1450px;padding:2rem 3rem}.hero h1{font-family:Manrope,sans-serif;font-style:normal;font-weight:800;font-size:clamp(2rem,4vw,3.5rem);letter-spacing:-.04em}.eyebrow{color:#b1c79e;font-weight:800;font-size:.65rem;letter-spacing:.2em}.version{text-align:right;color:#89958c;font-size:.68rem;letter-spacing:.12em;font-weight:700}.panel,.order,.metric{background:#09120de8;border:1px solid #dce9d91e;border-radius:14px;padding:1rem}.order{margin:.7rem 0;border-left:5px solid #d0ae62}.order.overdue{border-left-color:#e16f68}.order.done{border-left-color:#78b589}.desc{color:#bdc7be;margin:.5rem 0;line-height:1.5}.muted{color:#7f8b83;font-size:.7rem;letter-spacing:.07em}.badge{padding:.3rem .55rem;border-radius:99px;font-size:.62rem;font-weight:800}.work{color:#d0ae62;background:#d0ae6218}.late{color:#e16f68;background:#e16f6818}.finished{color:#78b589;background:#78b58918}.stButton>button{border-radius:8px;background:#78925f20;border:1px solid #a9bc9140;color:#d7e2d0;font-weight:800}.successbox{padding:18px;border:1px solid #9ab58a55;border-radius:14px;background:#263d2a}.stTextInput input,.stTextArea textarea{background:#0004!important;color:#fff!important}</style>'''
st.markdown(CSS,unsafe_allow_html=True)
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
 c.execute('''CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,number TEXT,deadline TEXT,description TEXT,folder TEXT,filename TEXT,path TEXT,mime TEXT,status TEXT DEFAULT 'progress',completion_outgoing TEXT DEFAULT '',created_at TEXT)''')
 c.execute('''CREATE TABLE IF NOT EXISTS responses(id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER,response_date TEXT,outgoing TEXT,comment TEXT,filename TEXT,path TEXT,mime TEXT,is_final INTEGER DEFAULT 0,created_at TEXT)''')
 c.commit(); return c
def safe(s): return ''.join(x if x.isalnum() or x in ' ._-()[]' else '_' for x in str(s)).strip() or 'Документ'
def copy_upload(f,folder):
 folder.mkdir(parents=True,exist_ok=True); p=folder/safe(f.name); i=2
 while p.exists(): p=folder/f'{p.stem}_{i}{p.suffix}'; i+=1
 p.write_bytes(f.getvalue()); return p
def state(r):
 if r['status']=='done': return 'done'
 try:return 'overdue' if date.fromisoformat(r['deadline'])<date.today() else 'progress'
 except:return 'progress'
def open_file(path):
 try:
  if sys.platform.startswith('win'): os.startfile(str(path))
  elif sys.platform=='darwin': subprocess.Popen(['open',str(path)])
  else: subprocess.Popen(['xdg-open',str(path)])
 except Exception as e: st.error(f'Не вдалося відкрити файл: {e}')
def audio(path):
 if not path.exists(): return
 import base64
 b=base64.b64encode(path.read_bytes()).decode()
 st.markdown(f'<audio autoplay><source src="data:audio/mpeg;base64,{b}" type="audio/mpeg"></audio>',unsafe_allow_html=True)
def add_order(n,d,desc,f):
 folder=ORDERS/safe(n); i=2
 while folder.exists(): folder=ORDERS/f'{safe(n)}_{i}'; i+=1
 p=copy_upload(f,folder); c=db(); c.execute('INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(n,d.isoformat(),desc,folder.name,p.name,str(p.relative_to(WORK)),f.type or mimetypes.guess_type(p.name)[0] or 'application/octet-stream','progress',datetime.now().isoformat())); c.commit(); c.close()
def add_response(r,d,out,comment,f,final):
 folder=ORDERS/r['folder']/'Відповіді'; p=copy_upload(f,folder); c=db(); c.execute('INSERT INTO responses(order_id,response_date,outgoing,comment,filename,path,mime,is_final,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)',(r['id'],d.isoformat(),out,comment,p.name,str(p.relative_to(WORK)),f.type or 'application/octet-stream',int(final),datetime.now().isoformat()))
 if final:c.execute("UPDATE orders SET status='done',completion_outgoing=? WHERE id=?",(out,r['id']))
 c.commit();c.close()
c=db()
if c.execute('SELECT COUNT(*) FROM orders').fetchone()[0]==0:
 folder=ORDERS/'01-2026';folder.mkdir(exist_ok=True);p=folder/'Розпорядження_01-2026.txt';p.write_text('ДЕМОНСТРАЦІЙНЕ РОЗПОРЯДЖЕННЯ\n\nПідготувати та надати узагальнену інформацію про стан виконання визначених завдань.',encoding='utf-8');c.execute('INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,created_at) VALUES(?,?,?,?,?,?,?,?,?)',('01/2026','2026-10-05','Підготувати та надати узагальнену інформацію про стан виконання визначених завдань.',folder.name,p.name,str(p.relative_to(WORK)),'text/plain','progress',datetime.now().isoformat()));c.commit()
rows=c.execute('SELECT * FROM orders ORDER BY deadline').fetchall();c.close()
l,r=st.columns([4,1])
with l:
 lang=st.selectbox('Мова інтерфейсу',['Українська','Російська'],index=0 if st.session_state.lang=='Українська' else 1,label_visibility='collapsed');st.session_state.lang=lang
 st.markdown(f'<div class="muted">Мова інтерфейсу — <b>{lang}</b></div>',unsafe_allow_html=True)
with r:st.markdown('<div class="version">ВЕРСІЯ 1.0.1</div>',unsafe_allow_html=True)
if lang=='Російська': st.warning('Ти що, москаль? 😄')
st.markdown('<div class="eyebrow">ЗБРОЙНІ СИЛИ УКРАЇНИ</div><div class="hero"><h1>Процес виконання розпоряджень</h1><p class="muted">Контроль термінів, документів та відповідей у єдиному робочому просторі.</p></div>',unsafe_allow_html=True)
if st.button('＋ ДОДАТИ РОЗПОРЯДЖЕННЯ'):st.session_state.add_open=not st.session_state.add_open;st.rerun()
if st.session_state.add_open:
 with st.form('new'):
  a,b=st.columns(2)
  with a:n=st.text_input('№ розпорядження');d=st.date_input('Дата, до якої потрібно виконати',value=date.today())
  with b:desc=st.text_area('Короткий опис розпорядження',height=120);f=st.file_uploader('Файл розпорядження')
  x,y=st.columns(2)
  with x:save=st.form_submit_button('ЗБЕРЕГТИ РОЗПОРЯДЖЕННЯ')
  with y:cancel=st.form_submit_button('СКАСУВАТИ')
  if cancel:st.session_state.add_open=False;st.rerun()
  if save:
   if not n or not desc or not f:st.error('Заповніть №, короткий опис та додайте файл.')
   else:add_order(n,d,desc,f);st.session_state.add_open=False;st.session_state.just_added=True;st.rerun()
if st.session_state.pop('just_added',False):
 st.markdown('<div class="successbox"><b>РОЗПОРЯДЖЕННЯ ДОДАНО</b><br><span class="muted">Опять работа? 😄</span></div>',unsafe_allow_html=True)
 audio(APP/'opiat-rabota.mp3')
c=db();rows=c.execute('SELECT * FROM orders ORDER BY deadline').fetchall();c.close();counts={'progress':0,'overdue':0,'done':0}
for r in rows:counts[state(r)]+=1
for col,label,val in zip(st.columns(4),['УСЬОГО','У РОБОТІ','ПРОСТРОЧЕНО','ВИКОНАНО'],[len(rows),counts['progress'],counts['overdue'],counts['done']]):
 with col:st.markdown(f'<div class="metric"><div class="muted">{label}</div><b style="font-size:1.8rem">{val}</b></div>',unsafe_allow_html=True)
st.write('');q=st.text_input('🔎 Пошук за № або коротким описом',placeholder='Введіть текст...');filt=st.radio('ФІЛЬТР',['Усі','У роботі','Прострочені','Виконані'],horizontal=True)
for r in rows:
 s=state(r);hay=f'{r["number"]} {r["description"]}'.lower()
 if q.lower() not in hay or (filt=='У роботі' and s!='progress') or (filt=='Прострочені' and s!='overdue') or (filt=='Виконані' and s!='done'):continue
 cls='overdue' if s=='overdue' else ('done' if s=='done' else '');badge='late' if s=='overdue' else ('finished' if s=='done' else 'work');label={'overdue':'ПРОСТРОЧЕНО','done':'ВИКОНАНО','progress':'У РОБОТІ'}[s]
 st.markdown(f'<div class="order {cls}"><b>№ {html.escape(r["number"])}</b> <span class="badge {badge}">{label}</span><div class="desc">{html.escape(r["description"])}</div><div class="muted">ТЕРМІН: {r["deadline"]}</div></div>',unsafe_allow_html=True)
 a,b,c=st.columns(3)
 with a:
  if st.button('📄 ВІДКРИТИ РОЗПОРЯДЖЕННЯ',key=f'open{r["id"]}'):open_file(WORK/r['path'])
 with b:
  if st.button('↩ ДОДАТИ ВІДПОВІДЬ',key=f'res{r["id"]}'):st.session_state.response_order=r['id'];st.rerun()
 with c:
  if s!='done' and st.button('✓ ПОЗНАЧИТИ ВИКОНАНИМ',key=f'done{r["id"]}'):st.session_state.response_order=r['id'];st.session_state.final_response=True;st.rerun()
 if st.session_state.response_order==r['id']:
  st.markdown('<div class="panel"><b>ВІДПОВІДЬ НА РОЗПОРЯДЖЕННЯ</b></div>',unsafe_allow_html=True)
  with st.form(f'form{r["id"]}'):
   d=st.date_input('Дата відповіді',value=date.today(),key=f'date{r["id"]}');out=st.text_input('Вихідний номер відповіді',key=f'out{r["id"]}');comment=st.text_area('Короткий зміст відповіді',key=f'com{r["id"]}');rf=st.file_uploader('Файл відповіді / архів',key=f'file{r["id"]}');final=st.checkbox('Позначити розпорядження виконаним',value=st.session_state.pop('final_response',False),key=f'fin{r["id"]}');ok=st.form_submit_button('ЗБЕРЕГТИ ВІДПОВІДЬ')
   if ok:
    if not rf:st.error('Додайте файл відповіді або архів.')
    else:add_response(r,d,out,comment,rf,final);st.session_state.response_order=None;st.success('Відповідь збережено у папці цього розпорядження.');st.rerun()
st.markdown('<div class="muted" style="text-align:center;margin-top:3rem">СИСТЕМА КОНТРОЛЮ ВИКОНАННЯ • ЛОКАЛЬНИЙ РЕЖИМ • ВЕРСІЯ 1.0.1</div>',unsafe_allow_html=True)
