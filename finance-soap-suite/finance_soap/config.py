import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    HOST: str = os.getenv("SOAP_HOST", "127.0.0.1")
    PORT: int = int(os.getenv("SOAP_PORT", "8000"))
    SERVICE_NAME: str = os.getenv("SOAP_SERVICE_NAME", "FinanceService")
    TARGET_NAMESPACE: str = os.getenv("SOAP_TNS", "http://myproject.com/finance")
    APP_NAME: str = os.getenv("SOAP_APP_NAME", "finance-soap-suite")

settings = Settings()
