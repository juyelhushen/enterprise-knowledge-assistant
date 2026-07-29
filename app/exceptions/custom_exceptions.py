class EnterpriseAssistantException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class RetrievalException(EnterpriseAssistantException):
    pass


class LLMException(EnterpriseAssistantException):
    pass


class DocumentException(EnterpriseAssistantException):
    pass

class DocumentNotFoundException(Exception):
    pass


class ConfigurationException(EnterpriseAssistantException):
    pass

class ValidationException(Exception):
    """
    Raised when uploaded file validation fails.
    """

class FileValidationException(Exception):

    def __init__(self, message: str):
        self.message = message

