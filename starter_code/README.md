
# Thabo's Corner Store — Sales Insights System

**Student:** Ntsondwa Sanele
**Student number:** 9909085710088
**Module:** KM-04 / KM-05 Integrated Project
**Repository:** https://github.com/ntsondwasanele80-dot/thabo-corner-store

An end-to-end data application that cleans two messy CSVs, stores them in a
relational SQLite database, analyses them in plain Python, produces two
matplotlib charts, and gates the reports behind a hashed-password login.

---

## 1. How to install and run

**Requirements:** Python 3.10+, VS Code, Git.

From the project root:

```bash
python -m venv venv
Activate the virtual environment:

powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1
bash
# macOS / Linux
source venv/bin/activate
Install the required packages:

bash
pip install -r starter_code/requirements.txt
Run the pipeline:

bash
cd starter_code
python main.py
Outputs:

store.db — the SQLite database

revenue_per_product.png — bar chart of revenue per product

monthly_trend.png — line chart of monthly units sold

2. Data cleaning decisions
products.csv
Rows with a missing unit_price or product_name are dropped. We cannot
invent a price for a product, and a nameless product cannot be sold.

The category field is normalised to Title Case ("beverages" → "Beverages")
so category groupings do not split into two.

Exact duplicate rows are removed (P003 appeared twice).

Result: 16 raw rows → 12 clean rows (4 removed).

sales.csv
The raw file mixes four date formats:

Format	Example
ISO	2026-01-01
Day-first slash	02/01/2026
ISO with slashes	2026/01/03
Day-first dash	05-01-2026
I standardised every date to ISO YYYY-MM-DD. This sorts correctly, cannot be
misread, and matches how the database stores dates. Day-first was chosen for
the slash and dash formats because this is a South African store and dd/mm/yyyy
is the local convention. This decision is deliberately documented — the brief
warns against silently guessing.

Cleaning rules applied:

Drop rows with a missing or unparseable sale_date — they cannot be placed
on the monthly trend.

Drop rows with a missing quantity — no quantity means no revenue, and we
do not want to fabricate a number.

Fill missing payment_method with "Unknown" — the sale still happened; only
the payment channel is unrecorded.

Drop rows whose product_id does not exist in products (P009, P099) —
referential integrity.

Drop exact duplicate rows (S0011 appeared twice).

Result: 71 raw rows → 43 clean rows (28 removed).

3. Database schema
SQLite, two tables with a foreign-key relationship:

text
products                          sales
--------                          -----
product_id  TEXT  PK              sale_id        TEXT  PK
product_name TEXT NOT NULL        product_id     TEXT  FK → products.product_id
category     TEXT                 quantity       INTEGER
unit_price   REAL                 sale_date      TEXT   (ISO YYYY-MM-DD)
                                  payment_method TEXT
                                  customer_type  TEXT
products.product_id is the primary key and is referenced by
sales.product_id, giving a proper one-to-many relationship.

4. SQL queries and results
All queries live in database.py. Five are required, two are custom.

Q1 — Total revenue per product (JOIN + SUM aggregation)
Product	Revenue (R)
5kg Maize Meal	801.00
Eggs (6 pack)	364.00
Bar One Chocolate	224.00
Sugar 1kg	220.50
Coca-Cola 500ml	148.00
Airtime Voucher R10	140.00
Simba Chips 120g	132.00
Full Cream Milk 1L	129.00
Fanta Orange 500ml	111.00
Data Bundle 1GB	98.00
Coca-Cola 500ml (second entry)	74.00
White Bread 700g	48.00
Q2 — Best-selling product by total quantity (JOIN + SUM + LIMIT)
Top result: 5kg Maize Meal (consistent with Q1).

Q3 — Sales count by payment method (GROUP BY + COUNT)
Method	Number of sales
Cash	14
Mobile Money	11
Card	10
Unknown	8
Q4 — Revenue per product category (custom one — JOIN + SUM + GROUP BY)
Category	Revenue (R)
Household	1021.50
Dairy	493.00
Snacks	356.00
Beverages	333.00
Airtime & Data	238.00
Bakery	48.00
Q5 — Sales count by customer type (custom two — GROUP BY + COUNT)
Groups: Walk-in, Regular, and blank (customer_type not always recorded).

Programmatic results (from analysis.py)
Total sales records: 43

Monthly trend: 2026-01 → 52 units, 2026-02 → 44 units

Average basket size: 2.23 units per sale

Low-stock alerts: Data Bundle 1GB

5. Charts
revenue_per_product.png — bar chart
Vertical bars, one per product, ordered by revenue descending. 5kg Maize Meal
dominates, followed by Eggs and Bar One Chocolate. Bakery (only White Bread)
sits at the bottom, which makes sense for a small corner store where bread is a
low-margin staple.

monthly_trend.png — line chart
Two points: January 2026 (52 units) and February 2026 (44 units). Sales dropped
by ~15% month-on-month. Two months is not enough to call it a trend, but it is
worth watching — the drop could be seasonal (post-holiday) or a supply issue.

6. Security — CIA triad reflection
Confidentiality. The login gate requires a password before reports are shown.
The password is never stored in plain text — only its SHA-256 hash is kept in
security.py. On login, the typed password is hashed and compared to the stored
hash, so even if someone reads the source file, they cannot recover the password.
This protects the sales data from casual inspection by anyone who happens to have
the laptop.

Integrity. The login gate does not protect data integrity — that is a separate
concern. Integrity is enforced in database.py through (a) primary keys on
products.product_id and sales.sale_id, which prevent duplicate rows, (b) the
foreign key from sales.product_id to products.product_id, which prevents
orphaned sales, and (c) typed columns (INTEGER, REAL, TEXT), which prevent
nonsense values like a text quantity. These constraints mean the database can
only hold logically valid data.

Availability. The project lives only on my laptop, so a stolen, broken, or
wiped laptop would destroy both the code and the database. To protect against
this I would (a) push the code to GitHub regularly (which I do), (b) store the
database in a cloud-synced folder or remote backup, and (c) keep a copy of the
raw CSVs separately so the pipeline can always be re-run.

7. Key business insights (for Thabo)
Hello Thabo — here is what your two months of sales data is telling you.

Household goods are your bread and butter. They brought in R1021.50 of your
total revenue — more than Dairy, Snacks, and Beverages combined. The single
biggest winner is 5kg Maize Meal, which alone made R801. If you can only
keep one item fully stocked, keep that one.

Dairy is your second engine room. Eggs and Full Cream Milk together pulled
in R493. These are repeat-purchase staples that keep customers coming back, so
they are worth protecting with competitive pricing.

Cash is still king. 14 of your 43 sales were cash, 11 were Mobile Money, and
10 were Card. Only 8 sales have no payment method recorded — that is a data-entry
gap worth closing so you can see which channels are truly growing.

Watch the drop into February. January moved 52 units, February moved 44. A
15% drop over one month is not alarming yet, but if March repeats it, it will be
worth digging into which products lost the most volume.

One stock warning: the Data Bundle 1GB is marked as out of stock. Given that
Airtime & Data still brought in R238, it is worth reordering soon so you do not
lose those sales to a competitor.

One data-entry fix: the item "Coca-Cola 500ml" appears twice in your product
list with different IDs (P001 and P015). Merging them into one entry will
simplify your records and stop future confusion.

In short: keep Maize Meal and Dairy well-stocked, watch the February volume dip,
and tidy up the Coca-Cola duplicate.

8. Evidence checklist
☑ PLAN.md — computational-thinking plan (project root)
☑ data_cleaning.py, database.py, analysis.py, visualize.py, security.py, main.py
☑ store.db — SQLite database
☑ revenue_per_product.png, monthly_trend.png
☑ README.md — this file
☑ GitHub repository with ≥8 meaningful commits
text

---

## ▶️ After saving, verify in your terminal

```powershell
Get-Content .\starter_code\README.md | Measure-Object -Line