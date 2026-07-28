from abc import ABC, abstractmethod

from app.models.audit_log import AuditLog


class AuditLogRepository(ABC):

    @abstractmethod
    def save(
            self,
            log: AuditLog
    ) -> None:
        pass
        
    @abstractmethod
    def find_all(self) -> list[AuditLog]:
        pass
    
    @abstractmethod
    def clear(self) -> None:
        pass