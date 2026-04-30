from db_queries import DBQueries
from utils import print_dynamic_table

class DealerMenu:
    def __init__(self, db_connection):
        self.queries = DBQueries(db_connection)

    def show_menu(self):
        print("\n--- 🏢 Dealer Menu ---")
        print("[1] View Local Inventory")
        print("[2] Locate Vehicle at Other Dealerships")
        print("[3] Log Unfulfilled Customer Request")
        print("[4] Process New Vehicle Sale")
        print("[5] Return to Main Menu")

    # ------------------------------------------------------------------
    # Shared lookup helpers
    # ------------------------------------------------------------------

    def _get_dealer_id(self):
        search = input("Enter dealership name (or part of it): ").strip()
        if not search:
            print("Dealership name cannot be empty.")
            return None
        try:
            results = self.queries.find_dealers(search)
        except Exception as e:
            print(f"Error searching dealers: {e}")
            return None
        if not results:
            print("No dealerships found matching that name.")
            return None
        if len(results) == 1:
            print(f"Found: {results[0][1]} ({results[0][2]}, {results[0][3]}) — ID: {results[0][0]}")
            return results[0][0]
        print_dynamic_table(["ID", "Dealership Name", "City", "State"], results)
        try:
            return int(input("Enter dealer ID from the list above: "))
        except ValueError:
            print("Invalid ID entered.")
            return None

    def _get_customer_id(self):
        search = input("Enter customer first or last name: ").strip()
        if not search:
            print("Customer name cannot be empty.")
            return None
        try:
            results = self.queries.find_customers(search)
        except Exception as e:
            print(f"Error searching customers: {e}")
            return None
        if not results:
            print("No customers found matching that name.")
            return None
        if len(results) == 1:
            print(f"Found: {results[0][1]} (Phone: {results[0][2]}) — ID: {results[0][0]}")
            return results[0][0]
        print_dynamic_table(["ID", "Customer Name", "Phone"], results)
        try:
            return int(input("Enter customer ID from the list above: "))
        except ValueError:
            print("Invalid ID entered.")
            return None

    def _get_model_id(self):
        search = input("Enter desired model name (or press Enter to skip): ").strip()
        if not search:
            return None
        try:
            results = self.queries.find_model(search)
        except Exception as e:
            print(f"Error searching models: {e}")
            return None
        if not results:
            print("No matching models found — inquiry will be logged without a specific model.")
            return None
        if len(results) == 1:
            print(f"Found: {results[0][2]} {results[0][1]} — ID: {results[0][0]}")
            return results[0][0]
        print_dynamic_table(["ID", "Model Name", "Brand"], results)
        try:
            return int(input("Enter model ID from the list above: "))
        except ValueError:
            print("Invalid ID — inquiry will be logged without a specific model.")
            return None

    # ------------------------------------------------------------------
    # Feature 1 — View Local Inventory
    # ------------------------------------------------------------------

    def view_local_inventory(self):
        print("\n[Executing: View Local Inventory]")
        dealer_id = self._get_dealer_id()
        if dealer_id is None:
            return
        try:
            results = self.queries.get_local_inventory(dealer_id)
            if not results:
                print("No available vehicles in local inventory.")
                return
            formatted = [[row[0], row[1], row[2], f"${row[3]:,.2f}", row[4]] for row in results]
            headers = ["VIN", "Model Name", "Color", "Price", "Date Received"]
            print_dynamic_table(headers, formatted)
        except Exception as e:
            print(f"Error loading local inventory: {e}")

    # ------------------------------------------------------------------
    # Feature 2 — Global Vehicle Locator
    # ------------------------------------------------------------------

    def locate_vehicle(self):
        print("\n[Executing: Global Vehicle Locator]")
        search = input("Enter VIN or model name to search across all dealerships: ").strip()
        if not search:
            print("Search term cannot be empty.")
            return
        try:
            results = self.queries.locate_vehicle_globally(search)
            if not results:
                print("No matching vehicles found in any dealership inventory.")
                return
            formatted = [[row[0], row[1], row[2], row[3], row[4], f"${row[5]:,.2f}"] for row in results]
            headers = ["Dealership Name", "City", "State", "VIN", "Model", "Price"]
            print_dynamic_table(headers, formatted)
        except Exception as e:
            print(f"Error locating vehicle: {e}")

    # ------------------------------------------------------------------
    # Feature 3 — Log Unfulfilled Customer Request
    # ------------------------------------------------------------------

    def log_unfulfilled_request(self):
        print("\n[Executing: Log Unfulfilled Customer Request]")
        customer_id = self._get_customer_id()
        if customer_id is None:
            return
        dealer_id = self._get_dealer_id()
        if dealer_id is None:
            return
        model_id = self._get_model_id()
        notes = input("Enter notes about the customer's request: ").strip()
        notes = notes if notes else None
        try:
            self.queries.log_customer_inquiry(customer_id, dealer_id, model_id, notes)
            print("✅ Customer inquiry logged successfully with status 'Unfulfilled'.")
        except Exception as e:
            self.queries.rollback()
            print(f"Error logging inquiry: {e}")

    # ------------------------------------------------------------------
    # Feature 4 — Process New Vehicle Sale
    # ------------------------------------------------------------------

    def process_sale(self):
        print("\n[Executing: Process New Vehicle Sale]")
        vin = input("Enter VIN of the vehicle being sold: ").strip().upper()
        if not vin:
            print("VIN cannot be empty.")
            return
        dealer_id = self._get_dealer_id()
        if dealer_id is None:
            return
        customer_id = self._get_customer_id()
        if customer_id is None:
            return
        try:
            sale_price = float(input("Enter final sale price: $"))
            if sale_price <= 0:
                print("Sale price must be greater than zero.")
                return
        except ValueError:
            print("Invalid price — please enter a numeric value.")
            return
        try:
            self.queries.process_sale(vin, dealer_id, customer_id, sale_price)
            print(f"✅ Sale processed successfully for VIN: {vin}")
            print(f"   Vehicle marked as 'sold'. Inventory record updated with today's date.")
        except ValueError as e:
            print(f"Cannot process sale: {e}")
        except Exception as e:
            self.queries.rollback()
            print(f"Error processing sale: {e}")

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self):
        while True:
            self.show_menu()
            choice = input("Enter choice (1-5): ")

            if choice == "1":
                self.view_local_inventory()
            elif choice == "2":
                self.locate_vehicle()
            elif choice == "3":
                self.log_unfulfilled_request()
            elif choice == "4":
                self.process_sale()
            elif choice == "5":
                print("\nReturning to main menu...")
                break
            else:
                print("\nInvalid choice. Try again.")
