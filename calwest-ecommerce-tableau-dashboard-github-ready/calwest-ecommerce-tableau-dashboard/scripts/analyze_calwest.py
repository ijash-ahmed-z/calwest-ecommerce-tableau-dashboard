"""Validate Calwest e-commerce Tableau metrics from authorised local source files.

Expected files under data/raw/:
- factOrder.csv
- dimCustomer.csv
- dimLocation.csv
- dimPayment.csv
- dimProduct.csv
- dimPromo.csv
- dimShipping.csv

The script exports aggregate outputs only. It does not export customer names or emails.
"""

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(name: str) -> pd.DataFrame:
    path = RAW / name
    if not path.exists():
        raise FileNotFoundError(f"Missing source file: {path}")
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise UnicodeError(f"Unable to decode {path}")


def main() -> None:
    fact = read_csv("factOrder.csv")
    product = read_csv("dimProduct.csv")
    location = read_csv("dimLocation.csv")
    promo = read_csv("dimPromo.csv")
    payment = read_csv("dimPayment.csv")
    shipping = read_csv("dimShipping.csv")
    customer = read_csv("dimCustomer.csv")

    for column in ("Order Date", "Ship Date"):
        fact[column] = pd.to_datetime(fact[column], errors="coerce")

    fact["Profit"] = fact["Revenue"] - fact["Cost"]
    fact["Discount"] = fact["BaseRevenue"] - fact["Revenue"]
    fact["Is Promo"] = np.where(fact["PromoId"].notna(), "Promo", "No Promo")

    model = (
        fact.merge(product, on="ProductId", how="left", validate="many_to_one")
        .merge(location, on="LocationId", how="left", validate="many_to_one")
        .merge(
            promo[["PromoId", "Promo Code", "Promo Description", "Campaign", "Promo Type", "Promo Amount"]],
            on="PromoId",
            how="left",
            validate="many_to_one",
        )
        .merge(payment, on="PaymentId", how="left", validate="many_to_one")
        .merge(shipping, on="ShippingMethodId", how="left", validate="many_to_one")
    )

    revenue = fact["Revenue"].sum()
    profit = fact["Profit"].sum()
    orders = fact["Order ID"].nunique()

    pd.DataFrame(
        [
            ["Order lines", len(fact)],
            ["Distinct orders", orders],
            ["Distinct customers", fact["CustomerId"].nunique()],
            ["Products", product["ProductId"].nunique()],
            ["States", location["State"].nunique()],
            ["Gross revenue", revenue],
            ["Profit", profit],
            ["Profit margin", profit / revenue],
            ["Discount", fact["Discount"].sum()],
            ["Units", fact["Units"].sum()],
            ["Quantity", fact["Quantity"].sum()],
            ["Average order value", revenue / orders],
        ],
        columns=["Metric", "Value"],
    ).to_csv(OUT / "kpi_summary.csv", index=False)

    monthly = (
        model.assign(OrderMonth=model["Order Date"].dt.to_period("M").astype(str))
        .groupby(["OrderMonth", "Category"], dropna=False)
        .agg(
            GrossRevenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique"),
            Quantity=("Quantity", "sum"),
        )
        .reset_index()
    )
    monthly["ProfitMargin"] = monthly["Profit"] / monthly["GrossRevenue"]
    monthly.to_csv(OUT / "revenue_trend_by_month_category.csv", index=False)

    category = (
        model.groupby(["Category", "SubCategory"], dropna=False)
        .agg(
            GrossRevenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Discount=("Discount", "sum"),
            Orders=("Order ID", "nunique"),
            Quantity=("Quantity", "sum"),
        )
        .reset_index()
    )
    category["ProfitMargin"] = category["Profit"] / category["GrossRevenue"]
    category.to_csv(OUT / "category_subcategory_performance.csv", index=False)

    products = (
        model.groupby(["ProductId", "ProductName", "Category", "SubCategory"], dropna=False)
        .agg(
            GrossRevenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Discount=("Discount", "sum"),
            Orders=("Order ID", "nunique"),
            Quantity=("Quantity", "sum"),
        )
        .reset_index()
    )
    products["ProfitMargin"] = products["Profit"] / products["GrossRevenue"]
    products = products.sort_values("GrossRevenue", ascending=False)
    products.to_csv(OUT / "product_profitability.csv", index=False)
    products.head(10).to_csv(OUT / "top_10_products_by_revenue.csv", index=False)

    regions = (
        model.groupby("Region", dropna=False)
        .agg(
            GrossRevenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Discount=("Discount", "sum"),
            Orders=("Order ID", "nunique"),
            Customers=("CustomerId", "nunique"),
        )
        .reset_index()
    )
    regions["ProfitMargin"] = regions["Profit"] / regions["GrossRevenue"]
    regions.to_csv(OUT / "regional_performance.csv", index=False)

    states = (
        model.groupby(["Region", "State", "Abbreviation"], dropna=False)
        .agg(
            GrossRevenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique"),
        )
        .reset_index()
    )
    states["ProfitMargin"] = states["Profit"] / states["GrossRevenue"]
    states.to_csv(OUT / "state_performance.csv", index=False)

    promo_month = (
        model.assign(OrderMonth=model["Order Date"].dt.to_period("M").astype(str))
        .groupby(["OrderMonth", "Is Promo"], dropna=False)
        .agg(GrossRevenue=("Revenue", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
    )
    promo_month["RevenueShare"] = promo_month["GrossRevenue"] / promo_month.groupby("OrderMonth")["GrossRevenue"].transform("sum")
    promo_month.to_csv(OUT / "promotion_revenue_share_by_month.csv", index=False)

    # Aggregate data-quality summary; no customer-level values are exported.
    quality_rows = []
    for name, frame in (
        ("factOrder", fact),
        ("dimProduct", product),
        ("dimLocation", location),
        ("dimPromo", promo),
        ("dimPayment", payment),
        ("dimShipping", shipping),
        ("dimCustomer", customer),
    ):
        quality_rows.append(
            {
                "Table": name,
                "Rows": len(frame),
                "Columns": len(frame.columns),
                "DuplicateRows": int(frame.duplicated().sum()),
                "ColumnsWithNulls": int((frame.isna().sum() > 0).sum()),
                "TotalNullCells": int(frame.isna().sum().sum()),
            }
        )
    pd.DataFrame(quality_rows).to_csv(OUT / "data_quality_summary.csv", index=False)

    print("Calwest validation outputs created in", OUT)


if __name__ == "__main__":
    main()
