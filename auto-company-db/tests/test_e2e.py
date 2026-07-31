import unittest
import subprocess
import os
import sys

class TestE2E(unittest.TestCase):
    def setUp(self):
        # Determine paths
        self.tests_dir = os.path.dirname(os.path.abspath(__file__))
        self.src_dir = os.path.join(self.tests_dir, '../src')
        self.main_path = os.path.join(self.src_dir, 'main.py')
        
        # We need a database connection to pass the initial connection check.
        if not os.getenv("DB_PASS") and not os.getenv("DB_PASSWORD"):
            self.skipTest("Database credentials missing, skipping E2E tests.")
            
        self.env = os.environ.copy()
        # Ensure DB_PASS is set for main.py if DB_PASSWORD is provided
        if not self.env.get("DB_PASS") and self.env.get("DB_PASSWORD"):
            self.env["DB_PASS"] = self.env["DB_PASSWORD"]
            
    def run_cli(self, inputs):
        """Helper to run the CLI with a list of string inputs."""
        input_str = "\n".join(inputs) + "\n"
        result = subprocess.run(
            [sys.executable, self.main_path],
            input=input_str,
            text=True,
            capture_output=True,
            cwd=self.src_dir,
            env=self.env
        )
        return result.stdout, result.stderr, result.returncode

    def test_e2e_exit_immediately(self):
        stdout, stderr, code = self.run_cli(["5"])
        self.assertEqual(code, 0)
        self.assertIn("Exiting system...", stdout)

    def test_e2e_invalid_choice_then_exit(self):
        stdout, stderr, code = self.run_cli(["99", "5"])
        self.assertEqual(code, 0)
        self.assertIn("Invalid selection", stdout)
        self.assertIn("Exiting system...", stdout)

    def test_e2e_dba_menu_identify_stagnant(self):
        # 4: DBA Menu
        # 3: Identify Stagnant Inventory
        # 4: Return to Main Menu
        # 5: Exit System
        stdout, stderr, code = self.run_cli(["4", "3", "4", "5"])
        self.assertEqual(code, 0)
        self.assertIn("Top 10 Longest Sitting Vehicles", stdout)
        self.assertIn("Exiting system...", stdout)

    def test_e2e_customer_menu_search_dealership(self):
        # 1: Customer Menu
        # 1: Search Dealerships
        # (city input): Dallas
        # (state input): TX
        # 4: Return to Main Menu
        # 5: Exit System
        stdout, stderr, code = self.run_cli(["1", "1", "Dallas", "TX", "4", "5"])
        self.assertEqual(code, 0)
        self.assertIn("Executing: Dealership Search", stdout)
        self.assertIn("Exiting system...", stdout)

if __name__ == '__main__':
    unittest.main()
