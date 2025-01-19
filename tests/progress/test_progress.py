import pytest
import time
from unittest.mock import patch
from io import StringIO
from src.progress.progress_bar import EnhancedProgressBar

@pytest.fixture
def progress_bar():
    return EnhancedProgressBar(total=100, description="Processing")

def test_progress_initialization(progress_bar):
    assert progress_bar.total == 100
    assert progress_bar._stats.current == 0
    assert not progress_bar._stats.is_paused

def test_progress_update():
    with patch('sys.stdout', new=StringIO()) as fake_output:
        bar = EnhancedProgressBar(total=10)
        bar.update(5)
        output = fake_output.getvalue()
        assert "50%" in output
        assert "5/10" in output

def test_pause_resume():
    bar = EnhancedProgressBar(total=100)
    bar.update(10)
    initial_rate = bar._stats.rate
    
    bar.pause()
    assert bar._stats.is_paused
    bar.update(10)  # Should not increase while paused
    assert bar._stats.current == 10
    
    bar.resume()
    assert not bar._stats.is_paused
    bar.update(10)
    assert bar._stats.current == 20

def test_memory_tracking():
    bar = EnhancedProgressBar(total=100, show_memory=True)
    bar.update(50)
    assert bar._stats.memory_usage_mb > 0

def test_eta_calculation():
    bar = EnhancedProgressBar(total=100)
    start_time = time.time()
    
    with patch('time.time', side_effect=[start_time, start_time + 2]):
        bar.update(20)
        assert 8 <= bar._stats.eta_seconds <= 10  # Expected ~8 seconds at current rate
