class QueueMetrics:
    def __init__(self):
        self.messages_published = 0
        self.messages_processed = 0
        self.messages_failed = 0
        self.processing_time = []

    def increment_published(self):
        self.messages_published += 1

    def increment_processed(self):
        self.messages_processed += 1

    def increment_failed(self):
        self.messages_failed += 1

    def add_processing_time(self, duration: float):
        self.processing_time.append(duration)

    def get_metrics(self) -> Dict:
        return {
            "published": self.messages_published,
            "processed": self.messages_processed,
            "failed": self.messages_failed,
            "avg_processing_time": sum(self.processing_time) / len(self.processing_time) if self.processing_time else 0
        }
