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

    def test_rollback(self):
        self.db_queries.rollback()
        self.mock_conn.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()
