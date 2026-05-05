import datetime
from typing import Dict, List, Optional, Union
import random

class AccountingSystem:
    def __init__(self):
        # Chart of Accounts: {account_id: {"name": str, "type": str, "balance": float, "normal_balance": str}}
        self.chart_of_accounts: Dict[str, Dict] = {}

        # Transactions: {transaction_id: {"date": str, "account": str, "amount": float, "description": str, "type": str, "status": str}}
        self.transactions: Dict[str, Dict] = {}

        # Internal Controls: {control_id: {"name": str, "description": str, "compliance_status": bool, "last_audit": str}}
        self.internal_controls: Dict[str, Dict] = {}

        # Finance Team: {employee_id: {"name": str, "role": str, "training_status": str, "performance": float}}
        self.finance_team: Dict[str, Dict] = {}

        # Financial Statements: {statement_id: {"name": str, "data": Dict, "date": str}}
        self.financial_statements: Dict[str, Dict] = {}

        # Audit Logs: List[Dict]
        self.audit_logs: List[Dict] = []

        # Next IDs for auto-increment
        self.next_account_id = 1
        self.next_transaction_id = 1
        self.next_control_id = 1
        self.next_employee_id = 1
        self.next_statement_id = 1

    # --- Chart of Accounts (Zoho/QuickBooks-like) ---
    def add_account(self, name: str, account_type: str, normal_balance: str = "Debit") -> str:
        """Add an account to the chart of accounts (e.g., Assets, Liabilities, Equity, Revenue, Expenses)."""
        account_id = f"ACCT{self.next_account_id}"
        self.chart_of_accounts[account_id] = {
            "name": name,
            "type": account_type,
            "balance": 0.0,
            "normal_balance": normal_balance  # "Debit" or "Credit"
        }
        self.next_account_id += 1
        self._log_audit(f"Added account: {name} ({account_id})")
        return f"Account '{name}' added with ID: {account_id}"

    def update_account_balance(self, account_id: str, amount: float, transaction_type: str = "Debit") -> str:
        """Update account balance based on transaction type (Debit/Credit)."""
        if account_id in self.chart_of_accounts:
            account = self.chart_of_accounts[account_id]
            if (transaction_type == "Debit" and account["normal_balance"] == "Debit") or \
               (transaction_type == "Credit" and account["normal_balance"] == "Credit"):
                account["balance"] += amount
            else:
                account["balance"] -= amount
            self._log_audit(f"Updated balance for {account['name']}: {transaction_type} ₦{amount:,.2f}")
            return f"Balance updated for {account['name']}: ₦{account['balance']:,.2f}"
        return f"Account ID {account_id} not found."

    # --- Transactions (Full-Cycle Automation) ---
    def record_transaction(self, account_id: str, amount: float, description: str, transaction_type: str = "Debit") -> str:
        """Record a financial transaction (e.g., Journal Entry, Invoice, Payment)."""
        if account_id in self.chart_of_accounts:
            transaction_id = f"TXN{self.next_transaction_id}"
            self.transactions[transaction_id] = {
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "account": account_id,
                "amount": amount,
                "description": description,
                "type": transaction_type,
                "status": "Posted"
            }
            self.update_account_balance(account_id, amount, transaction_type)
            self.next_transaction_id += 1
            self._log_audit(f"Recorded transaction: {description} (₦{amount:,.2f})")
            return f"Transaction {transaction_id} recorded: {description}"
        return f"Account ID {account_id} not found."

    # --- Internal Controls (GAAP/SAP FCM Compliance) ---
    def add_internal_control(self, name: str, description: str) -> str:
        """Add an internal control policy (e.g., Segregation of Duties, Approval Hierarchies)."""
        control_id = f"CTRL{self.next_control_id}"
        self.internal_controls[control_id] = {
            "name": name,
            "description": description,
            "compliance_status": True,
            "last_audit": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        self.next_control_id += 1
        self._log_audit(f"Added internal control: {name}")
        return f"Internal control '{name}' added with ID: {control_id}"

    def audit_controls(self) -> Dict[str, List[str]]:
        """Audit all internal controls and return compliance status."""
        results = {"compliant": [], "non_compliant": []}
        for control_id, control in self.internal_controls.items():
            if control["compliance_status"]:
                results["compliant"].append(f"{control['name']} (Last Audited: {control['last_audit']})")
            else:
                results["non_compliant"].append(f"{control['name']} (Last Audited: {control['last_audit']})")
        self._log_audit("Conducted internal controls audit")
        return results

    # --- Finance Team Management ---
    def add_team_member(self, name: str, role: str) -> str:
        """Add a finance team member."""
        employee_id = f"EMP{self.next_employee_id}"
        self.finance_team[employee_id] = {
            "name": name,
            "role": role,
            "training_status": "Pending",
            "performance": 0.0
        }
        self.next_employee_id += 1
        self._log_audit(f"Added team member: {name} ({role})")
        return f"Team member '{name}' added with ID: {employee_id}"

    def update_training_status(self, employee_id: str, status: str, performance: float = 0.0) -> str:
        """Update training status and performance for a team member."""
        if employee_id in self.finance_team:
            self.finance_team[employee_id]["training_status"] = status
            self.finance_team[employee_id]["performance"] = performance
            self._log_audit(f"Updated training for {self.finance_team[employee_id]['name']}: {status}")
            return f"Training status updated for {self.finance_team[employee_id]['name']}: {status}"
        return f"Employee ID {employee_id} not found."

    # --- Financial Reporting (Strategic Audits) ---
    def generate_financial_statement(self, statement_type: str, data: Dict) -> str:
        """Generate a financial statement (e.g., Balance Sheet, Income Statement, Cash Flow)."""
        statement_id = f"STMT{self.next_statement_id}"
        self.financial_statements[statement_id] = {
            "name": statement_type,
            "data": data,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.next_statement_id += 1
        self._log_audit(f"Generated {statement_type}")
        return f"Financial statement '{statement_type}' generated with ID: {statement_id}"

    def get_financial_statement(self, statement_id: str) -> Optional[Dict]:
        """Retrieve a financial statement by ID."""
        return self.financial_statements.get(statement_id)

    # --- Audit Logging ---
    def _log_audit(self, action: str) -> None:
        """Log an action to the audit trail."""
        self.audit_logs.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "user": "System"  # In a real system, this would be the logged-in user
        })

    def get_audit_logs(self) -> List[Dict]:
        """Retrieve all audit logs."""
        return self.audit_logs

    # --- Efficiency Metrics (40% Increase Simulation) ---
    def calculate_efficiency_improvement(self, baseline_process_time: float) -> float:
        """Simulate a 40% increase in process efficiency (e.g., manual vs. automated)."""
        improved_time = baseline_process_time * 0.60  # 40% faster
        return improved_time

# --- Example Usage ---
if __name__ == "__main__":
    system = AccountingSystem()

    # Set up Chart of Accounts (GAAP-compliant)
    print("=== Setting Up Chart of Accounts ===")
    print(system.add_account("Cash", "Asset", "Debit"))
    print(system.add_account("Accounts Payable", "Liability", "Credit"))
    print(system.add_account("Revenue", "Revenue", "Credit"))
    print(system.add_account("Salaries Expense", "Expense", "Debit"))

    # Record transactions (Full-Cycle Automation)
    print("\n=== Recording Transactions ===")
    print(system.record_transaction("ACCT1", 5_000_000.00, "Initial Cash Deposit", "Debit"))
    print(system.record_transaction("ACCT2", 2_000_000.00, "Vendor Payment", "Credit"))
    print(system.record_transaction("ACCT3", 3_000_000.00, "Service Revenue", "Credit"))

    # Add Internal Controls (GAAP/SAP FCM)
    print("\n=== Adding Internal Controls ===")
    print(system.add_internal_control("Segregation of Duties", "No single person should handle all aspects of a transaction."))
    print(system.add_internal_control("Approval Hierarchy", "All payments over ₦1M require managerial approval."))
    print("Audit Results:", system.audit_controls())

    # Manage Finance Team
    print("\n=== Managing Finance Team ===")
    print(system.add_team_member("John Doe", "Senior Accountant"))
    print(system.add_team_member("Jane Smith", "Financial Analyst"))
    print(system.update_training_status("EMP1", "Completed", 95.0))
    print(system.update_training_status("EMP2", "In Progress", 75.0))

    # Generate Financial Statements
    print("\n=== Generating Financial Statements ===")
    balance_sheet_data = {
        "assets": {"Cash": 5_000_000.00, "Accounts Receivable": 1_000_000.00},
        "liabilities": {"Accounts Payable": 2_000_000.00},
        "equity": {"Retained Earnings": 4_000_000.00}
    }
    print(system.generate_financial_statement("Balance Sheet", balance_sheet_data))

    income_statement_data = {
        "revenue": {"Service Revenue": 3_000_000.00},
        "expenses": {"Salaries Expense": 500_000.00, "Rent Expense": 200_000.00},
        "net_income": 2_300_000.00
    }
    print(system.generate_financial_statement("Income Statement", income_statement_data))

    # Simulate Efficiency Improvement
    print("\n=== Efficiency Metrics ===")
    baseline_time = 100.0  # Hours (manual process)
    improved_time = system.calculate_efficiency_improvement(baseline_time)
    print(f"Process efficiency improved from {baseline_time} hours to {improved_time} hours (40% increase).")

    # Display Audit Logs
    print("\n=== Audit Logs ===")
    for log in system.get_audit_logs():
        print(f"{log['timestamp']}: {log['action']}")
