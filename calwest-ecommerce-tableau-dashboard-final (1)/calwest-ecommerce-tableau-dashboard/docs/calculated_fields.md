# Tableau calculated fields

The dashboard uses the following calculated measures.

## Profit

```text
SUM([Revenue]) - SUM([Cost])
```

## Gross Revenue

```text
SUM([Revenue])
```

## Profit Margin %

```text
[Profit] / [Gross Revenue]
```

## Row-Level Profit Margin %

```text
([Revenue] - [Cost]) / [Revenue]
```

## Discount

```text
SUM([BaseRevenue]) - [Gross Revenue]
```

## Order Count

```text
COUNTD([Order ID])
```

## Customer Count

```text
COUNTD([CustomerId])
```

## Average Order Value

```text
[Gross Revenue] / [Order Count]
```

## Promotion Status

```text
IF NOT ISNULL([Promo Code]) THEN "Promo"
ELSE "No Promo"
END
```

## Measure Selector

A parameter can switch the trend and category views between gross revenue and profit.

```text
CASE [Select Measure]
WHEN "Gross Revenue" THEN [Gross Revenue]
WHEN "Profit" THEN [Profit]
END
```
