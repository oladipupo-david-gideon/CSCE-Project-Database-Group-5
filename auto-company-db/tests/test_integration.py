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
        except Exception as e:
            self.skipTest(f"Database connection failed, skipping integration tests: {e}")

    def tearDown(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def test_connection(self):
        self.assertIsNotNone(self.conn)

    def test_execute_simple_query(self):
        columns, results = self.db_queries.execute_raw_sql("SELECT 1 AS test_col;")
        self.assertEqual(columns, ["test_col"])
        self.assertEqual(results[0][0], 1)

if __name__ == '__main__':
    unittest.main()
