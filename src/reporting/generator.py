
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime, timedelta
import pandas as pd
from .exporters import CSVExporter, PDFExporter

@dataclass
class ReportConfig:
    title: str
    period: str  # daily, weekly, monthly
    metrics: List[str]
    format: str  # csv, pdf
    schedule: Optional[str] = None  # cron expression

class ReportGenerator:
    def __init__(self):
        self.exporters = {
            'csv': CSVExporter(),
            'pdf': PDFExporter()
        }
        self.scheduled_reports: Dict[str, ReportConfig] = {}
        self._running = False

    async def generate_report(
        self,
        config: ReportConfig,
        data: Dict[str, Any]
    ) -> bytes:
        df = self._prepare_data(data, config.metrics)
        exporter = self.exporters[config.format.lower()]
        return await exporter.export(
            df,
            title=config.title,
            period=config.period
        )

    def schedule_report(self, report_id: str, config: ReportConfig):
        self.scheduled_reports[report_id] = config

    async def start_scheduler(self):
        self._running = True
        while self._running:
            now = datetime.now()
            for report_id, config in self.scheduled_reports.items():
                if self._should_generate(config, now):
                    await self._generate_scheduled_report(report_id)
            await asyncio.sleep(60)

    def _prepare_data(
        self,
        data: Dict[str, Any],
        metrics: List[str]
    ) -> pd.DataFrame:
        filtered_data = {
            metric: data[metric]
            for metric in metrics
            if metric in data
        }
        return pd.DataFrame(filtered_data)

    def _should_generate(self, config: ReportConfig, now: datetime) -> bool:
        if not config.schedule:
            return False

        last_run = getattr(config, 'last_run', None)
        if not last_run:
            return True

        period_map = {
            'daily': timedelta(days=1),
            'weekly': timedelta(weeks=1),
            'monthly': timedelta(days=30)
        }

        return now - last_run >= period_map[config.period]

    async def _generate_scheduled_report(self, report_id: str):
        config = self.scheduled_reports[report_id]
        data = await self._collect_report_data(config)
        report = await self.generate_report(config, data)
        await self._store_report(report_id, report)
        config.last_run = datetime.now()

    async def _collect_report_data(
        self,
        config: ReportConfig
    ) -> Dict[str, Any]:
        # Collect data from various sources based on metrics
        data = {}
        for metric in config.metrics:
            if metric.startswith('system_'):
                data[metric] = await self._get_system_metrics()
            elif metric.startswith('build_'):
                data[metric] = await self._get_build_metrics()
            elif metric.startswith('api_'):
                data[metric] = await self._get_api_metrics()
        return data

    async def _store_report(self, report_id: str, report: bytes):
        # Store the generated report (implementation depends on storage solution)
        filename = f"report_{report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with open(f"reports/{filename}", "wb") as f:
            f.write(report)
