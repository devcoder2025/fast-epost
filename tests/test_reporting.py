
import pytest
from unittest.mock import Mock, patch
import pandas as pd
from datetime import datetime
from src.reporting.generator import ReportGenerator, ReportConfig
from src.reporting.exporters import CSVExporter, PDFExporter

@pytest.fixture
def report_generator():
    return ReportGenerator()

@pytest.fixture
def sample_data():
    return {
        'system_cpu': [10, 20, 30],
        'system_memory': [40, 50, 60],
        'build_time': [100, 200, 300]
    }

@pytest.fixture
def report_config():
    return ReportConfig(
        title="Test Report",
        period="daily",
        metrics=['system_cpu', 'system_memory'],
        format='csv'
    )

@pytest.mark.asyncio
async def test_report_generation(report_generator, sample_data, report_config):
    report = await report_generator.generate_report(report_config, sample_data)
    assert isinstance(report, bytes)
    assert len(report) > 0

@pytest.mark.asyncio
async def test_csv_export():
    exporter = CSVExporter()
    df = pd.DataFrame({'test': [1, 2, 3]})
    result = await exporter.export(df, "Test", "daily")
    assert isinstance(result, bytes)
    assert b'test' in result

@pytest.mark.asyncio
async def test_pdf_export():
    exporter = PDFExporter()
    df = pd.DataFrame({'test': [1, 2, 3]})
    result = await exporter.export(df, "Test", "daily")
    assert isinstance(result, bytes)
    assert len(result) > 0

def test_report_scheduling(report_generator, report_config):
    report_generator.schedule_report('test_report', report_config)
    assert 'test_report' in report_generator.scheduled_reports

@pytest.mark.asyncio
async def test_scheduled_report_generation(report_generator, report_config):
    with patch.object(report_generator, '_collect_report_data') as mock_collect:
        mock_collect.return_value = {'system_cpu': [1, 2, 3]}
        
        report_generator.schedule_report('test_report', report_config)
        await report_generator._generate_scheduled_report('test_report')
        
        assert mock_collect.called
