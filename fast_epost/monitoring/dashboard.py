from flask import Blueprint, render_template
from .metrics import MetricsCollector
import plotly.express as px
import pandas as pd

dashboard = Blueprint('dashboard', __name__)
metrics_collector = MetricsCollector()

class DashboardManager:
    def __init__(self):
        self.collector = MetricsCollector()
        
    def generate_metrics_chart(self):
        metrics_data = self.collector.metrics
        df = pd.DataFrame(metrics_data)
        fig = px.line(df, x='timestamp', y=['cpu_usage', 'memory_usage', 'response_time'])
        return fig.to_html()
        
    def get_system_stats(self):
        return {
            'total_requests': len(self.collector.metrics),
            'avg_response_time': sum(m.response_time for m in self.collector.metrics) / len(self.collector.metrics),
            'peak_cpu': max(m.cpu_usage for m in self.collector.metrics),
            'peak_memory': max(m.memory_usage for m in self.collector.metrics)
        }
