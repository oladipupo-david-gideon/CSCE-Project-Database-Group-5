from db_queries import DBQueries
from utils import print_dynamic_table

class CustomerMenu:
    def __init__(self, db_connection):
        self.queries = DBQueries(db_connection)

    def show_menu(self):
        print("\n--- 🛒 Online Customer Menu ---")
        print("1. Search Dealerships by Location")
        print("2. Browse Vehicle Catalog")
        print("3. Search Inventory for Specific Model")
        print("4. Return to Main Menu")

    def search_dealerships(self):
        print("\n[Executing: Dealership Search]")
        city = input("Enter city (or press Enter to skip): ")
        state = input("Enter state (or press Enter to skip): ")

        try:
            results = self.queries.search_dealerships(city, state)
            headers = ["Dealership Name", "Address", "City", "State", "Phone"]
            print_dynamic_table(headers, results)
        except Exception as e:
            print(f"Error searching dealerships: {e}")

    def browse_catalog(self):
        print("\n[Executing: Vehicle Catalog]")
        try:
            results = self.queries.get_vehicle_catalog()
            headers = ["Brand", "Model", "Style", "Year", "Engine", "Transmission", "Color"]
            print_dynamic_table(headers, results)
        except Exception as e:
            print(f"Error loading catalog: {e}")

    def search_inventory(self):
        print("\n[Executing: Inventory Search]")
        model = input("Enter model name: ")

        try:
            results = self.queries.search_available_inventory(model)
            
            # Format the price with $ and commas before sending to dynamic table
            formatted_results = []
            for row in results:
                formatted_results.append([row[0], row[1], f"${row[2]:,.2f}", row[3]])
                
            headers = ["Model Name", "Dealership", "Price", "Date Arrived"]
            print_dynamic_table(headers, formatted_results)
        except Exception as e:
            print(f"Error searching inventory: {e}")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Enter choice (1-4): ")

            if choice == "1":
                self.search_dealerships()
            elif choice == "2":
                self.browse_catalog()
            elif choice == "3":
                self.search_inventory()
            elif choice == "4":
                print("\nReturning to main menu...")
                break
            else:
                print("\nInvalid choice. Try again.")