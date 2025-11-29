import sqlite3
from pathlib import Path

db = sqlite3.connect(Path.cwd()/'backend'/'resourcely.db')

def create_table():
    dbcursor = db.cursor()
    dbcursor.execute("""
        CREATE TABLE IF NOT EXISTS resource (
            id INTEGER PRIMARY KEY,
            title text,
            type text,
            subject text,
            tags text,
            url_or_path text,
            notes text,
            created_at DEFAULT CURRENT_TIMESTAMP,
            updated_at DEFAULT CURRENT_TIMESTAMP
            )
    """)
    db.commit()

def add_data(title, subject, notes, url_or_path, tags='default', type_='default'):
    '''url_or_path -> where this resource lives (url, path, notes)'''
    dbcursor = db.cursor()
    dbcursor.execute(
        """
        INSERT INTO resource (title, subject, notes, url_or_path, tags, type)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, subject, notes, url_or_path, tags, type_)
    )
    db.commit()

def get_all_data():
    dbcursor = db.cursor()
    dbcursor.execute(
        """
        SELECT *
        FROM resource
        ORDER BY updated_at DESC 
        """
    )
    return dbcursor.fetchall()

def get_data_by_subject(subject):
    dbcursor = db.cursor()
    dbcursor.execute(
        """
        SELECT id, title, type, subject, notes, url_or_path, tags, created_at, updated_at
        FROM resource
        WHERE subject = ?
        ORDER BY updated_at DESC 
        """,
        (subject,),     # we need to use comma inside to make it touple, touple cant be single element
    )
    return dbcursor.fetchall()

def search_data(query):
    dbcursor = db.cursor()
    pattern = f"%{query}%"
    dbcursor.execute(
        """
        SELECT id, title, type, subject, notes, url_or_path, tags, created_at, updated_at
        FROM resource
        WHERE tile LIKE ? OR notes LIKE ?
        ORDER BY updated_at DESC 
        """,
        (pattern, pattern),
    )
    return dbcursor.findall()


db.close()