# run_tests.py

import unittest
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)
