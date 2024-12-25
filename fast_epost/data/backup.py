import shutil
from datetime import datetime
from pathlib import Path

class BackupManager:
    def __init__(self, backup_dir: str):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self) -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f'backup_{timestamp}.zip'
        shutil.make_archive(str(backup_path), 'zip', 'data')
        return str(backup_path)
