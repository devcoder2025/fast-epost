import pandas as pd
import matplotlib.pyplot as plt

class PerformanceAnalyzer:
    def __init__(self, test_results: List[LoadTestResult]):
        self.results = test_results
        
    def generate_report(self) -> Dict:
        df = pd.DataFrame([vars(r) for r in self.results])
        return {
            'average_rps': df['requests_per_second'].mean(),
            'peak_response_time': df['average_response_time'].max(),
            'error_rate': df['error_rate'].mean()
        }
