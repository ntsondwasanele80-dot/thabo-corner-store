"""
database.py
------------
Task 3: Build a relational database from your cleaned data.
"""

import sqlite3


def get_connection(db_path: str = "store.db") -> sqlite3.Connection:
    """Open or create the SQLite database."""
    return sqlite3.connect(db_path)


def create_tables(conn: sqlite3.Connection) -> None:
    """Create the products and sales tables."""

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            unit_price REAL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id TEXT PRIMARY KEY,
            product_id TEXT,
            quantity INTEGER,
            sale_date TEXT,
            payment_method TEXT,
            customer_type TEXT,
            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    conn.commit()


def insert_products(conn: sqlite3.Connection, products_df) -> None:
    """Insert the required product columns into the database."""

    # Clear existing rows so re-runs are idempotent.
    conn.execute("DELETE FROM products")
    conn.commit()

    columns = [
        "product_id",
        "product_name",
        "category",
        "unit_price"
    ]

    products_to_insert = products_df[columns]

    products_to_insert.to_sql(
        "products",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()


def insert_sales(conn: sqlite3.Connection, sales_df) -> None:
    """Insert the required sales columns into the database."""

    # Clear existing rows so re-runs are idempotent.
    conn.execute("DELETE FROM sales")
    conn.commit()

    columns = [
        "sale_id",
        "product_id",
        "quantity",
        "sale_date",
        "payment_method",
        "customer_type"
    ]

    sales_to_insert = sales_df[columns]

    sales_to_insert.to_sql(
        "sales",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()


def query_total_revenue_per_product(conn: sqlite3.Connection):
    """Return each product's total revenue."""

    sql = """
        SELECT
            p.product_name,
            SUM(s.quantity * p.unit_price) AS total_revenue
        FROM sales AS s
        JOIN products AS p
            ON s.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_revenue DESC
    """

    return conn.execute(sql).fetchall()


def query_best_selling_product(conn: sqlite3.Connection):
    """Return the product with the highest quantity sold."""

    sql = """
        SELECT
            p.product_name,
            SUM(s.quantity) AS total_quantity
        FROM sales AS s
        JOIN products AS p
            ON s.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_quantity DESC
        LIMIT 1
    """

    return conn.execute(sql).fetchall()


def query_sales_by_payment_method(conn: sqlite3.Connection):
    """Count sales transactions by payment method."""

    sql = """
        SELECT
            payment_method,
            COUNT(*) AS number_of_sales
        FROM sales
        GROUP BY payment_method
        ORDER BY number_of_sales DESC
    """

    return conn.execute(sql).fetchall()


def query_custom_one(conn: sqlite3.Connection):
    """Calculate revenue for each product category."""

    sql = """
        SELECT
            p.category,
            SUM(s.quantity * p.unit_price) AS total_revenue
        FROM sales AS s
        JOIN products AS p
            ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """

    return conn.execute(sql).fetchall()


def query_custom_two(conn: sqlite3.Connection):
    """Count sales transactions for each customer type."""

    sql = """
        SELECT
            customer_type,
            COUNT(*) AS number_of_sales
        FROM sales
        GROUP BY customer_type
        ORDER BY number_of_sales DESC
    """

    return conn.execute(sql).fetchall()
