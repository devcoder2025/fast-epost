from alembic import op
import sqlalchemy as sa
from typing import List

class MigrationManager:
    def __init__(self):
        self.migrations: List[str] = []
        
    def create_migration(self, name: str):
        revision = self._generate_revision()
        self.migrations.append(revision)
        return revision
        
    def run_migrations(self):
        for migration in self.migrations:
            op.execute(migration)
