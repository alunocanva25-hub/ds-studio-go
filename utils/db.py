from __future__ import annotations

import os
import sqlite3
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "ds_studio_go.db"


def connect() -> sqlite3.Connection:
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            display_name TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT NOT NULL,
            service TEXT NOT NULL,
            professional TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'Agendado'
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS financial_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            date TEXT NOT NULL,
            notes TEXT
        )
        """
    )
    cur.execute("SELECT COUNT(*) AS total FROM users")
    if cur.fetchone()["total"] == 0:
        cur.executemany(
            "INSERT INTO users (username, password, display_name, role) VALUES (?, ?, ?, ?)",
            [
                ("admin", "123456", "Administrador", "admin"),
                ("operacional", "123456", "Operacional", "operacional"),
            ],
        )
    conn.commit()
    conn.close()


def validate_user(username: str, password: str):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, display_name, role FROM users WHERE username = ? AND password = ?",
        (username.strip(), password),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def add_schedule(client: str, service: str, professional: str, dt: str, tm: str, notes: str) -> None:
    conn = connect()
    conn.execute(
        "INSERT INTO schedules (client, service, professional, date, time, notes) VALUES (?, ?, ?, ?, ?, ?)",
        (client.strip(), service.strip(), professional.strip(), dt, tm, notes.strip()),
    )
    conn.commit()
    conn.close()


def list_schedules(limit: int = 50):
    conn = connect()
    rows = conn.execute(
        "SELECT * FROM schedules ORDER BY date ASC, time ASC, id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_schedule_status(schedule_id: int, status: str) -> None:
    conn = connect()
    conn.execute("UPDATE schedules SET status = ? WHERE id = ?", (status, schedule_id))
    conn.commit()
    conn.close()


def add_financial_entry(entry_type: str, description: str, amount: float, payment_method: str, dt: str, notes: str) -> None:
    conn = connect()
    conn.execute(
        "INSERT INTO financial_entries (type, description, amount, payment_method, date, notes) VALUES (?, ?, ?, ?, ?, ?)",
        (entry_type, description.strip(), float(amount), payment_method, dt, notes.strip()),
    )
    conn.commit()
    conn.close()


def list_financial_entries(limit: int = 50):
    conn = connect()
    rows = conn.execute(
        "SELECT * FROM financial_entries ORDER BY date DESC, id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_dashboard_summary() -> dict:
    today = str(date.today())
    conn = connect()
    today_schedule_count = conn.execute(
        "SELECT COUNT(*) AS total FROM schedules WHERE date = ?",
        (today,),
    ).fetchone()["total"]
    received_today = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM financial_entries WHERE date = ? AND type = 'Entrada'",
        (today,),
    ).fetchone()["total"]
    expense_today = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM financial_entries WHERE date = ? AND type = 'Saída'",
        (today,),
    ).fetchone()["total"]
    next_schedules = conn.execute(
        "SELECT * FROM schedules ORDER BY date ASC, time ASC, id DESC LIMIT 5"
    ).fetchall()
    latest_entries = conn.execute(
        "SELECT * FROM financial_entries ORDER BY date DESC, id DESC LIMIT 5"
    ).fetchall()
    conn.close()
    return {
        "today_schedule_count": int(today_schedule_count or 0),
        "received_today": float(received_today or 0),
        "expense_today": float(expense_today or 0),
        "balance_today": float((received_today or 0) - (expense_today or 0)),
        "next_schedules": [dict(r) for r in next_schedules],
        "latest_entries": [dict(r) for r in latest_entries],
    }
