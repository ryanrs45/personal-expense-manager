# Personal Expense Manager

Student: Hemanth Ghanta
Internship: Python Programming — InternNova
Week: 6

## Project Description
A Python application to record expenses and review spending.

## Features
- Add and display expenses.
- Search by category or description.
- Delete expenses with confirmation.
- Show category and monthly summaries.
- Calculate total spending.
- Save records in a JSON file.
- Handle invalid input and file errors.

## Technologies Used
Python 3, Visual Studio Code, Git and GitHub.
Only Python standard library modules are required.

## Python Concepts Used
Variables, input/output, conditions, loops, functions,
lists, dictionaries, sets, file handling and exceptions.

OOP concepts:
- Classes and constructors: Expense and ExpenseManager.
- Inheritance: CategoryReport and MonthlyReport inherit Report.
- Polymorphism: both report classes implement generate().
- Encapsulation: private amount with a read-only property.
- Abstraction: Report contains an abstract generate() method.

## Project Files
- main.py: interactive menu.
- models.py: expense model and report classes.
- storage.py: JSON saving and loading.
- manager.py: expense operations.
- screenshots/: output and Git workflow screenshots.

## Installation and Setup
Install Python 3.
Download or clone the repository.
Open a terminal in the project folder.
No additional packages are needed.

## How to Run
Run this command:

python main.py

Select an option from 1 to 8.
Enter dates as YYYY-MM-DD or press Enter for today.

The application creates data/expenses.json automatically.
Personal records are excluded from Git.

## Future Improvements
- Edit expense records.
- Add monthly budgets.
- Export reports to CSV.
- Add charts and a graphical interface.
- Use SQLite for larger datasets.