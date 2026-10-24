# Save and load expense objects using JSON.
import json
from pathlib import Path

from models import Expense


class ExpenseStorage:
    def __init__(self, filename):
        self.path = Path(filename)

    def load(self):
        try:
            with self.path.open("r", encoding="utf-8") as file:
                records = json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as error:
            raise ValueError(
                "The expense file contains invalid JSON. "
                "Repair it before continuing."
            ) from error

        if not isinstance(records, list):
            raise ValueError("The expense file must contain a list.")

        expenses = []
        seen_ids = set()

        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Each expense record must be a dictionary.")

            try:
                expense = Expense(**record)
            except (TypeError, ValueError, ArithmeticError) as error:
                raise ValueError(
                    "The expense file contains an invalid record."
                ) from error

            expense_id = expense.expense_id

            if type(expense_id) is not int or expense_id <= 0:
                raise ValueError("Expense IDs must be positive integers.")

            if expense_id in seen_ids:
                raise ValueError("Duplicate expense IDs found.")

            seen_ids.add(expense_id)
            expenses.append(expense)

        return expenses

    def save(self, expenses):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(".tmp")

        try:
            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(
                    [expense.to_dict() for expense in expenses],
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            # Replace the saved file only after writing succeeds.
            temporary_path.replace(self.path)

        finally:
            if temporary_path.exists():
                temporary_path.unlink()


if __name__ == "__main__":
    # Test in a temporary folder without changing project data.
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as folder:
        storage = ExpenseStorage(Path(folder) / "expenses.json")

        print("Before saving:", len(storage.load()), "records")

        examples = [
            Expense(1, "250", "Food", "Lunch", "2026-10-23"),
            Expense(2, "150", "Travel", "Bus fare", "2026-10-23")
        ]

        storage.save(examples)
        loaded_expenses = storage.load()

        print("After loading:", len(loaded_expenses), "records")

        for expense in loaded_expenses:
            print(
                f"{expense.expense_id}: {expense.category} "
                f"- Rs. {expense.amount:.2f}"
            )

        print("JSON save and load completed successfully.")