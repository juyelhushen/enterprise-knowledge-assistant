class EnterpriseAssistantException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class RetrievalException(EnterpriseAssistantException):
    pass


class LLMException(EnterpriseAssistantException):
    pass


class DocumentException(EnterpriseAssistantException):
    pass


class ConfigurationException(EnterpriseAssistantException):
    pass
