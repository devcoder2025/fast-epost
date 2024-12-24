import unittest
from typing import List, Type
import coverage

class TestRunner:
    def __init__(self):
        self.cov = coverage.Coverage()
        
    def run_tests(self, test_cases: List[Type[unittest.TestCase]]):
        self.cov.start()
        suite = unittest.TestSuite()
        for test_case in test_cases:
            suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))
            
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        
        self.cov.stop()
        self.cov.save()
        self.cov.html_report()
        
        return result

```python:fast_epost/testing/fixtures.py
import pytest
from typing import Generator
import tempfile
import os

@pytest.fixture
def temp_storage() -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir
        
@pytest.fixture
def mock_db():
    from fast_epost.config.database import get_db_connection
    db = get_db_connection()
    yield db
    db.dispose()
