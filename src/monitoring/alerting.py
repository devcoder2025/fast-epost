
from typing import List, Dict, Optional
import asyncio
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class Alert:
    severity: str
    metric: str
    value: float
    threshold: float
    timestamp: datetime
    message: str

class AlertManager:
    def __init__(self, notification_manager=None):
        self.notification_manager = notification_manager
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self._running = False

    async def start_monitoring(self):
        self._running = True
        while self._running:
            await self._check_thresholds()
            await asyncio.sleep(10)

    def stop_monitoring(self):
        self._running = False

    async def _check_thresholds(self):
        metrics = self._collect_current_metrics()
        for metric, value in metrics.items():
            await self._evaluate_metric(metric, value)

    def _collect_current_metrics(self) -> Dict[str, float]:
        # Collect metrics from Prometheus client
        return {
            'cpu_usage': float(prom.REGISTRY.get_sample_value('cpu_usage')),
            'memory_usage': float(prom.REGISTRY.get_sample_value('memory_usage')),
            'disk_usage': float(prom.REGISTRY.get_sample_value('disk_usage'))
        }

    async def _evaluate_metric(self, metric: str, value: float):
        thresholds = self._get_thresholds(metric)
        
        if value >= thresholds.critical:
            await self._create_alert(
                metric,
                value,
                thresholds.critical,
                'critical'
            )
        elif value >= thresholds.warning:
            await self._create_alert(
                metric,
                value,
                thresholds.warning,
                'warning'
            )
        else:
            await self._resolve_alert(metric)

    async def _create_alert(
        self,
        metric: str,
        value: float,
        threshold: float,
        severity: str
    ):
        if metric not in self.active_alerts:
            alert = Alert(
                severity=severity,
                metric=metric,
                value=value,
                threshold=threshold,
                timestamp=datetime.now(),
                message=self._generate_alert_message(
                    metric,
                    value,
                    threshold,
                    severity
                )
            )
            
            self.active_alerts[metric] = alert
            self.alert_history.append(alert)
            
            if self.notification_manager:
                await self._send_alert_notification(alert)

    async def _resolve_alert(self, metric: str):
        if metric in self.active_alerts:
            del self.active_alerts[metric]
            if self.notification_manager:
                await self._send_resolution_notification(metric)

    def _generate_alert_message(
        self,
        metric: str,
        value: float,
        threshold: float,
        severity: str
    ) -> str:
        return (
            f"{severity.upper()} Alert: {metric} is {value:.2f}, "
            f"threshold is {threshold:.2f}"
        )

    async def _send_alert_notification(self, alert: Alert):
        await self.notification_manager.send_webhook({
            'type': 'alert',
            'severity': alert.severity,
            'metric': alert.metric,
            'value': alert.value,
            'message': alert.message,
            'timestamp': alert.timestamp.isoformat()
        })

    async def _send_resolution_notification(self, metric: str):
        await self.notification_manager.send_webhook({
            'type': 'resolution',
            'metric': metric,
            'message': f"Alert for {metric} has been resolved",
            'timestamp': datetime.now().isoformat()
        })

    def _get_thresholds(self, metric: str) -> MetricThreshold:
        return {
            'cpu_usage': MetricThreshold(warning=70.0, critical=90.0),
            'memory_usage': MetricThreshold(warning=80.0, critical=95.0),
            'disk_usage': MetricThreshold(warning=85.0, critical=95.0)
        }[metric]
