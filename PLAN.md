# PLAN — Thabo's Corner Store Sales Insights System

**Student:** Ntsondwa Sanele
**ID N0:** [9909085710088]
**Module:** KM-04 / KM-05 Integrated Project

## 1. Decomposition — what are the sub-problems?

The project breaks into five ordered sub-problems:

1. **Load and clean** two messy CSVs (`products.csv`, `sales.csv`) into tidy DataFrames.
2. **Build a relational database** with `products` and `sales` tables, correct primary
   and foreign keys, and query it with SQL.
3. **Analyse** the cleaned data with plain Python — loops, conditionals, dicts, lists.
4. **Visualise** the findings as at least one bar chart and one line chart.
5. **Protect** the reports behind a hashed-password login gate.

I will tackle them in this order because each one depends on the one before it:
I cannot build the database without clean data, cannot analyse without the database,
cannot chart without analysis results, and must gate the reports only once they exist.

## 2. Pattern recognition — what mess do I expect?

From reading the brief and inspecting the raw files:

- `products.csv`: two missing `unit_price` values (P006, P013), inconsistent category
  casing (`beverages` vs `Beverages`), one duplicated product row (P003 appears twice),
  and product IDs are non-contiguous (P009 missing entirely).
- `sales.csv`: four different date formats mixed together (ISO `YYYY-MM-DD`,
  `DD/MM/YYYY`, `YYYY/MM/DD`, `DD-MM-YYYY`), missing `quantity` on ~19 rows, missing
  `sale_date` on several rows, missing `payment_method` on several rows, invalid
  `product_id`s (P009, P099) that do not exist in products, and one duplicated row
  (S0011 appears twice).

The pattern is the classic real-world triad: missing values, inconsistent formats,
and referential-integrity violations.

## 3. Abstraction — what can I ignore for now?

- I do not need to model customers as a separate table for this project — `customer_type`
  is a simple enum-like field, not a full entity.
- I do not need real-time updates — this is a one-shot batch pipeline.
- I do not need bank-grade authentication — a single SHA-256 password gate is enough
  to demonstrate the concept.
- I do not need a front-end — the console output plus saved PNG charts are the deliverable.

## 4. Algorithm sketch — order of operations
