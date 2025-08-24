from decimal import Decimal
from datetime import date, datetime
from spyne import ComplexModel, Unicode, Integer, Decimal as SDecimal, Date, DateTime, Array, Boolean

class Customer(ComplexModel):
    customer_id = Unicode
    full_name = Unicode
    kyc_verified = Boolean

class Account(ComplexModel):
    account_id = Unicode
    customer_id = Unicode
    currency = Unicode
    balance = SDecimal(precision=18, scale=4)

class Transaction(ComplexModel):
    txn_id = Unicode
    account_id = Unicode
    amount = SDecimal(precision=18, scale=4)
    currency = Unicode
    type = Unicode  # DEPOSIT, WITHDRAWAL, TRANSFER_IN, TRANSFER_OUT
    timestamp = DateTime
    description = Unicode

class Invoice(ComplexModel):
    invoice_id = Unicode
    customer_id = Unicode
    amount = SDecimal(precision=18, scale=4)
    currency = Unicode
    status = Unicode  # OPEN, PAID, VOID
    due_date = Date

class Loan(ComplexModel):
    loan_id = Unicode
    customer_id = Unicode
    principal = SDecimal(precision=18, scale=4)
    rate_apr = SDecimal(precision=7, scale=4)
    term_months = Integer
    currency = Unicode

class StatementLine(ComplexModel):
    date = Date
    description = Unicode
    amount = SDecimal(precision=18, scale=4)
    balance_after = SDecimal(precision=18, scale=4)

class Statement(ComplexModel):
    account_id = Unicode
    from_date = Date
    to_date = Date
    lines = Array(StatementLine)

class FxQuote(ComplexModel):
    base = Unicode
    quote = Unicode
    rate = SDecimal(precision=18, scale=8)
    timestamp = DateTime

class RiskReport(ComplexModel):
    customer_id = Unicode
    score = Integer
    band = Unicode
    reason = Unicode

class KycResult(ComplexModel):
    customer_id = Unicode
    passed = Boolean
    reason = Unicode
