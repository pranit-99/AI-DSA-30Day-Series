from pydantic import BaseModel

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    transaction_count_last_hour: int
    account_age_days: int
    location_mismatch: int