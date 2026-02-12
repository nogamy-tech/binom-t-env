class DocumentQueryMockProcess:
    """
    Mock implementation of Document Process Query for testing and development.
    """
    @staticmethod
    def run_process(msg) -> tuple[int, str]:
        """
        Mock document process query with various error scenarios.
        
        Args:
            msg: Dictionary containing the request message with DocumentProcessRequest fields
            
        Returns:
            tuple: (error_code, error_message)
        """
        if DocumentQueryMockProcess.data_bucket_folder_not_exists():
            return 461, "BUCKET_NOT_EXISTS"
        elif DocumentQueryMockProcess.data_bucket_folder_timeout():
            return 462, "BUCKET_TIMEOUT"
        elif DocumentQueryMockProcess.file_not_exists_in_data_bucket():
            return 463, "DATA_MISSING"
        elif DocumentQueryMockProcess.text_model_timeout():
            return 467, "TEXT_MODEL_TIMEOUT"
        elif DocumentQueryMockProcess.text_model_failure():
            return 469, "MODEL_FAILURE"
        elif DocumentQueryMockProcess.vision_model_timeout():
            return 468, "VISION_MODEL_TIMEOUT"
        elif DocumentQueryMockProcess.vision_model_failure():
            return 469, "MODEL_FAILURE"
        elif DocumentQueryMockProcess.db_timeout():
            return 470, "DB_TIMEOUT"
        else:
            return 200, "OK"
    
    # Error scenario methods
    @staticmethod
    def data_bucket_folder_not_exists() -> bool:
        return False
    
    @staticmethod
    def data_bucket_folder_timeout() -> bool:
        return False
    
    @staticmethod
    def file_not_exists_in_data_bucket() -> bool:
        return True
    
    @staticmethod
    def text_model_timeout() -> bool:
        return False
    
    @staticmethod
    def text_model_failure() -> bool:
        return False
    
    @staticmethod
    def vision_model_timeout() -> bool:
        return False
    
    @staticmethod
    def vision_model_failure() -> bool:
        return False
    
    @staticmethod
    def db_timeout() -> bool:
        return False