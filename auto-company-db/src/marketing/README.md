# Marketing Department Interface
**Owner:** David Oladipupo

Your task is to build the reporting tools for the corporate marketing team using complex OLAP queries.

### 🛠️ Required Features & SQL Logic
1. **3-Year Sales Trend:** Group sales over the last 3 years by year, month, customer gender, and income range.
2. **Top Brands:** Return the top 2 brands by total revenue (`SUM(sale_price)`) and total units sold (`COUNT(sale_id)`) over the past year.
3. **Seasonal Data:** Identify the best-selling months for specific body styles, like convertibles.
4. **Review Inquiries:** Fetch and display the unfulfilled customer requests logged by the Dealer Interface.

### 🖥️ Expected Command-Line Interface
When a user selects your role from the main menu, your Python code should print this exact menu:

```text
--- 📊 Marketing Department Menu ---
[1] Generate 3-Year Sales Trend Report (OLAP)
[2] View Top Performing Brands (Revenue & Units)
[3] View Seasonal Convertible Sales Data
[4] Review Unfulfilled Customer Inquiries
[5] Return to Main Menu
