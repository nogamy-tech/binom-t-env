class VisionModelTimeOut(Exception):
    """Custom alert for when the vision model is Timed Out."""
    pass

class TextModelTimeOut(Exception):
    """Custom alert for when the text model is Timed Out."""            
    pass

class ModelFailure(Exception):
    """Custom alert for when the model is failed."""
    pass