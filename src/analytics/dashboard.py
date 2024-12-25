
import asyncio
from typing import Dict, List, Optional
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json
from .metrics import MetricsCollector

class AnalyticsDashboard:
    def __init__(self):
        self.app = FastAPI()
        self.metrics = MetricsCollector()
        self.clients: List[WebSocket] = []
        self._setup_routes()

    def _setup_routes(self):
        @self.app.get("/")
        async def get_dashboard():
            return HTMLResponse(self._generate_dashboard_html())

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self.clients.append(websocket)
            try:
                while True:
                    await websocket.receive_text()
                    metrics = self.metrics.get_metrics_snapshot()
                    await websocket.send_json(metrics)
            except:
                self.clients.remove(websocket)

        @self.app.get("/api/metrics")
        async def get_metrics():
            return self.metrics.get_metrics_snapshot()

    def _generate_dashboard_html(self) -> str:
        return """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Analytics Dashboard</title>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <script>
                    const ws = new WebSocket(`ws://${window.location.host}/ws`);
                    ws.onmessage = function(event) {
                        const metrics = JSON.parse(event.data);
                        updateCharts(metrics);
                    };

                    function updateCharts(metrics) {
                        // CPU Usage
                        Plotly.update('cpu-chart', {
                            y: [[metrics.system.cpu_usage]]
                        });

                        // Memory Usage
                        Plotly.update('memory-chart', {
                            y: [[metrics.system.memory_usage]]
                        });

                        // Update package stats
                        const packageStats = document.getElementById('package-stats');
                        packageStats.innerHTML = '';
                        for (const [name, stats] of Object.entries(metrics.packages)) {
                            packageStats.innerHTML += `
                                <div class="package">
                                    <h3>${name}</h3>
                                    <p>Downloads: ${stats.download_count}</p>
                                    <p>Build Time: ${stats.build_time}s</p>
                                </div>
                            `;
                        }
                    }
                </script>
                <style>
                    .chart { height: 300px; margin: 20px; }
                    .package { border: 1px solid #ccc; padding: 10px; margin: 10px; }
                </style>
            </head>
            <body>
                <h1>System Analytics</h1>
                <div id="cpu-chart" class="chart"></div>
                <div id="memory-chart" class="chart"></div>
                <h2>Package Statistics</h2>
                <div id="package-stats"></div>
            </body>
        </html>
        """

    async def start(self, host: str = "0.0.0.0", port: int = 8000):
        metrics_task = asyncio.create_task(self.metrics.start_collection())
        await self.app.start(host=host, port=port)
        await metrics_task
