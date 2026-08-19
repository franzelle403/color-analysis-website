import sqlite3
from pathlib import Path


# Always use the makeup.db file inside the backend folder
DATABASE_PATH = Path(__file__).parent / "makeup.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS makeup (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            shade TEXT NOT NULL,
            season TEXT NOT NULL,
            undertone TEXT,
            depth TEXT,
            chroma TEXT,
            price REAL,
            image_url TEXT,
            buy_url TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------
# GET ALL PRODUCTS
# Used by the admin frontend
# ---------------------------------------

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM makeup
        ORDER BY id DESC
    """)

    products = cursor.fetchall()
    conn.close()

    return [dict(product) for product in products]


# ---------------------------------------
# GET RECOMMENDATIONS BY SEASON
# Used by your color analysis result
# ---------------------------------------

def get_recommendations(season):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM makeup
        WHERE LOWER(season) = LOWER(?)
        ORDER BY category, brand
    """, (season,))

    products = cursor.fetchall()
    conn.close()

    return [dict(product) for product in products]


# ---------------------------------------
# ADD PRODUCT
# Used by admin.html
# ---------------------------------------

def add_product(
    brand,
    product_name,
    category,
    shade,
    season,
    undertone="",
    depth="",
    chroma="",
    price=0,
    image_url="",
    buy_url=""
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO makeup (
            brand,
            product_name,
            category,
            shade,
            season,
            undertone,
            depth,
            chroma,
            price,
            image_url,
            buy_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        brand,
        product_name,
        category,
        shade,
        season,
        undertone,
        depth,
        chroma,
        price,
        image_url,
        buy_url
    ))

    conn.commit()

    product_id = cursor.lastrowid

    conn.close()

    return product_id


# ---------------------------------------
# UPDATE PRODUCT
# Used by Edit button in admin.html
# ---------------------------------------

def update_product(
    product_id,
    brand,
    product_name,
    category,
    shade,
    season,
    undertone="",
    depth="",
    chroma="",
    price=0,
    image_url="",
    buy_url=""
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE makeup
        SET
            brand = ?,
            product_name = ?,
            category = ?,
            shade = ?,
            season = ?,
            undertone = ?,
            depth = ?,
            chroma = ?,
            price = ?,
            image_url = ?,
            buy_url = ?
        WHERE id = ?
    """, (
        brand,
        product_name,
        category,
        shade,
        season,
        undertone,
        depth,
        chroma,
        price,
        image_url,
        buy_url,
        product_id
    ))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated > 0


# ---------------------------------------
# DELETE PRODUCT
# Used by Delete button in admin.html
# ---------------------------------------

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM makeup
        WHERE id = ?
    """, (product_id,))

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    return deleted > 0


# ---------------------------------------
# OPTIONAL SAMPLE PRODUCTS
# ---------------------------------------

def add_sample_products():
    conn = get_connection()
    cursor = conn.cursor()

    # Prevent the same sample products from being
    # inserted every time you run database.py
    cursor.execute("SELECT COUNT(*) FROM makeup")

    count = cursor.fetchone()[0]

    if count > 0:
        conn.close()
        print("Database already has products. Samples were not added.")
        return


    products = [
        (
            "Rom&nd",
            "Juicy Lasting Tint",
            "Lip",
            "Bare Grape",
            "Soft Summer",
            "Cool",
            "Medium",
            "Muted",
            499,
            "https://example.com/bare-grape.jpg",
            "https://shopee.ph/"
        ),

        (
            "Rom&nd",
            "Juicy Lasting Tint",
            "Lip",
            "Nucadamia",
            "Soft Autumn",
            "Warm",
            "Medium",
            "Muted",
            499,
            "https://example.com/nucadamia.jpg",
            "https://shopee.ph/"
        ),

        (
            "Happy Skin",
            "Lip Mallow",
            "Lip",
            "Chai Latte",
            "Soft Autumn",
            "Warm",
            "Medium",
            "Muted",
            549,
            "https://example.com/chai-latte.jpg",
            "https://shopee.ph/"
        ),

        (
            "BLK Cosmetics",
            "Creamy All Over Paint",
            "Blush",
            "Peony",
            "Bright Winter",
            "Cool",
            "Medium",
            "Bright",
            399,
            "https://example.com/peony.jpg",
            "https://shopee.ph/"
        )
    ]

    cursor.executemany("""
        INSERT INTO makeup (
            brand,
            product_name,
            category,
            shade,
            season,
            undertone,
            depth,
            chroma,
            price,
            image_url,
            buy_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products)

    conn.commit()
    conn.close()

    print("Sample products added!")


# ---------------------------------------
# RUN DATABASE SETUP
# ---------------------------------------

if __name__ == "__main__":
    create_database()
    add_sample_products()
    print("Makeup database ready!")