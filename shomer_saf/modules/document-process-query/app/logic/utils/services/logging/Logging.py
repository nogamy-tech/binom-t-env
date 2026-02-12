import logging
import time
import functools

class ExecutionLogger:
    def __init__(self, customer_id="document-process-query", filename="Logging", source="main", process_name="Shomer_Saf", project_name="", ministry_name="",dna_transaction_id=""):
        self.customer_id = customer_id
        self.filename = filename
        self.source = source
        self.project_name = project_name
        self.ministry_name = ministry_name
        self.process_name = process_name
        self.dna_transaction_id = dna_transaction_id
        self.timespan = 0

        self.logger = self.setup_logger()

    def set_context(self, customer_id=None, filename=None, source=None, process_name=None, project_name=None, ministry_name=None, dna_transaction_id=None):
        if customer_id:
            self.customer_id = customer_id
        if filename:
            self.filename = filename
        if source:
            self.source = source
        if process_name:
            self.process_name = process_name
        if project_name:
            self.project_name = project_name
        if ministry_name:
            self.ministry_name = ministry_name
        if dna_transaction_id:
            self.dna_transaction_id = dna_transaction_id

    def log_execution(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.set_context(filename=func.__name__, source=f"{func.__module__}.{func.__name__}")
            
            start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                self.logger.exception(
                    f"Function '{func.__name__}' failed for customer_id='{self.customer_id}': {e}"
                )
                
                raise
            finally:
                self.timespan = time.time() - start
                customer_id = getattr(self, 'customer_id', 'N/A')
                self.logger.info(f"Finish document-process-query for: {customer_id}")
                
        return wrapper

    def setup_logger(self, log_level="INFO"):
        logger = logging.getLogger("result_processor")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        handler = logging.StreamHandler()
        handler.setFormatter(CloudRunFormatter(self))
        logger.addHandler(handler)
        logger.setLevel(log_level)
        return logger
    
class CloudRunFormatter(logging.Formatter):
    def __init__(self, context):
        super().__init__()
        self.context = context

    def format(self, record):
        record.customer_id = self.context.customer_id
        record.filename = self.context.filename
        record.source = self.context.source
        record.timespan = self.context.timespan
        record.process_name = self.context.process_name
        record.project_name = self.context.project_name
        record.ministry_name = self.context.ministry_name
        record.dna_transaction_id = self.context.dna_transaction_id

        log_format = (
            "%(levelname)s - %(customer_id)s - %(filename)s - %(source)s - %(process_name)s - "
            "%(project_name)s - %(ministry_name)s - %(dna_transaction_id)s - %(timespan).3fs - %(message)s"
        )
        formatter = logging.Formatter(log_format)
        return formatter.format(record)
