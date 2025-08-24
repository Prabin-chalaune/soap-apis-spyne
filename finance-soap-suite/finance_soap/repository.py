from __future__ import annotations
import uuid
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, date
from typing import Dict, List, Tuple
from finance_soap.schemas import Account, Customer, Transaction, Invoice, Loan, Statement, StatementLine, FxQuote, RiskReport, KycResult

class InMemoryRepo:
    def __init__(self) -> None:
        self.customers: Dict[str, Customer] = {}
        self.accounts: Dict[str, Account] = {}
        self.txs: Dict[str, List[Transaction]] = {}
        self.invoices: Dict[str, Invoice] = {}
        self.loans: Dict[str, Loan] = {}

    # Helpers
    @staticmethod
    def _id(prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex[:12]}"

    @staticmethod
    def _dec(x: str | Decimal) -> Decimal:
        return (x if isinstance(x, Decimal) else Decimal(str(x))).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

    # Customers
    def create_customer(self, full_name: str) -> Customer:
        cid = self._id("CUST")
        obj = Customer(customer_id=cid, full_name=full_name, kyc_verified=False)
        self.customers[cid] = obj
        return obj

    def kyc_check(self, customer_id: str) -> KycResult:
        cust = self.customers.get(customer_id)
        if not cust:
            return KycResult(customer_id=customer_id, passed=False, reason="NOT_FOUND")
        cust.kyc_verified = True
        return KycResult(customer_id=customer_id, passed=True, reason="VERIFIED_BASIC")

    # Accounts
    def open_account(self, customer_id: str, currency: str) -> Account:
        if customer_id not in self.customers:
            raise ValueError("Customer not found")
        aid = self._id("ACC")
        acc = Account(account_id=aid, customer_id=customer_id, currency=currency, balance=self._dec("0"))
        self.accounts[aid] = acc
        self.txs[aid] = []
        return acc

    def get_account(self, account_id: str) -> Account | None:
        return self.accounts.get(account_id)

    def deposit(self, account_id: str, amount: Decimal, desc="Deposit") -> Transaction:
        acc = self.accounts[account_id]
        amount = self._dec(amount)
        acc.balance = self._dec(acc.balance + amount)
        txn = Transaction(
            txn_id=self._id("TX"),
            account_id=account_id,
            amount=amount,
            currency=acc.currency,
            type="DEPOSIT",
            timestamp=datetime.utcnow(),
            description=desc
        )
        self.txs[account_id].append(txn)
        return txn

    def withdraw(self, account_id: str, amount: Decimal, desc="Withdrawal") -> Transaction:
        acc = self.accounts[account_id]
        amount = self._dec(amount)
        if acc.balance < amount:
            raise ValueError("INSUFFICIENT_FUNDS")
        acc.balance = self._dec(acc.balance - amount)
        txn = Transaction(
            txn_id=self._id("TX"),
            account_id=account_id,
            amount=-amount,
            currency=acc.currency,
            type="WITHDRAWAL",
            timestamp=datetime.utcnow(),
            description=desc
        )
        self.txs[account_id].append(txn)
        return txn

    def transfer(self, src_id: str, dst_id: str, amount: Decimal) -> Tuple[Transaction, Transaction]:
        if self.accounts[src_id].currency != self.accounts[dst_id].currency:
            raise ValueError("CURRENCY_MISMATCH")
        debit = self.withdraw(src_id, amount, desc=f"Transfer to {dst_id}")
        credit = self.deposit(dst_id, amount, desc=f"Transfer from {src_id}")
        # mark types
        debit.type = "TRANSFER_OUT"
        credit.type = "TRANSFER_IN"
        return debit, credit

    def list_transactions(self, account_id: str) -> List[Transaction]:
        return list(self.txs.get(account_id, []))

    # Invoices
    def create_invoice(self, customer_id: str, amount: Decimal, currency: str, due_date: date) -> Invoice:
        if customer_id not in self.customers:
            raise ValueError("Customer not found")
        inv = Invoice(
            invoice_id=self._id("INV"),
            customer_id=customer_id,
            amount=self._dec(amount),
            currency=currency,
            status="OPEN",
            due_date=due_date
        )
        self.invoices[inv.invoice_id] = inv
        return inv

    def pay_invoice(self, invoice_id: str) -> Invoice:
        inv = self.invoices[invoice_id]
        if inv.status != "OPEN":
            raise ValueError("INVALID_STATUS")
        inv.status = "PAID"
        return inv

    def invoice_status(self, invoice_id: str) -> str:
        return self.invoices[invoice_id].status

    # Loans
    def create_loan(self, customer_id: str, principal: Decimal, rate_apr: Decimal, term_months: int, currency: str) -> Loan:
        if customer_id not in self.customers:
            raise ValueError("Customer not found")
        loan = Loan(
            loan_id=self._id("LOAN"),
            customer_id=customer_id,
            principal=self._dec(principal),
            rate_apr=self._dec(rate_apr),
            term_months=int(term_months),
            currency=currency
        )
        self.loans[loan.loan_id] = loan
        return loan

    def calc_interest(self, principal: Decimal, rate_apr: Decimal, days: int) -> Decimal:
        rate = self._dec(rate_apr) / Decimal("100")
        interest = self._dec(principal) * rate * Decimal(days) / Decimal("365")
        return self._dec(interest)

    # FX (static demo rates)
    def fx_quote(self, base: str, quote: str) -> FxQuote:
        rates = {
            ("USD", "EUR"): Decimal("0.91000000"),
            ("EUR", "USD"): Decimal("1.09890110"),
            ("USD", "NPR"): Decimal("134.00000000"),
            ("NPR", "USD"): Decimal("0.00746269"),
            ("EUR", "NPR"): Decimal("147.40000000"),
            ("NPR", "EUR"): Decimal("0.00678426"),
        }
        rate = rates.get((base.upper(), quote.upper()))
        if rate is None:
            raise ValueError("PAIR_UNSUPPORTED")
        return FxQuote(base=base.upper(), quote=quote.upper(), rate=rate, timestamp=datetime.utcnow())

    # Statements
    def generate_statement(self, account_id: str, from_date: date, to_date: date) -> Statement:
        acc = self.accounts[account_id]
        lines: List[StatementLine] = []
        bal = Decimal("0")
        for t in self.txs.get(account_id, []):
            if from_date <= t.timestamp.date() <= to_date:
                bal = (bal + t.amount).quantize(Decimal("0.0001"))
                lines.append(
                    StatementLine(date=t.timestamp.date(), description=t.description, amount=t.amount, balance_after=bal)
                )
        return Statement(account_id=account_id, from_date=from_date, to_date=to_date, lines=lines)

    # Risk & KYC
    def risk_score(self, customer_id: str) -> RiskReport:
        if customer_id not in self.customers:
            raise ValueError("Customer not found")

        n_acc = sum(1 for a in self.accounts.values() if a.customer_id == customer_id)
        n_inv_open = sum(1 for i in self.invoices.values() if i.customer_id == customer_id and i.status == "OPEN")
        score = max(300, min(850, 700 + n_acc*10 - n_inv_open*30))
        band = "LOW" if score >= 700 else ("MEDIUM" if score >= 600 else "HIGH")
        return RiskReport(customer_id=customer_id, score=score, band=band, reason="Toy heuristic")
