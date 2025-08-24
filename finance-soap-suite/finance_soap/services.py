from datetime import date
from decimal import Decimal
from spyne import ServiceBase, rpc, Unicode, Integer, Decimal as SDecimal, Date, Array
from finance_soap.schemas import Customer, Account, Transaction, Invoice, Loan, Statement, FxQuote, RiskReport, KycResult
from finance_soap.repository import InMemoryRepo

# Exposed RPCs:
#  1 create_customer
#  2 kyc_check
#  3 open_account
#  4 get_account
#  5 get_balance
#  6 deposit
#  7 withdraw
#  8 transfer
#  9 list_transactions
# 10 create_invoice
# 11 pay_invoice
# 12 get_invoice_status
# 13 create_loan
# 14 calculate_interest
# 15 get_fx_quote
# 16 generate_statement
# 17 risk_score

_repo = InMemoryRepo()

class FinanceService(ServiceBase):
    @rpc(Unicode, _returns=Customer)
    def create_customer(ctx, full_name):
        return _repo.create_customer(full_name)

    @rpc(Unicode, _returns=KycResult)
    def kyc_check(ctx, customer_id):
        return _repo.kyc_check(customer_id)

    @rpc(Unicode, Unicode, _returns=Account)
    def open_account(ctx, customer_id, currency):
        return _repo.open_account(customer_id, currency)

    @rpc(Unicode, _returns=Account)
    def get_account(ctx, account_id):
        acc = _repo.get_account(account_id)
        if not acc:
            raise ValueError("ACCOUNT_NOT_FOUND")
        return acc

    @rpc(Unicode, _returns=SDecimal(precision=18, scale=4))
    def get_balance(ctx, account_id):
        return FinanceService.get_account(ctx, account_id).balance

    @rpc(Unicode, SDecimal(precision=18, scale=4), _returns=Transaction)
    def deposit(ctx, account_id, amount):
        return _repo.deposit(account_id, Decimal(amount))

    @rpc(Unicode, SDecimal(precision=18, scale=4), _returns=Transaction)
    def withdraw(ctx, account_id, amount):
        return _repo.withdraw(account_id, Decimal(amount))

    @rpc(Unicode, Unicode, SDecimal(precision=18, scale=4), _returns=Array(Unicode))
    def transfer(ctx, from_account_id, to_account_id, amount):
        d, c = _repo.transfer(from_account_id, to_account_id, Decimal(amount))
        return [d.txn_id, c.txn_id]

    @rpc(Unicode, _returns=Array(Transaction))
    def list_transactions(ctx, account_id):
        return _repo.list_transactions(account_id)

    @rpc(Unicode, SDecimal(precision=18, scale=4), Unicode, Date, _returns=Invoice)
    def create_invoice(ctx, customer_id, amount, currency, due_date):
        return _repo.create_invoice(customer_id, Decimal(amount), currency, due_date)

    @rpc(Unicode, _returns=Invoice)
    def pay_invoice(ctx, invoice_id):
        return _repo.pay_invoice(invoice_id)

    @rpc(Unicode, _returns=Unicode)
    def get_invoice_status(ctx, invoice_id):
        return _repo.invoice_status(invoice_id)

    @rpc(Unicode, SDecimal(precision=18, scale=4), SDecimal(precision=7, scale=4), Integer, Unicode, _returns=Loan)
    def create_loan(ctx, customer_id, principal, rate_apr, term_months, currency):
        return _repo.create_loan(customer_id, Decimal(principal), Decimal(rate_apr), int(term_months), currency)

    @rpc(SDecimal(precision=18, scale=4), SDecimal(precision=7, scale=4), Integer, _returns=SDecimal(precision=18, scale=4))
    def calculate_interest(ctx, principal, rate_apr, days):
        return _repo.calc_interest(Decimal(principal), Decimal(rate_apr), int(days))

    @rpc(Unicode, Unicode, _returns=FxQuote)
    def get_fx_quote(ctx, base, quote):
        return _repo.fx_quote(base, quote)

    @rpc(Unicode, Date, Date, _returns=Statement)
    def generate_statement(ctx, account_id, from_date, to_date):
        return _repo.generate_statement(account_id, from_date, to_date)

    @rpc(Unicode, _returns=RiskReport)
    def risk_score(ctx, customer_id):
        return _repo.risk_score(customer_id)
