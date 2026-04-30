import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import sys

# Import the Class objects instead of functions
from customer.customer_menu import CustomerMenu
from dealer.dealer_menu import DealerMenu
from marketing.marketing_menu import MarketingMenu
from dba.dba_menu import DBAMenu

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def get_db_url(self):
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "postgres")
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASS")

        if not all([host, user, password]):
            return None
            
        return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    def connect(self):
        print("\n--- Database Initialization ---")
        db_url = self.get_db_url()
        
        if not db_url:
            print("❌ Error: Missing database credentials in .env file.")
            return False

        try:
            self.connection = psycopg2.connect(db_url)
            self.cursor = self.connection.cursor()
            print("✅ Successfully connected to the Auto Company Database (Supabase)!")
            return True

        except (Exception, Error) as error:
            print(f"\n❌ Error connecting to PostgreSQL: {error}")
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("\nDatabase connection closed. Goodbye!")

def main():
    db = DatabaseConnection()
    
    if not db.connect():
        sys.exit(1)

    while True:
        print("\n===========================================")
        print(" Welcome to the Auto Company Database System ")
        print("===========================================")
        print("Please select your role:")
        print("1. Online Customer")
        print("2. Dealer (Vehicle Locator Service)")
        print("3. Marketing Department")
        print("4. Database Administrator (DBA)")
        print("5. Exit System")
        print("===========================================")
        
        choice = input("Enter choice (1-5): ")

        if choice == '1':
            print("\n--> Launching Customer Interface...")
            customer_ui = CustomerMenu(db)
            customer_ui.run()
            
        elif choice == '2':
            print("\n--> Launching Dealer Interface...")
            dealer_ui = DealerMenu(db)
            dealer_ui.run()
            
        elif choice == '3':
            print("\n--> Launching Marketing Interface...")
            marketing_ui = MarketingMenu(db)
            marketing_ui.run()
            
        elif choice == '4':
            print("\n--> Launching DBA Interface...")
            dba_ui = DBAMenu(db)
            dba_ui.run()
            
        elif choice == '5':
            print("\nExiting system...")
            db.close()
            break
            
        else:
            print("\nInvalid selection. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()