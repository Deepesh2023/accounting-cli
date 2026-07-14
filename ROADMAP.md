# 🚀 Printos Accounting - Development Roadmap

This document tracks the evolution of the Printos Accounting system from a basic CLI prototype to a professional, full-stack financial backend.

## 🎯 Project Goal
Transform a simple stock/sales tracker into a robust financial accounting system capable of supporting a web-based frontend (FastAPI) and providing accurate financial statements.

---

## ✅ Completed: Phase 0 - Architectural Foundation
*Focus: Decoupling and Dependency Injection*

- [x] **Layered Architecture**: Separated the app into Models $\rightarrow$ Repositories $\rightarrow$ Services $\rightarrow$ Workflows.
- [x] **Protocol-Based Design**: Introduced `shared/interfaces.py` to decouple business logic from storage implementation.
- [x] **Dependency Container**: Implemented a `Container` class to manage object lifecycles and injection.
- [x] **Professional Testing**: Added both Integration tests (Disk) and Unit tests (Mocks) to verify business logic.
- [x] **CLI Refactor**: Moved all `input/print` logic into `workflows.py`, leaving `service.py` as pure business logic.

---

## 🛠️ Planned: Phase 1 - The Accounting Core

### Sprint 1: The Purchase Cycle (The "Inflow")
**Goal**: Track how goods enter the business and the costs associated with them.
- [ ] **Accounting Lesson**: Introduction to Accounts Payable and Supplier relationships.
- [ ] **Implementation**: 
    - `Purchase` and `PurchaseItem` models.
    - `PurchaseService` for recording stock inflow.
    - CLI workflows to record purchases.
- [ ] **Verification**: Tests to ensure purchases correctly increase inventory stock.

### Sprint 2: Party Management (The "Who")
**Goal**: Move from simple "names" to a managed directory of business entities.
- [ ] **Accounting Lesson**: Understanding Debtors (Accounts Receivable) and Creditors (Accounts Payable).
- [ ] **Implementation**:
    - `Party` model (Contact info, balance, type).
    - Link `Sale` and `Purchase` records to specific `Party` IDs.
- [ ] **Verification**: Reports showing total outstanding balance per party.

### Sprint 3: Expenses & General Ledger (The "Leaks")
**Goal**: Track money spent on non-inventory items (Rent, Utilities, etc.).
- [ ] **Accounting Lesson**: Direct vs. Indirect Expenses and their impact on Net Profit.
- [ ] **Implementation**:
    - `Expense` module and repository.
    - Transaction logging for all cash/bank movements.
- [ ] **Verification**: Expense reports categorized by type.

### Sprint 4: Financial Statements (The "Truth")
**Goal**: Automate the creation of professional financial reports.
- [ ] **Accounting Lesson**: Building a Trading Account, P&L Statement, and Balance Sheet.
- [ ] **Implementation**:
    - `FinancialService` to calculate Gross/Net profit and equity.
    - Workflows to display a formatted Balance Sheet.
- [ ] **Verification**: Cross-referencing sales/purchases to ensure the Balance Sheet tallies.

---

## 🌐 Future Phase: Web Transition
- [ ] Replace CLI Workflows with **FastAPI** endpoints.
- [ ] Replace JSON Storage with a **SQL Database** (PostgreSQL).
- [ ] Integrate with the **React Frontend** prototype.
