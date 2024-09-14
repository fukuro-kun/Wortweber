# tests/test_error_handling.py

import unittest
from src.utils.error_handling import handle_exceptions, log_and_raise, logger
import logging

class TestErrorHandling(unittest.TestCase):

    def test_log_and_raise(self):
        with self.assertRaises(ValueError):
            with self.assertLogs(logger, level='ERROR') as log:
                log_and_raise(ValueError("Test error"), "Test message")
        self.assertIn("Test message: Test error", log.output[0])

    def test_handle_exceptions_decorator(self):
        @handle_exceptions
        def test_func():
            raise ValueError("Test error")

        with self.assertLogs(logger, level='ERROR') as log:
            with self.assertRaises(ValueError):
                test_func()
        self.assertIn("Fehler in test_func", log.output[0])

if __name__ == '__main__':
    unittest.main()
