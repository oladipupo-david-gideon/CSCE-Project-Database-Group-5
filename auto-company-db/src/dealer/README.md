# Dealer Interface (Vehicle Locator)
**Owner:** Snehitha Paruchi

Your task is to build the CLI menu for dealership employees to manage stock and process sales.

### 🛠️ Required Features & SQL Logic
1. **View Local Inventory:** Query the `Inventory` table filtering by a specific `dealer_id`.
2. **Global Vehicle Locator:** Query the `Inventory` table across *all* dealers for a specific VIN or Model.
3. **Log Unfulfilled Customer Request:** Log the customer's desired specs (brand, model, color) so the Marketing department can review it later.
4. **Process Sale:** Execute an `INSERT INTO Sale` and an `UPDATE Inventory SET status = 'sold'` for a specific VIN.

### 🖥️ Expected Command-Line Interface
When a user selects your role from the main menu, your Python code should print this exact menu:

```text
--- 🏢 Dealer Menu ---
[1] View Local Inventory
[2] Locate Vehicle at Other Dealerships
[3] Log Unfulfilled Customer Request
[4] Process New Vehicle Sale
[5] Return to Main Menu
