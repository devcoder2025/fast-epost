from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self, app_runner):
        self.app_runner = app_runner
        self.last_reload = time.time()
        
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            current_time = time.time()
            if current_time - self.last_reload > 1:
                self.app_runner.restart()
                self.last_reload = current_time

class DevServer:
    def __init__(self, app_path: str, port: int = 5000):
        self.app_path = app_path
        self.port = port
        self.process = None
        
    def start(self):
        self.process = subprocess.Popen(
            ['python', self.app_path],
            env={**os.environ, 'FLASK_ENV': 'development'}
        )
        
        observer = Observer()
        observer.schedule(
            CodeChangeHandler(self),
            path='.',
            recursive=True
        )
        observer.start()
        
    def restart(self):
        if self.process:
            self.process.terminate()
            self.start()
