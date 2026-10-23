# Databricks notebook source
# MAGIC %sql
# MAGIC -- Task 1: Channel performance
# MAGIC
# MAGIC with Revenue_Summary as (
# MAGIC      select o.channel, 
# MAGIC           round (sum (case when 
# MAGIC           order_date <= '2024-06-30'
# MAGIC             then l.line_revenue
# MAGIC           else 0 end),2) as Revenue24, 
# MAGIC      round (sum ( case when 
# MAGIC         order_date > '2024-06-30'
# MAGIC            then l.line_revenue
# MAGIC         else 0 end),2) as Revenue25
# MAGIC           
# MAGIC from sizwe_sales_orders as o
# MAGIC inner join sizwe_sales_lines as l
# MAGIC on o.order_id = l.order_id
# MAGIC group by o.channel )
# MAGIC
# MAGIC select channel, Revenue24, Revenue25, 
# MAGIC round(((Revenue25 - Revenue24)/nullif (Revenue24,0))*100,1) as Growth_Rate 
# MAGIC from Revenue_Summary 
# MAGIC

# COMMAND ----------

# MAGIC %sql 
# MAGIC -- Task 2: Where the profit actually comes from?
# MAGIC
# MAGIC with Revenue_Summary as (
# MAGIC     select o.channel, 
# MAGIC         round (sum (case when 
# MAGIC         order_date <= '2024-06-30'
# MAGIC            then l.line_revenue
# MAGIC         else 0 end),2) as Revenue24,
# MAGIC
# MAGIC round (sum ( case when 
# MAGIC     order_date > '2024-06-30'
# MAGIC        then l.line_revenue
# MAGIC     else 0 end),2) as Revenue25
# MAGIC       
# MAGIC from sizwe_sales_orders as o
# MAGIC inner join sizwe_sales_lines as l
# MAGIC on o.order_id = l.order_id
# MAGIC group by o.channel )
# MAGIC
# MAGIC select channel, Revenue24, Revenue25, 
# MAGIC round(((Revenue25 - Revenue24)/nullif (Revenue24,0))*100,1) as Growth_Rate 
# MAGIC from Revenue_Summary;
# MAGIC
# MAGIC with Margins as (
# MAGIC     select p.product_line as Product_Line,
# MAGIC     round(sum(line_revenue),2) as Total_Revenue,
# MAGIC     round(sum(cogs),2) as Total_Cost, 
# MAGIC     round(sum(line_revenue) - sum(cogs),2) as Gross_Profit, 
# MAGIC     round(((sum(line_revenue) - sum(cogs)) / nullif(sum(line_revenue),0)*100),2) as Gross_Mar_Per
# MAGIC from sizwe_sales_lines sl
# MAGIC inner join sizwe_products p
# MAGIC on sl.sku = p.sku
# MAGIC group by p.product_line
# MAGIC )
# MAGIC
# MAGIC select Product_Line, Total_Revenue, Total_Cost,Gross_Profit, Gross_Mar_Per
# MAGIC from Margins
# MAGIC order by Gross_Profit desc
# MAGIC
# MAGIC --- The House Blend line earns the highest absolute gross profit. However, it is not the same line that achieves the highest efficiency, as the highest gross margin percentage belongs to the Single Origin line.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Task 3 : The collections problem
# MAGIC
# MAGIC with customer_channels as (
# MAGIC     select distinct customer_id, channel
# MAGIC     from sizwe_ar_ledger
# MAGIC     where channel is not null
# MAGIC     )
# MAGIC
# MAGIC select
# MAGIC     c.channel,
# MAGIC     count(*) as Total_Invoices,
# MAGIC     count(case when i.amount_settled > 0 then 1 end) as Settled_Invoices,
# MAGIC     count(case when i.amount_settled = 0 then 1 end) as Open_Invoices,
# MAGIC     round(avg(case
# MAGIC         when i.settlement_date is not null
# MAGIC         then datediff(i.settlement_date, i.invoice_date)
# MAGIC         end), 2 ) as Avg_Days_to_Settle,
# MAGIC     round(sum(i.invoice_amount - i.amount_settled), 2) as Total_Outstanding_Value
# MAGIC from sizwe_ar_ledger as i
# MAGIC inner join customer_channels as c
# MAGIC on i.customer_id = c.customer_id
# MAGIC where i.invoice_no is not null
# MAGIC group by c.channel
# MAGIC order by Total_Outstanding_Value desc 
# MAGIC
# MAGIC --- Wholesale is the main collections concern, with 3,454 open invoices worth R87,848,227.20 and an average settlement time of 68.68 days. In comparison, Subscription has only 44 open invoices worth R751,178.89 and an average settlement time of 3.85 days. Nomsa should investigate the Wholesale channel first because it has substantially more outstanding debt and slower collections.
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Task 4 : The ten accounts that matter most
# MAGIC
# MAGIC with Revenue_Summary as(
# MAGIC     select
# MAGIC     c.customer_id, 
# MAGIC     c.trading_name,
# MAGIC     c.segment,
# MAGIC     c.province,
# MAGIC     round(sum(case when o.order_date between '2024-07-01' and '2025-06-30' 
# MAGIC         then l.line_revenue 
# MAGIC         else 0 end), 2) as Revenue25  
# MAGIC     from sizwe_sales_orders as o
# MAGIC     inner join sizwe_sales_lines as l on o.order_id = l.order_id
# MAGIC     inner join sizwe_customers as c on o.customer_id = c.customer_id 
# MAGIC     group by c.customer_id, c.trading_name, c.segment, c.province
# MAGIC )
# MAGIC select 
# MAGIC      r.trading_name, 
# MAGIC      r.segment, 
# MAGIC      r.province, 
# MAGIC      max(sr.rep_name) as Sales_Rep,
# MAGIC      r.Revenue25 
# MAGIC from Revenue_Summary as r
# MAGIC left join sizwe_rep_visits as v on r.customer_id = v.customer_id
# MAGIC left join sizwe_reps as sr on v.rep_id = sr.rep_id
# MAGIC group by r.trading_name, r.segment, r.province, r.Revenue25
# MAGIC order by r.Revenue25 desc
# MAGIC limit 10
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql 
# MAGIC -- Task 5 : A commercial gap
# MAGIC
# MAGIC with Customer_Revenue as (
# MAGIC     select 
# MAGIC         c.customer_id,
# MAGIC         c.trading_name,
# MAGIC         c.channel,      
# MAGIC         c.segment,
# MAGIC         c.province,
# MAGIC         round(sum(l.line_revenue), 2) as Total_Revenue
# MAGIC     from sizwe_customers as c
# MAGIC     inner join sizwe_sales_orders as o on c.customer_id = o.customer_id
# MAGIC     inner join sizwe_sales_lines as l on o.order_id = l.order_id
# MAGIC     group by c.customer_id, c.trading_name, c.channel, c.segment, c.province
# MAGIC )
# MAGIC
# MAGIC select cr.trading_name, cr.channel, cr.segment, cr.province, cr.Total_Revenue
# MAGIC from customer_revenue as cr
# MAGIC left join sizwe_trade_promotions as p 
# MAGIC on cr.customer_id = p.customer_id
# MAGIC where cr.channel = "Wholesale"  
# MAGIC and p.customer_id is null
# MAGIC order by cr.total_revenue desc
# MAGIC limit 15 
# MAGIC
# MAGIC --- I recommend proactively reaching out to the top three wholesale customers to offer them tailored trade promotions or volume-based discounts to reward their loyalty, secure their accounts, and prevent them from churning to competitors
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql 
# MAGIC --Task 6 : Are the sales representatives hitting target?
# MAGIC
# MAGIC with Rep_Revenue_Summary as (
# MAGIC select 
# MAGIC    r.rep_name,
# MAGIC    r.territory,
# MAGIC    r.target_monthly,
# MAGIC    round(sum( case 
# MAGIC         when o.order_date between '2024-07-01' and '2025-06-30'
# MAGIC         then l.line_revenue
# MAGIC         else 0 end),2) as total_revenue 
# MAGIC from sizwe_reps as r
# MAGIC left join sizwe_sales_orders as o
# MAGIC on o.rep_id = r.rep_id
# MAGIC left join sizwe_sales_lines as l
# MAGIC on o.order_id = l.order_id
# MAGIC group by r.rep_name, r.territory, r.target_monthly 
# MAGIC )
# MAGIC
# MAGIC select rs.rep_name,
# MAGIC        rs.territory,
# MAGIC        rs.target_monthly,
# MAGIC        round (rs.total_revenue / 12,2) as avg_mon_rev,
# MAGIC        round ((avg_mon_rev / target_monthly)*100,2) 
# MAGIC        as avg_mon_rev_per
# MAGIC from Rep_Revenue_Summary as rs
# MAGIC order by avg_mon_rev_per desc
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql 
# MAGIC -- Task 7 : The shape of the year
# MAGIC
# MAGIC with Monthly_Revenue as (
# MAGIC     select 
# MAGIC     date_trunc ('month', o.order_date)
# MAGIC     as Revenue_Month,  
# MAGIC     round(sum (l.line_revenue),2) 
# MAGIC     as Month_Revenue
# MAGIC
# MAGIC     from sizwe_sales_orders as o
# MAGIC     inner join sizwe_sales_lines as l
# MAGIC     on o.order_id = l.order_id
# MAGIC     where o.order_date between '2023-07-01' and '2025-06-30'
# MAGIC     group by date_trunc ('month', o.order_date)
# MAGIC ),
# MAGIC
# MAGIC Revenue_Analysis as (
# MAGIC     select   
# MAGIC        Revenue_Month, 
# MAGIC        Month_Revenue,
# MAGIC        lag(Month_Revenue,1) 
# MAGIC        over(order by Revenue_Month)as Previous_Mon_Revenue,
# MAGIC        avg(Month_Revenue)
# MAGIC        over(order by Revenue_Month
# MAGIC        rows between 2 preceding and current row)
# MAGIC        as Rolling_3Month_Avg   
# MAGIC        from Monthly_Revenue 
# MAGIC )
# MAGIC
# MAGIC select 
# MAGIC        Revenue_Month, 
# MAGIC        Month_Revenue,
# MAGIC        Previous_Mon_Revenue,
# MAGIC        round(100*(Month_Revenue - Previous_Mon_Revenue)/nullif(Previous_Mon_Revenue,0),2) as Percentage_Change,
# MAGIC        round(Rolling_3Month_Avg,2) as Rolling_3Month_Avg
# MAGIC        from Revenue_Analysis
# MAGIC        order by Revenue_Month;
# MAGIC
# MAGIC
# MAGIC --Sizwe's revenue shows a seasonal pattern, with higher revenue generally occurring between July and September and lower revenue during December and January, suggesting a possible slowdown around the festive season and start of the new year. December 2023 was Sizwe's quietest month, recording monthly revenue of R29,872,699.78.

# COMMAND ----------

# MAGIC %sql 
# MAGIC -- Task 8 : Why has the margin moved?
# MAGIC
# MAGIC with Product_Line_Revenue as (
# MAGIC     select
# MAGIC         case
# MAGIC             when o.order_date >= '2023-07-01'
# MAGIC             and o.order_date < '2024-07-01'
# MAGIC                 then 'FY2024'
# MAGIC             when o.order_date >= '2024-07-01'
# MAGIC             and o.order_date < '2025-07-01'
# MAGIC                 then 'FY2025'
# MAGIC         end as Financial_Year,
# MAGIC
# MAGIC         p.product_line,
# MAGIC         sum(l.line_revenue) as Revenue,
# MAGIC         sum(l.cogs) as COGS
# MAGIC
# MAGIC     from sizwe_sales_orders as o
# MAGIC     inner join sizwe_sales_lines as l
# MAGIC         on o.order_id = l.order_id
# MAGIC     inner join sizwe_products as p
# MAGIC         on l.sku = p.sku
# MAGIC
# MAGIC     where o.order_date >= '2023-07-01'
# MAGIC     and o.order_date < '2025-07-01'
# MAGIC
# MAGIC     group by
# MAGIC         case
# MAGIC             when o.order_date >= '2023-07-01'
# MAGIC             and o.order_date < '2024-07-01'
# MAGIC                 then 'FY2024'
# MAGIC             when o.order_date >= '2024-07-01'
# MAGIC             and o.order_date < '2025-07-01'
# MAGIC                 then 'FY2025'
# MAGIC         end,
# MAGIC         p.product_line
# MAGIC ),
# MAGIC
# MAGIC Product_Line_Analysis as (
# MAGIC     select
# MAGIC         Financial_Year,
# MAGIC         product_line,
# MAGIC         Revenue,
# MAGIC         COGS,
# MAGIC
# MAGIC         100 * (Revenue - COGS)
# MAGIC             / NULLIF(Revenue, 0) as Gross_Margin_Pct,
# MAGIC
# MAGIC         100 * Revenue
# MAGIC             / sum(Revenue) over (
# MAGIC                 partition by Financial_Year
# MAGIC             ) as Revenue_Share_Pct
# MAGIC
# MAGIC     from Product_Line_Revenue
# MAGIC )
# MAGIC
# MAGIC select
# MAGIC     Financial_Year,
# MAGIC     product_line,
# MAGIC     round(Revenue, 2) as Revenue,
# MAGIC     round(Gross_Margin_Pct, 2) as Gross_Margin_Pct,
# MAGIC     round(Revenue_Share_Pct, 2) as Revenue_Share_Pct
# MAGIC
# MAGIC from Product_Line_Analysis
# MAGIC order by
# MAGIC     Financial_Year,
# MAGIC     product_line
# MAGIC
# MAGIC --The gross margin declined from 34.7% in FY2024 to 33.0% in FY2025 mainly because of a shift in the revenue mix towards Bulk Commercial, which has a much lower gross margin than the other product lines. Bulk Commercial's revenue share increased from 25.02% to 33.65%, while its margin remained around 19.9%; meanwhile, House Blend's share fell from 32.14% to 28.71% and Single Origin's from 19.45% to 17.57%, despite both maintaining margins above 38%. This indicates that the decline was driven primarily by selling a larger proportion of lower-margin products rather than a major deterioration in individual product-line margins.