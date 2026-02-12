class DocumentPreProcessingMockProcess:
    """
    Mock implementation of Document PreProcessing for testing and development.
    """
    @staticmethod
    def run_process(msg) -> tuple[int, str]:
        """
        Mock document preprocessing that always returns success.
        
        Args:
            msg: Dictionary containing the request message with DocumentPreProcessing fields
            
        Returns:
            tuple: (error_code, error_message)
        """
        if DocumentPreProcessingMockProcess.document_bucket_folder():
            return 461, "BUCKET_NOT_EXISTS"
        elif DocumentPreProcessingMockProcess.document_bucket_folder_timeout():
            return 462, "BUCKET_TIMEOUT"
        elif DocumentPreProcessingMockProcess.document_exists() or DocumentPreProcessingMockProcess.multiple_documents():
            return 463, "NO_DOCUMENT_IN_BUCKET"
        elif DocumentPreProcessingMockProcess.page_bucket_folder():
            return 461, "BUCKET_NOT_EXISTS"
        elif DocumentPreProcessingMockProcess.page_bucket_folder_timeout():
            return 462, "BUCKET_TIMEOUT"
        else:
            return 200, "SUCCESS"

    @staticmethod
    def document_bucket_folder() -> bool:
        return False

    @staticmethod
    def document_bucket_folder_timeout() -> bool:
        return False

    @staticmethod
    def document_exists() -> bool:
        return False

    @staticmethod
    def multiple_documents() -> bool:
        return False
       
    @staticmethod
    def multiple_documents_exists() -> bool:
        return False
    @staticmethod
    def page_bucket_folder() -> bool:
        return False
        
    @staticmethod
    def page_bucket_folder_timeout() -> bool:
        return False
        
    @staticmethod
    def file_exists_in_page() -> bool:
        return False
        


