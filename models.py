# Expense model and report classes.
from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal, InvalidOperation


class Expense:
    def __init__(self, expense_id, amount, category, description, expense_date):
        try:
            value = Decimal(str(amount))
        except InvalidOperation:
            raise ValueError("Enter a valid numeric amount.")

        if not value.is_finite() or value <= 0:
            raise ValueError("Amount must be a positive, finite number.")

        # Store money with two decimal places.
        self.__amount = value.quantize(Decimal("0.01"))

        if self.__amount <= 0:
            raise ValueError("Amount must be at least Rs. 0.01.")

        category = category.strip().title()
        description = description.strip()

        if not category or not description:
            raise ValueError("Category and description cannot be empty.")

        # Validate the date.
        date.fromisoformat(expense_date)

        self.expense_id = expense_id
        self.category = category
        self.description = description
        self.expense_date = expense_date

    @property
    def amount(self):
        """Provide read access through a property."""
        return self.__amount

    def to_dict(self):
        """Convert the object into a JSON-compatible dictionary."""
        return {
            "expense_id": self.expense_id,
            "amount": str(self.__amount),
            "category": self.category,
            "description": self.description,
            "expense_date": self.expense_date
        }


# Abstract parent class.
class Report(ABC):
    @abstractmethod
    def generate(self, expenses):
        pass


class CategoryReport(Report):
    def generate(self, expenses):
        totals = {}

        for expense in expenses:
            key = expense.category
            totals[key] = totals.get(key, Decimal("0")) + expense.amount

        return totals


class MonthlyReport(Report):
    def generate(self, expenses):
        totals = {}

        for expense in expenses:
            key = expense.expense_date[:7]  # YYYY-MM
            totals[key] = totals.get(key, Decimal("0")) + expense.amount

        return totals


# Small demonstration; runs only when this file is executed directly.
if __name__ == "__main__":
    expenses = [
        Expense(1, "250", "food", "Lunch", "2026-10-23"),
        Expense(2, "150", "travel", "Bus fare", "2026-10-23")
    ]

    print("=== Expense Objects ===")
    for expense in expenses:
        print(expense.to_dict())

    print("\n=== Reports ===")
    for report in [CategoryReport(), MonthlyReport()]:
        print(report.__class__.__name__)
        for label, total in report.generate(expenses).items():
            print(f"{label}: Rs. {total:.2f}")