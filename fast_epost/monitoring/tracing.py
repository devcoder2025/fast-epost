from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from functools import wraps
import time

class TracingSystem:
    def __init__(self):
        provider = TracerProvider()
        processor = ConsoleSpanExporter()
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        self.tracer = trace.get_tracer(__name__)
        
    def trace_request(self, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            with self.tracer.start_as_current_span(f.__name__) as span:
                start_time = time.time()
                try:
                    result = f(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR))
                    span.record_exception(e)
                    raise
                finally:
                    span.set_attribute("duration", time.time() - start_time)
        return wrapped
