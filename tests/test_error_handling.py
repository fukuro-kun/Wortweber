# Wortweber - Echtzeit-Sprachtranskription mit KI
# Copyright (C) 2024 fukuro-kun
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#
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
