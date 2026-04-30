from db_queries import DBQueries
from utils import print_dynamic_table

class MarketingMenu:
    def __init__(self, db_connection):
        self.queries = DBQueries(db_connection)

    def show_menu(self):
        print("\n--- 📊 Marketing Department Menu ---")
        print("1. Generate 3-Year Sales Trend Report (OLAP)")
        print("2. View Top Performing Brands (Revenue & Units)")
        print("3. View Seasonal Convertible Sales Data")
        print("4. Review Unfulfilled Customer Inquiries")
        print("5. Return to Main Menu")

    def run_trend_report(self):
        print("\n[Executing: 3-Year Sales Trend Report]")
        try:
            results = self.queries.get_3_year_sales_trend()
            
            # Format numbers and currency
            formatted_results = [
                [int(row[0]), int(row[1]), row[2], f"${row[3]:,.2f}"] 
                for row in results
            ]
            
            headers = ["Year", "Month", "Units Sold", "Total Revenue"]
            print_dynamic_table(headers, formatted_results)
        except Exception as e:
            print(f"Error generating 3-Year Trend Report: {e}")

    def run_top_brands(self):
        print("\n[Executing: Top Performing Brands]")
        try:
            results = self.queries.get_top_performing_brands()
            
            # Format currency
            formatted_results = [
                [row[0], row[1], f"${row[2]:,.2f}"] 
                for row in results
            ]
            
            headers = ["Brand", "Units Sold", "Total Revenue"]
            print_dynamic_table(headers, formatted_results)
        except Exception as e:
            print(f"Error generating Top Brands Report: {e}")

    def run_seasonal_convertibles(self):
        print("\n[Executing: Seasonal Convertible Sales Data]")
        try:
            results = self.queries.get_seasonal_convertibles()
            formatted_results = [[int(row[0]), row[1]] for row in results]
            
            headers = ["Month", "Units Sold"]
            print_dynamic_table(headers, formatted_results)
        except Exception as e:
            print(f"Error generating Seasonal Convertible Data: {e}")

    def run_unfulfilled_inquiries(self):
        print("\n[Executing: Review Unfulfilled Customer Inquiries]")
        try:
            results = self.queries.get_unfulfilled_inquiries()
            
            if not results:
                print("\n✅ Great news! There are no unfulfilled inquiries.")
                return

            # Optionally truncate notes if they are massive
            formatted_results = []
            for row in results:
                notes = row[4] if row[4] else "No notes provided"
                notes_preview = (notes[:40] + '...') if len(notes) > 40 else notes
                formatted_results.append([row[0], row[1], row[2], row[3], notes_preview])

            headers = ["Date", "Customer Name", "Dealership", "Requested Model", "Notes"]
            print_dynamic_table(headers, formatted_results)
        except Exception as e:
            print(f"Error checking inquiries: {e}")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Enter choice (1-5): ")

            if choice == '1':
                self.run_trend_report()
            elif choice == '2':
                self.run_top_brands()
            elif choice == '3':
                self.run_seasonal_convertibles()
            elif choice == '4':
                self.run_unfulfilled_inquiries()
            elif choice == '5':
                print("\nReturning to Main Menu...")
                break
            else:
                print("\nInvalid selection. Try again.")