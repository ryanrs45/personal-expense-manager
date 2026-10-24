# Manage expenses and save changes using ExpenseStorage.
from datetime import date
from decimal import Decimal

from models import Expense, CategoryReport, MonthlyReport
from storage import ExpenseStorage


class ExpenseManager:
    def __init__(self, storage):
        self.storage = storage
        self.__expenses = storage.load()

    def get_all(self):
        return list(self.__expenses)

    def add_expense(self, amount, category, description, expense_date):
        # Store dates consistently as YYYY-MM-DD.
        expense_date = date.fromisoformat(expense_date).isoformat()

        next_id = max(
            (expense.expense_id for expense in self.__expenses),
            default=0
        ) + 1

        expense = Expense(
            next_id, amount, category, description, expense_date
        )

        updated_expenses = self.__expenses + [expense]
        self.storage.save(updated_expenses)
        self.__expenses = updated_expenses
        return expense

    def search(self, keyword):
        keyword = keyword.strip().casefold()

        if not keyword:
            raise ValueError("Enter a search keyword.")

        return [
            expense
            for expense in self.__expenses
            if keyword in expense.category.casefold()
            or keyword in expense.description.casefold()
        ]

    def delete_expense(self, expense_id):
        updated_expenses = [
            expense
            for expense in self.__expenses
            if expense.expense_id != expense_id
        ]

        if len(updated_expenses) == len(self.__expenses):
            return False

        self.storage.save(updated_expenses)
        self.__expenses = updated_expenses
        return True

    def total_amount(self):
        return sum(
            (expense.amount for expense in self.__expenses),
            Decimal("0.00")
        )

    def category_summary(self):
        return CategoryReport().generate(self.__expenses)

    def monthly_summary(self):
        return MonthlyReport().generate(self.__expenses)


if __name__ == "__main__":
    from pathlib import Path
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as folder:
        storage = ExpenseStorage(Path(folder) / "expenses.json")
        manager = ExpenseManager(storage)

        manager.add_expense(
            "250", "Food", "Lunch", "2026-10-23"
        )
        manager.add_expense(
            "150", "Travel", "Bus fare", "2026-10-23"
        )

        print("Records added:", len(manager.get_all()))
        print(f"Total expenses: Rs. {manager.total_amount():.2f}")

        print("\nSearch results for 'food':")
        for expense in manager.search("food"):
            print(
                f"{expense.expense_id}: {expense.description}"
                f" - Rs. {expense.amount:.2f}"
            )

        print("\nCategory summary:")
        for category, total in manager.category_summary().items():
            print(f"{category}: Rs. {total:.2f}")

        print("\nMonthly summary:")
        for month, total in manager.monthly_summary().items():
            print(f"{month}: Rs. {total:.2f}")

        print("\nDelete record 2:", manager.delete_expense(2))
        print("Remaining records:", len(manager.get_all()))

        # Confirm that the deletion was saved to JSON.
        reloaded_manager = ExpenseManager(storage)
        print(
            "Records after reloading:",
            len(reloaded_manager.get_all())
        )