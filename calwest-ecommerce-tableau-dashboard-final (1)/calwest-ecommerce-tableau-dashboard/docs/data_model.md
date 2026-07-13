# Data model

The Tableau model follows a fact-and-dimension structure using relationships rather than physical joins.

```mermaid
erDiagram
    FACT_ORDER }o--|| DIM_CUSTOMER : CustomerId
    FACT_ORDER }o--|| DIM_LOCATION : LocationId
    FACT_ORDER }o--|| DIM_PAYMENT : PaymentId
    FACT_ORDER }o--|| DIM_PRODUCT : ProductId
    FACT_ORDER }o--o| DIM_PROMO : PromoId
    FACT_ORDER }o--|| DIM_SHIPPING : ShippingMethodId
```

## Tables

- `factOrder`: order-line transactions, dates, revenue, quantity, units, cost and foreign keys
- `dimCustomer`: customer reference data
- `dimLocation`: state, abbreviation, population and region
- `dimPayment`: payment provider and method
- `dimProduct`: product, SKU, category and subcategory
- `dimPromo`: promotion code, campaign, type and amount
- `dimShipping`: shipping type and method

The promotion relationship is optional because some order lines have no promotion.
