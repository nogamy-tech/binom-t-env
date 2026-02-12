class DocumentQueryGetMockProcess:
    """
    Mock implementation of Document Query Get for testing and development.
    """
    @staticmethod
    def run_process(msg) -> tuple[int, str, list, list, dict]:
        """
        Mock document query get that always returns success with sample data.
        
        Args:
            msg: Dictionary containing the request message with PollThresholdCheckResult fields
            
        Returns:
            tuple: (error_code, error_message, queries_page_results, queries_results, queries_aggregated_results)
        """
        # Mock implementation - can be extended to simulate different scenarios
        if DocumentQueryGetMockProcess.schema_validation_failed():
            return 422, "Unprocessable Entity", None, None, None
        elif DocumentQueryGetMockProcess.accounts_db_timeout():
            return 500, "Internal Server Error", None, None, None
        elif DocumentQueryGetMockProcess.unknown_client():
            return 500, "Internal Server Error", None, None, None
        elif DocumentQueryGetMockProcess.db_timeout():
            return 500, "Internal Server Error", None, None, None
        elif DocumentQueryGetMockProcess.no_content():
            return 500, "Internal Server Error", None, None, None
        else:
            # Return mock success data
            queries_page_results = [
                {"queryID": "1", "page": "1", "response": "model response", "compliance": "True", "confidence": "0.9"}
            ]
            queries_results = [
                {"queryID": "1", "compliance": "True"}
            ]
            queries_aggregated_results = {
                "total_queries": 5,
                "true_queries": 2,
                "false_queries": 3
            }
            return 200, "OK", queries_page_results, queries_results, queries_aggregated_results

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
    def db_timeout() -> bool:
        return False

    @staticmethod
    def no_content() -> bool:
        return False

