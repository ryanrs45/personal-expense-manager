# Interactive Personal Expense Manager.
from datetime import date
from decimal import InvalidOperation
from pathlib import Path

from manager import ExpenseManager
from storage import ExpenseStorage


def display_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    print("\nID | Date | Category | Amount | Description")
    print("-" * 70)

    for expense in expenses:
        print(
            f"{expense.expense_id} | "
            f"{expense.expense_date} | "
            f"{expense.category} | "
            f"Rs. {expense.amount:.2f} | "
            f"{expense.description}"
        )


def display_summary(title, totals):
    print(f"\n{title}")

    if not totals:
        print("No expenses available.")
        return

    for label, amount in sorted(totals.items()):
        print(f"{label}: Rs. {amount:.2f}")


def main():
    project_folder = Path(__file__).resolve().parent
    data_file = project_folder / "data" / "expenses.json"

    try:
        manager = ExpenseManager(ExpenseStorage(data_file))
    except (ValueError, OSError) as error:
        print(f"Cannot load saved expenses: {error}")
        print("Check the data file before restarting.")
        return

    while True:
        print("\n===== PERSONAL EXPENSE MANAGER =====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Search expenses")
        print("4. Delete expense")
        print("5. Category summary")
        print("6. Monthly summary")
        print("7. Total expenses")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                amount = input("Amount (Rs.): ").strip()
                category = input("Category: ").strip()
                description = input("Description: ").strip()
                expense_date = input(
                    "Date (YYYY-MM-DD, Enter for today): "
                ).strip()

                if not expense_date:
                    expense_date = date.today().isoformat()

                expense = manager.add_expense(
                    amount, category, description, expense_date
                )
                print(
                    f"Expense saved successfully. "
                    f"Record ID: {expense.expense_id}"
                )

            elif choice == "2":
                display_expenses(manager.get_all())

            elif choice == "3":
                keyword = input(
                    "Search category or description: "
                )
                display_expenses(manager.search(keyword))

            elif choice == "4":
                expense_id = int(input("Enter expense ID: "))

                if expense_id <= 0:
                    raise ValueError("Enter a positive expense ID.")

                confirmation = input(
                    f"Delete expense {expense_id}? (yes/no): "
                ).strip().lower()

                if confirmation == "yes":
                    if manager.delete_expense(expense_id):
                        print("Expense deleted successfully.")
                    else:
                        print("Expense ID not found.")
                else:
                    print("Deletion cancelled.")

            elif choice == "5":
                display_summary(
                    "Expenses by Category",
                    manager.category_summary()
                )

            elif choice == "6":
                display_summary(
                    "Expenses by Month",
                    manager.monthly_summary()
                )

            elif choice == "7":
                print(
                    f"Total expenses: "
                    f"Rs. {manager.total_amount():.2f}"
                )

            elif choice == "8":
                print("Thank you for using Personal Expense Manager!")
                break

            else:
                print("Invalid choice. Select a number from 1 to 8.")

        except InvalidOperation:
            print("Invalid amount. Enter a reasonable numeric value.")
        except ValueError as error:
            print(f"Invalid input: {error}")
        except OSError as error:
            print(f"File operation failed: {error}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nApplication closed.")