from flask import jsonify
import psutil

class HealthCheck:
    @staticmethod
    def check_database():
        try:
            db.session.execute('SELECT 1')
            return True
        except Exception:
            return False
            
    @staticmethod
    def check_storage():
        try:
            storage.get_file('health_check.txt')
            return True
        except Exception:
            return False
            
    def get_status(self):
        return {
            'status': 'healthy',
            'database': self.check_database(),
            'storage': self.check_storage(),
            'memory': psutil.virtual_memory().percent,
            'cpu': psutil.cpu_percent()
        }
