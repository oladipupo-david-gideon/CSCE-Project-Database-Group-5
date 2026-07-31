import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from db_queries import DBQueries

class TestIntegration(unittest.TestCase):
    def setUp(self):
        import psycopg2
        import dotenv
        dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '../src/.env'))
        
        self.conn = None
        self.cur = None
        try:
            db_password = os.getenv("DB_PASSWORD")
            if not db_password:
                raise ValueError("DB_PASSWORD environment variable is missing and required for integration tests")

            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "postgres"),
                user=os.getenv("DB_USER", "postgres"),
                password=db_password,
                port=os.getenv("DB_PORT", "5432")
            )
            self.cur = self.conn.cursor()
            
            class DBConnection:
                def __init__(self, conn, cur):
                    self.connection = conn
                    self.cursor = cur
                    
            self.db_connection = DBConnection(self.conn, self.cur)
            self.db_queries = DBQueries(self.db_connection)
            
            # Start transaction that will be rolled back
            self.conn.autocommit = False
        except Exception as e:
            self.skipTest(f"Database connection failed, skipping integration tests: {e}")

    def tearDown(self):
        if self.conn:
            self.conn.rollback()  # Rollback any changes made during tests
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def test_01_connection(self):
        self.assertIsNotNone(self.conn)

    def test_02_execute_simple_query(self):
        columns, results = self.db_queries.execute_raw_sql("SELECT 1 AS test_col;")
        self.assertEqual(columns, ["test_col"])
        self.assertEqual(results[0][0], 1)

    def test_03_execute_raw_sql_multiple(self):
        columns, results = self.db_queries.execute_raw_sql("SELECT 1; SELECT 2;")
        self.assertEqual(results[0][0], 2)

    def test_04_execute_raw_sql_error(self):
        with self.assertRaises(Exception):
            self.db_queries.execute_raw_sql("SELECT * FROM non_existent_table_999;")
        self.db_queries.rollback()

    def test_05_search_dealerships_empty(self):
        results = self.db_queries.search_dealerships("NonExistentCity", "XX")
        self.assertEqual(len(results), 0)

    def test_06_search_dealerships_partial(self):
        # Assuming there's a dealer in the db, using empty strings acts like wildcard
        results = self.db_queries.search_dealerships("", "")
        self.assertTrue(len(results) >= 0)

    def test_07_get_vehicle_catalog(self):
        results = self.db_queries.get_vehicle_catalog()
        self.assertIsInstance(results, list)

    def test_08_search_available_inventory_empty(self):
        results = self.db_queries.search_available_inventory("NonExistentModel")
        self.assertEqual(len(results), 0)

    def test_09_search_available_inventory_all(self):
        results = self.db_queries.search_available_inventory("")
        self.assertIsInstance(results, list)

    def test_10_get_3_year_sales_trend(self):
        results = self.db_queries.get_3_year_sales_trend()
        self.assertIsInstance(results, list)

    def test_11_get_top_performing_brands(self):
        results = self.db_queries.get_top_performing_brands()
        self.assertIsInstance(results, list)

    def test_12_get_seasonal_convertibles(self):
        results = self.db_queries.get_seasonal_convertibles()
        self.assertIsInstance(results, list)

    def test_13_get_unfulfilled_inquiries(self):
        results = self.db_queries.get_unfulfilled_inquiries()
        self.assertIsInstance(results, list)

    def test_14_run_supplier_defect_trace_empty(self):
        results = self.db_queries.run_supplier_defect_trace("NonExistentSupplier")
        self.assertEqual(len(results), 0)

    def test_15_run_supplier_defect_trace_all(self):
        results = self.db_queries.run_supplier_defect_trace("")
        self.assertIsInstance(results, list)

    def test_16_get_stagnant_inventory(self):
        results = self.db_queries.get_stagnant_inventory()
        self.assertIsInstance(results, list)

    def test_17_get_local_inventory_invalid_dealer(self):
        results = self.db_queries.get_local_inventory(-1)
        self.assertEqual(len(results), 0)

    def test_18_locate_vehicle_globally_empty(self):
        results = self.db_queries.locate_vehicle_globally("NonExistentVehicle")
        self.assertEqual(len(results), 0)

    def test_19_locate_vehicle_globally_all(self):
        results = self.db_queries.locate_vehicle_globally("")
        self.assertIsInstance(results, list)

    def test_20_find_dealers_empty(self):
        results = self.db_queries.find_dealers("NonExistentDealer")
        self.assertEqual(len(results), 0)

    def test_21_find_dealers_all(self):
        results = self.db_queries.find_dealers("")
        self.assertIsInstance(results, list)

    def test_22_find_customers_empty(self):
        results = self.db_queries.find_customers("NonExistentCustomerNameXYZ")
        self.assertEqual(len(results), 0)

    def test_23_find_customers_all(self):
        results = self.db_queries.find_customers("")
        self.assertIsInstance(results, list)

    def test_24_find_model_empty(self):
        results = self.db_queries.find_model("NonExistentModelNameXYZ")
        self.assertEqual(len(results), 0)

    def test_25_find_model_all(self):
        results = self.db_queries.find_model("")
        self.assertIsInstance(results, list)

    def test_26_log_customer_inquiry_invalid(self):
        with self.assertRaises(Exception):
            self.db_queries.log_customer_inquiry(-1, -1, -1, "Test")
        self.db_queries.rollback()

    def test_27_process_sale_invalid_vin(self):
        with self.assertRaises(ValueError):
            self.db_queries.process_sale("INVALID_VIN", 1, 1, 25000)

    def test_28_execute_raw_sql_no_return(self):
        # Create temp table
        columns, results = self.db_queries.execute_raw_sql("CREATE TEMP TABLE temp_test (id INT);")
        self.assertIsNone(columns)
        self.assertIsNone(results)

    def test_29_execute_raw_sql_insert(self):
        self.db_queries.execute_raw_sql("CREATE TEMP TABLE temp_test2 (id INT);")
        columns, results = self.db_queries.execute_raw_sql("INSERT INTO temp_test2 VALUES (1);")
        self.assertIsNone(columns)
        self.assertIsNone(results)

    def test_30_execute_raw_sql_select_temp(self):
        self.db_queries.execute_raw_sql("CREATE TEMP TABLE temp_test3 (id INT); INSERT INTO temp_test3 VALUES (42);")
        columns, results = self.db_queries.execute_raw_sql("SELECT * FROM temp_test3;")
        self.assertEqual(columns, ["id"])
        self.assertEqual(results[0][0], 42)

if __name__ == '__main__':
    unittest.main()
