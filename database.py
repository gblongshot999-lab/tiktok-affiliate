"""Database module for TikTok Affiliate Suite — SQLite storage."""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "affiliate.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            commission_rate REAL,
            source_url TEXT,
            notes TEXT,
            status TEXT DEFAULT 'researching',
            added_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS affiliate_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            url TEXT NOT NULL,
            platform TEXT DEFAULT 'tiktok',
            clicks INTEGER DEFAULT 0,
            conversions INTEGER DEFAULT 0,
            revenue REAL DEFAULT 0.0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS content_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            title TEXT NOT NULL,
            content_type TEXT DEFAULT 'video',
            platform TEXT DEFAULT 'tiktok',
            scheduled_date TEXT,
            status TEXT DEFAULT 'planned',
            hashtags TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()


# --- Product CRUD ---

def add_product(name, category, price, commission_rate, source_url="", notes=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO products (name, category, price, commission_rate, source_url, notes) VALUES (?, ?, ?, ?, ?, ?)",
        (name, category, price, commission_rate, source_url, notes),
    )
    conn.commit()
    conn.close()


def get_products():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM products ORDER BY added_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_product_status(product_id, status):
    conn = get_connection()
    conn.execute("UPDATE products SET status = ? WHERE id = ?", (status, product_id))
    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = get_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


# --- Affiliate Link CRUD ---

def add_affiliate_link(product_id, url, platform="tiktok"):
    conn = get_connection()
    conn.execute(
        "INSERT INTO affiliate_links (product_id, url, platform) VALUES (?, ?, ?)",
        (product_id, url, platform),
    )
    conn.commit()
    conn.close()


def get_affiliate_links():
    conn = get_connection()
    rows = conn.execute("""
        SELECT al.*, p.name as product_name
        FROM affiliate_links al
        LEFT JOIN products p ON al.product_id = p.id
        ORDER BY al.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_link_stats(link_id, clicks, conversions, revenue):
    conn = get_connection()
    conn.execute(
        "UPDATE affiliate_links SET clicks = ?, conversions = ?, revenue = ? WHERE id = ?",
        (clicks, conversions, revenue, link_id),
    )
    conn.commit()
    conn.close()


def delete_affiliate_link(link_id):
    conn = get_connection()
    conn.execute("DELETE FROM affiliate_links WHERE id = ?", (link_id,))
    conn.commit()
    conn.close()


# --- Content Plan CRUD ---

def add_content_plan(product_id, title, content_type, platform, scheduled_date, hashtags="", notes=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO content_plans (product_id, title, content_type, platform, scheduled_date, hashtags, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (product_id, title, content_type, platform, scheduled_date, hashtags, notes),
    )
    conn.commit()
    conn.close()


def get_content_plans():
    conn = get_connection()
    rows = conn.execute("""
        SELECT cp.*, p.name as product_name
        FROM content_plans cp
        LEFT JOIN products p ON cp.product_id = p.id
        ORDER BY cp.scheduled_date ASC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_content_status(plan_id, status):
    conn = get_connection()
    conn.execute("UPDATE content_plans SET status = ? WHERE id = ?", (status, plan_id))
    conn.commit()
    conn.close()


def delete_content_plan(plan_id):
    conn = get_connection()
    conn.execute("DELETE FROM content_plans WHERE id = ?", (plan_id,))
    conn.commit()
    conn.close()


# --- Analytics ---

def get_dashboard_stats():
    conn = get_connection()
    stats = {}
    stats["total_products"] = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    stats["active_links"] = conn.execute("SELECT COUNT(*) FROM affiliate_links").fetchone()[0]
    stats["total_clicks"] = conn.execute("SELECT COALESCE(SUM(clicks), 0) FROM affiliate_links").fetchone()[0]
    stats["total_conversions"] = conn.execute("SELECT COALESCE(SUM(conversions), 0) FROM affiliate_links").fetchone()[0]
    stats["total_revenue"] = conn.execute("SELECT COALESCE(SUM(revenue), 0) FROM affiliate_links").fetchone()[0]
    stats["planned_content"] = conn.execute("SELECT COUNT(*) FROM content_plans WHERE status = 'planned'").fetchone()[0]
    conn.close()
    return stats


# Initialize on import
init_db()
