Run server:
 python -m finance_soap.server

# Finance SOAP Suite

A **SOAP-based financial service API** built with [Spyne](https://spyne.io/).
This project demonstrates SOAP endpoints for handling finance-related operations such as managing customers, accounts, transactions, invoices, loans, and more.

## Important points
- SOAP supports WS-Security , enabling message-level encryption, digital signatures, and authentication.
- Built-in support for ACID-like transactional integrity using standards such as WS-AtomicTransaction. Ensures operations are completed fully or rolled back, avoiding partial transactions.
- SOAP uses WSDL, which clearly defines request/response structures. Prevents data inconsistency and enforces strict validation—imp incase of transactions.
- Supports WS-ReliableMessaging, ensuring messages are delivered once and in order. Reduces risks like duplicate or lost transactions.
- SOAP is fully platform-neutral and works reliably across Java, .NET, mainframes, and legacy systems.
- SOAP uses WSDL and XSD, enforcing strict data types and structures, which prevents invalid or inconsistent transaction data.
- SOAP messages are self-describing XML, making them easy to log, trace, and audit for compliance. It also supports security and logging standards required for PCI-DSS, SOX, ISO, and financial regulations.

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
