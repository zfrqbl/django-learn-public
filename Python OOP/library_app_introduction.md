[Python OOP notes](https://docs.google.com/... "Click to view OOP notes")

# Library Management System: An OOP Demonstration

## Introduction

Welcome, aspiring developers! This project provides a hands-on, practical example of building a simple **Library Management System** using Python. More importantly, it serves as an excellent illustration of core **Object-Oriented Programming (OOP)** principles.

As junior developers, understanding OOP is crucial for writing clean, modular, and maintainable code. This application is designed to help you see these concepts in action.

## What You'll Find in This Project

The `library_app.py` file you're looking at implements a basic library system that allows you to:

* **Manage Books**: Add new books, including different types like **Fiction** and **Non-Fiction**.
* **Manage Members**: Add new library members.
* **Handle Loans**: Process the borrowing and returning of books by members.
* **Persist Data**: All your library's information (books and members) is saved to a CSV file (`data.csv`) and loaded automatically when the application starts, so your data isn't lost.

## OOP Concepts Illustrated

This project is structured to showcase several key OOP concepts:

* **Classes and Objects**: You'll see how real-world entities like `Book`, `Member`, and `Librarian` are modeled as Python classes, and how individual instances of these classes (objects) interact.
* **Inheritance**: The `FictionBook` and `NonFictionBook` classes extend the base `Book` class, demonstrating how to reuse code and create specialized types of objects.
* **Encapsulation**: Data (attributes) within each object is managed and accessed primarily through methods, protecting the internal state and ensuring data integrity.
* **Polymorphism**: Notice how different types of books (`Book`, `FictionBook`, `NonFictionBook`) can be treated uniformly (e.g., when saving to CSV or displaying details), yet behave differently based on their specific type.
* **Composition**: The `Librarian` class manages collections of `Book` and `Member` objects, illustrating how objects can be composed to build more complex systems.
* **Exception Handling**: Custom error types are used to provide clear and specific feedback when operations cannot be completed (e.g., trying to borrow a book that's already out).
* **Type Hinting**: Modern Python best practices are used with type hints to improve code readability and help catch potential errors during development.

## How to Use

1.  **Save the Code**: Save the provided Python code as `library_app.py`.
2.  **Run the Application**: Open your terminal or command prompt, navigate to the directory where you saved the file, and run:
    ```bash
    python library_app.py
    ```
3.  **Interact**: Follow the prompts in the terminal to add books, members, borrow books, return books, and explore the library's state.
4.  **Observe `data.csv`**: A file named `data.csv` will be created (or updated) in the same directory. Open it with a text editor or spreadsheet program to see how the object data is persisted.

## Learning Objectives for Junior Devs

As you explore this code, pay close attention to:

* How each class is defined and what attributes and methods it contains.
* How `super().__init__()` is used in subclasses.
* The role of `to_csv_row()` in preparing data for saving.
* How `_load_data()` intelligently reconstructs objects of different types from the CSV.
* The logic within `borrow_book()` and `return_book()` and how they handle interactions between `Member` and `Book` objects.
* The custom exceptions and how they're raised and caught.
