# Sizwe Coffee: Sales and Business Performance Analysis Using SQL

## Project Overview

This project uses SQL in Databricks to analyse Sizwe Coffee's sales and business performance. The aim was to answer eight business questions and provide insights that can help management make data-driven decisions.

The analysis covers revenue growth, product profitability, outstanding invoices, customer performance, trade promotions, sales representative targets, monthly revenue trends and gross margin changes.

## Dataset

This project uses the Sizwe Coffee business dataset provided for analysis during my SQL training.

The dataset contains business information relating to sales orders, sales transactions, products, customers, sales representatives, trade promotions and accounts receivable.

Main Tables Used
| Table              | Description                                                                        |
|--------------------|------------------------------------------------------------------------------------|
| sizwe_sales_orders | Sales order information, including order dates and order IDs.                      |
| sizwe_sales_lines  | Sales transaction details, including product SKUs, revenue and cost of goods sold. |
| sizwe_products     | Product information and product-line classifications.                              |
| sizwe_ar_ledger    | Invoice and payment information used to analyse accounts receivable.               |

                                     
Additional tables were used where required for customer details, sales representatives, sales targets and trade promotions.

Data source: Training dataset provided for the Sizwe Coffee SQL project. The dataset is not included in this repository.

## Tools Used

- SQL
- Databricks
- GitHub

## Business Questions

This project addresses eight business questions:

1. **Revenue by Channel:** Compared Wholesale and Subscription revenue and calculated growth rates.
2. **Product Profitability:** Analysed revenue, cost of goods sold, gross profit and gross margin by product line.
3. **Accounts Receivable:** Investigated invoice settlement times, open invoices and outstanding balances.
4. **Top Customers:** Identified the ten highest-revenue customers for FY2025.
5. **Trade Promotions:** Identified high-revenue Wholesale customers who had never received a trade promotion.
6. **Sales Performance:** Compared sales representatives' average monthly revenue with their targets.
7. **Monthly Revenue Trends:** Analysed monthly revenue, month-on-month changes and rolling three-month averages.
8. **Gross Margin Analysis:** Investigated why overall gross margin declined despite revenue growth.

## SQL Skills Demonstrated

- Common Table Expressions (CTEs)
- INNER JOIN and LEFT JOIN
- Aggregate functions: SUM, COUNT and AVG
- CASE WHEN statements
- Date filtering and date functions
- GROUP BY and ORDER BY
- Window functions, including LAG and rolling averages
- Percentage calculations
- Data validation and quality checks

## Key Findings

### 1. Revenue Growth

Wholesale revenue increased from approximately R308.17 million to R335.43 million, while Subscription revenue increased from R132.83 million to R144.57 million. Both channels recorded growth of approximately 8.8% across the periods defined in the analysis.

### 2. Product Profitability

House Blend generated the highest absolute gross profit, while Single Origin achieved the highest gross margin percentage. This shows the difference between generating the most profit in rand terms and achieving the highest margin.

### 3. Accounts Receivable

Wholesale was the main collections concern.

- Wholesale had 3,454 open invoices and approximately R87.85 million outstanding.
- Its average invoice settlement time was 68.68 days.
- Subscription had 44 open invoices and approximately R751,178.89 outstanding.
- Its average settlement time was 3.85 days.

**Recommendation:** Prioritise Wholesale collections and investigate overdue accounts to reduce outstanding balances.

### 4. Customer Performance

The top-customer analysis identified the largest FY2025 revenue contributors and provided visibility into their customer segments, provinces and assigned sales representatives.

**Recommendation:** Use these results to support key-account management and customer retention strategies.

### 5. Trade Promotion Opportunities

Three high-revenue Wholesale customers identified for potential trade promotions were:

- Umhlanga Fresh 108 — R6.22 million
- Ridgeway Foods 308 — R4.45 million
- Kalahari Kitchen 42 — R4.45 million

**Recommendation:** Evaluate targeted promotions for these accounts and measure their impact on sales and customer retention.

### 6. Sales Representative Performance

All 15 sales representatives exceeded their monthly targets based on their calculated FY2025 monthly revenue averages.

- Karabo van Wyk achieved 250.32% of target.
- Kagiso Mkhize achieved 249.82%.
- Bongani Mahlangu recorded the lowest result at 116.06%, while still exceeding target.

**Recommendation:** Review whether sales targets are appropriately calibrated across territories.

### 7. Monthly Revenue Trends

The analysis showed a recurring decline in revenue during December, followed by a recovery in the new year.

December 2023 was the quietest month, with revenue of approximately R29.87 million. December 2024 also recorded a month-on-month decline of 12.89%.

**Recommendation:** Consider seasonal patterns when planning sales campaigns, inventory and revenue targets.

### 8. Gross Margin Decline

The overall gross margin declined from 34.7% in FY2024 to 33.0% in FY2025, despite revenue growth.

Bulk Commercial's share of total revenue increased from 25.02% to 33.65%, while its gross margin remained approximately 19.9%. Over the same period, House Blend's revenue share decreased from 32.14% to 28.71%, and Single Origin's share decreased from 19.45% to 17.57%.

This suggests that the shift towards the lower-margin Bulk Commercial product line was the main contributor to the decline in overall gross margin.

**Recommendation:** Investigate opportunities to improve Bulk Commercial profitability and support sales of higher-margin product lines.

## Data Quality

Validation checks were performed as part of the accounts receivable analysis. The tested checks found no customers mapped to multiple channels, no partially paid invoices under the check used, and no missing amounts under the validation performed.

LEFT JOINs were used where appropriate to retain records such as customers without assigned sales representatives and sales representatives without revenue.

## Project Code

The eight SQL queries were developed and executed in Databricks. They cover the business questions described above and demonstrate practical SQL skills applied to a business dataset.

## How to Run the SQL Queries

All eight SQL queries for this project were developed and executed in a Databricks notebook. The notebook contains the SQL code used to answer the eight business questions, along with the query results.

Databricks Notebook: https://github.com/YamkelaCenenda/WitleAcademyProject-/blob/main/queries.sql.ipynb

## Steps to Run the Project

 1. Click the Databricks notebook link above.
 2. Sign in to Databricks and ensure you have permission to access the notebook.
 3. Ensure the Sizwe Coffee training dataset and required tables are available in your workspace.
 4. Run each SQL query in the notebook.
 5. Review the results alongside the business insights and recommendations in this README.

## Requirements:

- Access to a Databricks workspace.
- Access to the Sizwe Coffee training dataset.
- Permission to query the relevant tables.

**Note**: The notebook and dataset are maintained separately from this GitHub repository. Access to the notebook may require additional permissions.

## Conclusion

This project demonstrates how SQL can be used to analyse business performance, identify risks and opportunities, and translate data into practical recommendations.

It forms part of my data analytics learning journey and portfolio as I develop my skills in SQL, data analysis and business intelligence.

## Author

Aspiring Data Analyst | SQL | Databricks | Business Analysis
