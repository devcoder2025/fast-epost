class RecoverySystem:
    def __init__(self):
        self.recovery_strategies = {}
        self.max_retries = 3
        
    async def attempt_recovery(self, error: AppError):
        if strategy := self.recovery_strategies.get(error.code):
            for attempt in range(self.max_retries):
                try:
                    return await strategy(error)
                except Exception:
                    continue
