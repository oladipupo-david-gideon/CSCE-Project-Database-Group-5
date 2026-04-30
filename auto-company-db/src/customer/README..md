# Online Customer Interface
**Owner:** Shegofa Ahmadi

Your task is to build the CLI menu that allows a customer to browse the database.

### 🛠️ Required Features & SQL Logic
1. **Search Dealerships by Location:** Query the `Dealer` table by city/state to find the closest location.
2. **Browse Vehicle Catalog:** Query the `Brand`, `Model`, and `Options` tables to show what cars exist without needing a specific VIN.
3. **Search Inventory:** Query the `Inventory` table joined with `Dealer` to find a specific car model and display its listed price.

### 🖥️ Expected Command-Line Interface
When a user selects your role from the main menu, your Python code should print this exact menu:

```text
--- 🛒 Online Customer Menu ---
[1] Search Dealerships by Location
[2] Browse Vehicle Catalog
[3] Search Inventory for Specific Model
[4] Return to Main Menu
