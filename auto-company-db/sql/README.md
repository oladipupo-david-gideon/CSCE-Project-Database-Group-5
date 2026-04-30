# Database Administration
**Owner:** Ronitkumar Sabhaya

Your task is to manage the database architecture and ensure our schema meets all project requirements. 

This folder contains the master `.sql` files used to build the database, which is currently hosted on **Supabase PostgreSQL**.

### 📋 Responsibilities:
* Maintain the `schema.sql` file (all `CREATE TABLE` commands).
* Maintain the `dummy_data.sql` file (all `INSERT` commands for testing).
* Maintain the `.env` file configuration to ensure secure database connection credentials (`DB_HOST`, `DB_USER`, `DB_PASS`, etc.) load properly.
* Ensure the E-R diagram perfectly matches our final tables before submission.

### 🛠️ Required Features & SQL Logic
Within the main application, the DBA role is responsible for the following interactive menu operations:
1. **System Maintenance (Raw SQL):** Execute raw SQL scripts directly through the CLI to build tables, manage indices, and troubleshoot concurrency issues.
2. **Supplier Defect Trace:** Run complex ad-hoc queries to find all cars with defective parts (e.g., Getrag transmissions) and trace their corresponding production and customer contact info.
3. **Stagnant Inventory Identification:** Query the database to identify vehicles that have been sitting in inventory the longest to assist with dealer adjustments.

### 🖥️ Expected Interface
The DBA is integrated directly into the main application via a custom Python CLI menu (`DBAMenu`), accessible by selecting **Option 4** on the main system welcome screen. 

**The DBA Menu includes:**
* `[1]` Execute Raw SQL Query
* `[2]` Run Supplier Defect Trace
* `[3]` Identify Stagnant Inventory
* `[4]` Return to Main Menu

*Note: While the CLI handles application-level database tasks, direct administrative access for heavy backend work is still available via standard command-line tools (`psql`) or graphical clients like **pgAdmin4** connected to your Supabase credentials.*