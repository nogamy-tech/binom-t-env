class DocumentStartJobMockProcess:
    """
    Mock implementation of Document Start Job for testing and development.
    """
    @staticmethod
    def run_process(msg) -> tuple[int, str]:
        """
        Mock document start job that always returns success.
        
        Args:
            msg: Dictionary containing the request message with QueueThresholdCheck fields
            
        Returns:
            tuple: (error_code, error_message)
        """
        # Mock implementation - can be extended to simulate different scenarios
        if DocumentStartJobMockProcess.schema_validation_failed():
            return 422, "Unprocessable Entity"
        elif DocumentStartJobMockProcess.accounts_db_timeout():
            return 500, "Internal Server Error"
        elif DocumentStartJobMockProcess.unknown_client():
            return 500, "Internal Server Error"
        elif DocumentStartJobMockProcess.unsupported_format():
            return 500, "Internal Server Error"
        elif DocumentStartJobMockProcess.unreadable_file():
            return 500, "Internal Server Error"
        elif DocumentStartJobMockProcess.bucket_not_exists():
            return 500, "Internal Server Error"
        elif DocumentStartJobMockProcess.bucket_timeout():
            return 500, "Internal Server Error"
        elif DocumentStartJobMockProcess.client_request_id_already_used():
            return 500, "Internal Server Error"
        elif DocumentStartJobMockProcess.db_timeout():
            return 500, "Internal Server Error"
        elif DocumentStartJobMockProcess.workflow_timeout():
            return 500, "Internal Server Error"
        elif DocumentStartJobMockProcess.workflow_error():
            return 500, "Internal Server Error"
        else:
            return 202, "OK"

    @staticmethod
    def schema_validation_failed() -> bool:
        return False

    @staticmethod
    def accounts_db_timeout() -> bool:
        return False

    @staticmethod
    def unknown_client() -> bool:
        return False

    @staticmethod
    def unsupported_format() -> bool:
        return False

    @staticmethod
    def unreadable_file() -> bool:
        return False

    @staticmethod
    def bucket_not_exists() -> bool:
        return False

    @staticmethod
    def bucket_timeout() -> bool:
        return False

    @staticmethod
    def client_request_id_already_used() -> bool:
        return False

    @staticmethod
    def db_timeout() -> bool:
        return False

    @staticmethod
    def workflow_timeout() -> bool:
        return False

    @staticmethod
    def workflow_error() -> bool:
        return False

