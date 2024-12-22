from datetime import datetime
from config.config import Config

class VatService:
    @staticmethod
    def calculate_vat(amount: float, calculation_date: datetime = None) -> dict:
        if calculation_date is None:
            calculation_date = datetime.now()
            
        vat_rate = Config.VAT_RATE_FUTURE if calculation_date >= datetime(2025, 1, 1) else Config.VAT_RATE_CURRENT
        vat_amount = round(amount * vat_rate, 2)
        total = round(amount + vat_amount, 2)
        
        return {
            'base_amount': amount,
            'vat_rate': vat_rate,
            'vat_amount': vat_amount,
            'total_amount': total,
            'calculation_date': calculation_date.isoformat()
        }
