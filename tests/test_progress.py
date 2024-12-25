import unittest
import io
import sys
from src.progress.progress_bar import ProgressBar, ProgressBarStyle, ColorScheme
from src.progress.formatters import ProgressFormatter, format_bytes, format_time

class TestProgressBar(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_progress_bar_initialization(self):
        progress = ProgressBar(total=100)
        self.assertEqual(progress.total, 100)
        self.assertEqual(progress.n, 0)

    def test_progress_bar_update(self):
        progress = ProgressBar(total=100)
        progress.update(10)
        self.assertEqual(progress.n, 10)

    def test_color_schemes(self):
        progress = ProgressBar(total=100, color_scheme=ColorScheme.SUCCESS)
        progress.update(50)
        output = self.output.getvalue()
        self.assertIn(ColorScheme.SUCCESS.value, output)

    def test_custom_style(self):
        style = ProgressBarStyle(fill_char="#", empty_char="-")
        progress = ProgressBar(total=100, style=style)
        progress.update(50)
        output = self.output.getvalue()
        self.assertIn("#", output)
        self.assertIn("-", output)

class TestFormatters(unittest.TestCase):
    def test_byte_formatter(self):
        self.assertEqual(format_bytes(1024), "1.0 KB")
        self.assertEqual(format_bytes(1024 * 1024), "1.0 MB")

    def test_time_formatter(self):
        self.assertEqual(format_time(65), "0:01:05")

    def test_progress_formatter(self):
        formatter = ProgressFormatter()
        self.assertEqual(formatter.percentage(0.756), "75.6%")
        self.assertEqual(formatter.fraction(75, 100), "75/100")
