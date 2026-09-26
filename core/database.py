from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

SCHEMA={
"orders":"""CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,number TEXT NOT NULL,deadline TEXT NOT NULL,description TEXT NOT NULL,folder TEXT NOT NULL,filename TEXT NOT NULL,path TEXT NOT NULL,mime TEXT NOT NULL,status TEXT DEFAULT 'progress',completion_outgoing TEXT DEFAULT '',priority TEXT DEFAULT 'Звичайний',responsible TEXT DEFAULT '',category TEXT DEFAULT 'Інше',received_date TEXT DEFAULT '',tags TEXT DEFAULT '',created_at TEXT NOT NULL,updated_at TEXT DEFAULT '',deleted_at TEXT DEFAULT '',deleted_path TEXT DEFAULT '')""",
"responses":"""CREATE TABLE IF NOT EXISTS responses(id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER NOT NULL,response_date TEXT NOT NULL,outgoing TEXT DEFAULT '',comment TEXT DEFAULT '',filename TEXT NOT NULL,path TEXT NOT NULL,mime TEXT NOT NULL,is_final INTEGER DEFAULT 0,created_at TEXT NOT NULL)""",
"attachments":"""CREATE TABLE IF NOT EXISTS attachments(id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER NOT NULL,response_id INTEGER DEFAULT 0,filename TEXT NOT NULL,path TEXT NOT NULL,mime TEXT NOT NULL,created_at TEXT NOT NULL)""",
"events":"""CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER NOT NULL,event_type TEXT NOT NULL,details TEXT DEFAULT '',created_at TEXT NOT NULL)""",
"settings":"""CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT NOT NULL)"""}
MIGRATIONS={"orders":{"completion_outgoing":"TEXT DEFAULT ''","priority":"TEXT DEFAULT 'Звичайний'","responsible":"TEXT DEFAULT ''","category":"TEXT DEFAULT 'Інше'","received_date":"TEXT DEFAULT ''","tags":"TEXT DEFAULT ''","updated_at":"TEXT DEFAULT ''","deleted_at":"TEXT DEFAULT ''","deleted_path":"TEXT DEFAULT ''"}}

class Database:
    def __init__(self,path:Path): self.path=path; self.initialize()
    @contextmanager
    def connection(self)->Iterator[sqlite3.Connection]:
        conn=sqlite3.connect(self.path); conn.row_factory=sqlite3.Row; conn.execute("PRAGMA foreign_keys=ON")
        try: yield conn; conn.commit()
        except Exception: conn.rollback(); raise
        finally: conn.close()
    def initialize(self)->None:
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.connection() as conn:
            for sql in SCHEMA.values(): conn.execute(sql)
            for table,columns in MIGRATIONS.items():
                existing={r[1] for r in conn.execute(f"PRAGMA table_info({table})")}
                for name,definition in columns.items():
                    if name not in existing: conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {definition}")
            for sql in ("CREATE INDEX IF NOT EXISTS idx_orders_deadline ON orders(deadline)","CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)","CREATE INDEX IF NOT EXISTS idx_orders_responsible ON orders(responsible)","CREATE INDEX IF NOT EXISTS idx_orders_deleted ON orders(deleted_at)","CREATE INDEX IF NOT EXISTS idx_responses_order ON responses(order_id)","CREATE INDEX IF NOT EXISTS idx_attachments_order ON attachments(order_id)","CREATE INDEX IF NOT EXISTS idx_attachments_response ON attachments(response_id)","CREATE INDEX IF NOT EXISTS idx_events_order ON events(order_id)"): conn.execute(sql)
    def execute(self,sql:str,params:tuple[Any,...]=())->int:
        with self.connection() as conn: return int(conn.execute(sql,params).lastrowid or 0)
    def fetchone(self,sql:str,params:tuple[Any,...]=())->sqlite3.Row|None:
        with self.connection() as conn: return conn.execute(sql,params).fetchone()
    def fetchall(self,sql:str,params:tuple[Any,...]=())->list[sqlite3.Row]:
        with self.connection() as conn: return conn.execute(sql,params).fetchall()
    def log(self,order_id:int,event_type:str,details:str="")->None: self.execute("INSERT INTO events(order_id,event_type,details,created_at) VALUES(?,?,?,?)",(order_id,event_type,details,datetime.now().isoformat(timespec="seconds")))
    def get_orders(self,include_deleted:bool=False)->list[sqlite3.Row]:
        where="" if include_deleted else "WHERE COALESCE(deleted_at,'')=''"; return self.fetchall(f"SELECT * FROM orders {where} ORDER BY CASE WHEN status='done' THEN 2 ELSE 0 END, deadline ASC,id DESC")
    def get_order(self,order_id:int,include_deleted:bool=False)->sqlite3.Row|None:
        where="" if include_deleted else "AND COALESCE(deleted_at,'')=''"; return self.fetchone(f"SELECT * FROM orders WHERE id=? {where}",(order_id,))
    def get_responses(self,order_id:int)->list[sqlite3.Row]: return self.fetchall("SELECT * FROM responses WHERE order_id=? ORDER BY response_date DESC,id DESC",(order_id,))
    def get_attachments(self,order_id:int,response_id:int=0)->list[sqlite3.Row]: return self.fetchall("SELECT * FROM attachments WHERE order_id=? AND response_id=? ORDER BY id DESC",(order_id,response_id))
    def get_events(self,order_id:int)->list[sqlite3.Row]: return self.fetchall("SELECT * FROM events WHERE order_id=? ORDER BY created_at DESC,id DESC",(order_id,))
    def get_trash(self)->list[sqlite3.Row]: return self.fetchall("SELECT * FROM orders WHERE COALESCE(deleted_at,'')<>'' ORDER BY deleted_at DESC,id DESC")
    def set_setting(self,key:str,value:str)->None: self.execute("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(key,value))
    def get_setting(self,key:str,default:str="")->str:
        row=self.fetchone("SELECT value FROM settings WHERE key=?",(key,)); return str(row[0]) if row else default
    def move_to_trash(self,order_id:int,deleted_path:str)->None:
        now=datetime.now().isoformat(timespec="seconds")
        with self.connection() as conn:
            conn.execute("UPDATE orders SET deleted_at=?,deleted_path=?,updated_at=? WHERE id=?",(now,deleted_path,now,order_id)); conn.execute("INSERT INTO events(order_id,event_type,details,created_at) VALUES(?,?,?,?)",(order_id,"Переміщено до кошика","Розпорядження можна відновити",now))
    def restore_from_trash(self,order_id:int)->None: self.execute("UPDATE orders SET deleted_at='',deleted_path='',updated_at=? WHERE id=?",(datetime.now().isoformat(timespec="seconds"),order_id)); self.log(order_id,"Відновлено","Розпорядження повернуто з кошика")
    def purge_order(self,order_id:int)->None:
        with self.connection() as conn:
            conn.execute("DELETE FROM attachments WHERE order_id=?",(order_id,)); conn.execute("DELETE FROM responses WHERE order_id=?",(order_id,)); conn.execute("DELETE FROM events WHERE order_id=?",(order_id,)); conn.execute("DELETE FROM orders WHERE id=?",(order_id,))
