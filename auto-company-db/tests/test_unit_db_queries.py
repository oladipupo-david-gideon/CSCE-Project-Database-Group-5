import unittest
from unittest.mock import MagicMock
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from db_queries import DBQueries

class TestDBQueriesUnit(unittest.TestCase):
    def setUp(self):
        # Mock database connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cur = MagicMock()
        
        class MockDBConnection:
            def __init__(self, conn, cur):
                self.connection = conn
                self.cursor = cur
                
        self.db_connection = MockDBConnection(self.mock_conn, self.mock_cur)
        self.db_queries = DBQueries(self.db_connection)

    def test_search_dealerships(self):
        self.mock_cur.fetchall.return_value = [("Dealer A", "123 Main", "Dallas", "TX", "555-1234")]
        results = self.db_queries.search_dealerships("Dallas", "TX")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "Dealer A")
        self.mock_cur.execute.assert_called_once()

    def test_get_vehicle_catalog(self):
        self.mock_cur.fetchall.return_value = [("Toyota", "Camry", "Sedan", 2023, "V6", "Auto", "Red")]
        results = self.db_queries.get_vehicle_catalog()
        self.assertEqual(len(results), 1)
        self.mock_cur.execute.assert_called_once()

    def test_search_available_inventory(self):
        self.mock_cur.fetchall.return_value = [("Camry", "Dealer A", 25000.00, "2023-01-01")]
        results = self.db_queries.search_available_inventory("Camry")
        self.assertEqual(len(results), 1)
        self.mock_cur.execute.assert_called_once()

    def test_get_3_year_sales_trend(self):
        self.mock_cur.fetchall.return_value = [(2023, 1, 10, 250000.00)]
        results = self.db_queries.get_3_year_sales_trend()
        self.assertEqual(results[0][3], 250000.00)
        self.mock_cur.execute.assert_called_once()

    def test_get_top_performing_brands(self):
        self.mock_cur.fetchall.return_value = [("Toyota", 50, 1250000.00)]
        results = self.db_queries.get_top_performing_brands()
        self.assertEqual(results[0][0], "Toyota")
        self.mock_cur.execute.assert_called_once()

    def test_get_seasonal_convertibles(self):
        self.mock_cur.fetchall.return_value = [(6, 15)]
        results = self.db_queries.get_seasonal_convertibles()
        self.assertEqual(results[0][1], 15)
        self.mock_cur.execute.assert_called_once()

    def test_get_unfulfilled_inquiries(self):
        self.mock_cur.fetchall.return_value = [("2023-05-01", "John Doe", "Dealer A", "Camry", "Wants red")]
        results = self.db_queries.get_unfulfilled_inquiries()
        self.assertEqual(len(results), 1)
        self.mock_cur.execute.assert_called_once()

    def test_execute_raw_sql_select(self):
        self.mock_cur.description = [("col1",)]
        self.mock_cur.fetchall.return_value = [("val1",)]
        columns, results = self.db_queries.execute_raw_sql("SELECT 1;")
        self.assertEqual(columns, ["col1"])
        self.assertEqual(results, [("val1",)])

    def test_execute_raw_sql_update(self):
        self.mock_cur.description = None
        columns, results = self.db_queries.execute_raw_sql("UPDATE t SET a = 1;")
        self.assertIsNone(columns)
        self.assertIsNone(results)
        self.mock_conn.commit.assert_called_once()

    def test_run_supplier_defect_trace(self):
        self.mock_cur.fetchall.return_value = [("VIN123", "Camry", "Brake Pad", "Supplier X", "John", "Doe", "555", "2023-01-01")]
        results = self.db_queries.run_supplier_defect_trace("Brake")
        self.assertEqual(len(results), 1)
        self.mock_cur.execute.assert_called_once()

    def test_get_stagnant_inventory(self):
        self.mock_cur.fetchall.return_value = [(1, "VIN123", "Camry", "2022-01-01", 500)]
        results = self.db_queries.get_stagnant_inventory()
        self.assertEqual(results[0][4], 500)
        self.mock_cur.execute.assert_called_once()

    def test_rollback(self):
        self.db_queries.rollback()
        self.mock_conn.rollback.assert_called_once()

    def test_get_local_inventory(self):
        self.mock_cur.fetchall.return_value = [("VIN123", "Camry", "Red", 25000, "2023-01-01")]
        results = self.db_queries.get_local_inventory(1)
        self.assertEqual(results[0][0], "VIN123")
        self.mock_cur.execute.assert_called_once()

    def test_locate_vehicle_globally(self):
        self.mock_cur.fetchall.return_value = [("Dealer A", "Dallas", "TX", "VIN123", "Camry", 25000)]
        results = self.db_queries.locate_vehicle_globally("Camry")
        self.assertEqual(len(results), 1)
        self.mock_cur.execute.assert_called_once()

    def test_find_dealers(self):
        self.mock_cur.fetchall.return_value = [(1, "Dealer A", "Dallas", "TX")]
        results = self.db_queries.find_dealers("Dealer A")
        self.assertEqual(len(results), 1)
        self.mock_cur.execute.assert_called_once()

    def test_find_customers(self):
        self.mock_cur.fetchall.return_value = [(1, "John Doe", "555-1234")]
        results = self.db_queries.find_customers("John")
        self.assertEqual(len(results), 1)
        self.mock_cur.execute.assert_called_once()

    def test_find_model(self):
        self.mock_cur.fetchall.return_value = [(1, "Camry", "Toyota")]
        results = self.db_queries.find_model("Camry")
        self.assertEqual(results[0][1], "Camry")
        self.mock_cur.execute.assert_called_once()

    def test_log_customer_inquiry(self):
        self.db_queries.log_customer_inquiry(1, 1, 1, "Notes")
        self.mock_cur.execute.assert_called_once()
        self.mock_conn.commit.assert_called_once()

    def test_process_sale_success(self):
        self.mock_cur.fetchone.return_value = (1,)  # Inventory ID exists
        self.db_queries.process_sale("VIN123", 1, 1, 25000)
        self.assertEqual(self.mock_cur.execute.call_count, 4)  # check, insert sale, update vehicle, update inventory
        self.mock_conn.commit.assert_called_once()

    def test_process_sale_vin_not_found(self):
        self.mock_cur.fetchone.return_value = None  # VIN not found
        with self.assertRaises(ValueError):
            self.db_queries.process_sale("VIN123", 1, 1, 25000)
        self.assertEqual(self.mock_cur.execute.call_count, 1)

if __name__ == '__main__':
    unittest.main()
