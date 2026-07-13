# Calwest E-Commerce Analytics Dashboard | Tableau

A Tableau e-commerce analytics case study covering revenue, profit, discounts, customers, product performance, promotions and regional trends across **251,431 order lines**.

> This repository documents my completed Tableau case study and independently validates its metrics. Course-provider slides, pre-completed workbooks and unlicensed raw datasets are intentionally excluded.

## Dashboard scope

### E-Commerce Performance Overview

- KPI dashboard for revenue, profit, discount, profit margin, orders, customers, units, quantity and average order value
- Monthly revenue and profit trend analysis by product category
- Category and subcategory revenue analysis
- Product profitability scatter plot
- Interactive order-date filters
- Parameter-driven switching between revenue and profit

### Regional Performance Summary

- US state map grouped by region
- Promotion versus non-promotion revenue share by month
- Category and subcategory treemap
- Top-10 products by gross revenue
- Dashboard actions for state-level filtering

## Verified results

| Metric | Result |
|---|---:|
| Order lines | 251,431 |
| Distinct orders | 184,375 |
| Customers | 12,246 |
| Products | 44 |
| Gross revenue | $81.27M |
| Profit | $44.17M |
| Profit margin | 54.35% |
| Discount | $4.11M |
| Average order value | $440.79 |

## Key findings

- **Very Berry Parfum** was the highest-revenue product at approximately **$4.88M**.
- The **East** was the highest-revenue region at approximately **$22.10M**.
- **Cat Dry Food** was the highest-revenue subcategory at approximately **$12.65M**.
- Promotion-linked revenue reached its highest monthly share in **January 2021**, at approximately **47.49%**.

## Tools and techniques

- Tableau Public
- Tableau relationships and multi-table data modelling
- Calculated fields and parameters
- Dashboard actions and interactive filtering
- Maps, treemaps, line charts, bar charts, scatter plots and lollipop charts
- Python and Pandas for independent metric validation

## Repository structure

```text
assets/       Original dashboard screenshot placeholder
data/         Source-data availability and privacy note
docs/         Methodology, data model, calculations and findings
outputs/      Aggregate validation results
scripts/      Reproducible Python validation script
tableau/      Completed workbook placeholder
```

## Reproduce the validation

1. Place authorised source CSV files under `data/raw/` using the filenames listed in `data/README.md`.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run:

```bash
python scripts/analyze_calwest.py
```

## Tableau workbook and screenshot

The public package does not substitute a course-provider completed workbook or slide screenshot for my work. Add the personally completed workbook and original exported dashboard screenshot using the instructions in `tableau/README.md` and `assets/README.md`.

## Author

**Ijash Ahmed Z**  
[LinkedIn](https://www.linkedin.com/in/ijash-ahmed-z/) | [GitHub](https://github.com/ijash-ahmed-z) | [Portfolio](https://ijash-ahmed-z.netlify.app/)
