class CustomError extends Error {
  constructor(message: string, public code: number) {
    super(message);
    this.name = 'CustomError';
  }
}

export const errorHandler = (error: Error) => {
  if (error instanceof CustomError) {
    logger.error(`${error.code}: ${error.message}`);
  }
  // Handle other error types
};
