
"""
analysis.py
------------
Task 4: Programming logic — functions, loops, conditionals and arrays.

This module demonstrates programming fundamentals using plain Python.
"""


def total_sales_records(sales_rows: list) -> int:
    """Count sales records using a loop."""
    count = 0

    for row in sales_rows:
        count += 1

    return count


def low_stock_alert(products_rows: list, threshold: int = 5) -> list:
    """Return products that need reordering when stock information exists."""
    alerts = []

    for product in products_rows:
        if "in_stock" in product:
            if product["in_stock"] is False:
                alerts.append(product["product_name"])

        elif "stock_count" in product:
            if product["stock_count"] <= threshold:
                alerts.append(product["product_name"])

    return alerts


def monthly_sales_trend(sales_rows: list) -> dict:
    """Calculate total quantity sold per month."""
    trend = {}

    for row in sales_rows:
        sale_date = row["sale_date"]
        month = str(sale_date)[:7]
        quantity = int(row["quantity"])

        if month in trend:
            trend[month] += quantity
        else:
            trend[month] = quantity

    return trend


def classify_transaction_size(quantity: int) -> str:
    """Classify a transaction according to its quantity."""
    if quantity >= 5:
        return "Bulk"
    elif quantity >= 2:
        return "Multiple"
    elif quantity == 1:
        return "Single"
    else:
        return "Invalid"


def average_basket_size(sales_rows: list) -> float:
    """Calculate the average quantity per sale."""
    if not sales_rows:
        return 0.0

    total = 0

    for row in sales_rows:
        total += int(row["quantity"])

    return round(total / len(sales_rows), 2)

