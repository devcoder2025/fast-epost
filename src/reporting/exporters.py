
from typing import Dict, Any
import pandas as pd
import asyncio
from datetime import datetime
import plotly.express as px
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class CSVExporter:
    async def export(
        self,
        data: pd.DataFrame,
        title: str,
        period: str
    ) -> bytes:
        return await asyncio.to_thread(
            self._generate_csv,
            data,
            title,
            period
        )

    def _generate_csv(
        self,
        data: pd.DataFrame,
        title: str,
        period: str
    ) -> bytes:
        return data.to_csv().encode('utf-8')

class PDFExporter:
    async def export(
        self,
        data: pd.DataFrame,
        title: str,
        period: str
    ) -> bytes:
        return await asyncio.to_thread(
            self._generate_pdf,
            data,
            title,
            period
        )

    def _generate_pdf(
        self,
        data: pd.DataFrame,
        title: str,
        period: str
    ) -> bytes:
        from io import BytesIO
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Add title
        elements.append(Table(
            [[title]],
            style=TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 16)
            ])
        ))

        # Add period
        elements.append(Table(
            [[f"Period: {period}"]],
            style=TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 12)
            ])
        ))

        # Add data table
        table_data = [data.columns.tolist()] + data.values.tolist()
        elements.append(Table(
            table_data,
            style=TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
        ))

        doc.build(elements)
        return buffer.getvalue()
