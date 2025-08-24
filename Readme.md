Run server:
 python -m finance_soap.server

# Finance SOAP Suite

A **SOAP-based financial service API** built with [Spyne](https://spyne.io/).
This project demonstrates SOAP endpoints for handling finance-related operations such as managing customers, accounts, transactions, invoices, loans, and more.



##  Features
- SOAP 1.1 web service with multiple operations
- Customer, Account, Transaction, Invoice, Loan, Statement, FX Quotes, Risk Report, and KYC service schemas
- In-memory repository for demonstration (can be extended to database)
- WSDL auto-generated for easy integration
- Built with Python 3 and Spyne


## Note:
- Always use POST requests with Content-Type: text/xml for SOAP calls.
- WSDL is auto-generated and can be consumed by SOAP UI, Postman, or client SDKs.
- The in-memory repo can be swapped with a database-backed repository for persistence.
