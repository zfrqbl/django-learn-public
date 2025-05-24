"""
Library Management System - OOP Demonstration

This program demonstrates key Object-Oriented Programming concepts in Python:
- Classes and objects
- Inheritance
- Encapsulation
- Polymorphism
- Exception handling
- Type hints
- Data persistence (CSV file storage)

The system models a library with books, members, and librarian operations.
"""

import csv
from typing import List, Dict, Optional, TypeVar

# Define custom exceptions
# Using custom exceptions makes error handling more specific and meaningful
class LibraryError(Exception):
    """Base exception class for all library-related errors."""
    pass

class BookNotFoundException(LibraryError):
    """Raised when attempting to access a book that doesn't exist in the library."""
    pass

class BookAlreadyBorrowedException(LibraryError):
    """Raised when trying to borrow a book that's already checked out."""
    pass

class MemberNotFoundException(LibraryError):
    """Raised when attempting to access a member that doesn't exist."""
    pass

class BookNotBorrowedByMemberException(LibraryError):
    """Raised when a member tries to return a book they didn't borrow."""
    pass

class BookNotAvailableException(LibraryError):
    """Raised when trying to borrow a book that is not available."""
    pass

# Type variable for Book and its subclasses
# This enables type hints to work with the Book class and any of its subclasses
TBook = TypeVar('TBook', bound='Book')

class Book:
    """
    Represents a generic book in the library.
    
    Attributes:
        title (str): The title of the book
        author (str): The author of the book
        isbn (str): The unique ISBN identifier
        is_borrowed (bool): Whether the book is currently borrowed
    
    Methods:
        __str__: Returns a formatted string representation of the book
        to_csv_row: Converts book data to CSV format for storage
    """
    
    def __init__(self, title: str, author: str, isbn: str, is_borrowed: bool = False):
        """
        Initializes a new Book instance.
        
        Args:
            title: The title of the book
            author: The author of the book
            isbn: The unique ISBN identifier
            is_borrowed: Whether the book is currently borrowed (defaults to False)
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = is_borrowed

    def __str__(self) -> str:
        """Returns a human-readable string representation of the book."""
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Status: {status}"

    def to_csv_row(self) -> List[str]:
        """
        Converts the book's data to a CSV row format.
        
        Returns:
            List[str]: A list of strings representing the book's data in CSV format
        """
        return ["BOOK", self.isbn, self.title, self.author, str(self.is_borrowed), ""]


class FictionBook(Book):
    """
    Represents a fiction book, inheriting from Book.
    Adds a genre attribute specific to fiction books.
    
    Attributes:
        genre (str): The genre of the fiction book (e.g., "Science Fiction")
    """
    
    def __init__(self, title: str, author: str, isbn: str, genre: str, is_borrowed: bool = False):
        """
        Initializes a new FictionBook instance.
        
        Args:
            title: The title of the book
            author: The author of the book
            isbn: The unique ISBN identifier
            genre: The genre of the fiction book
            is_borrowed: Whether the book is currently borrowed (defaults to False)
        """
        super().__init__(title, author, isbn, is_borrowed)
        self.genre = genre

    def __str__(self) -> str:
        """Returns a string representation including the book's genre."""
        return f"{super().__str__()}, Genre: {self.genre}"

    def to_csv_row(self) -> List[str]:
        """
        Converts the fiction book's data to a CSV row format.
        
        Returns:
            List[str]: A list of strings representing the book's data in CSV format,
                      including the genre information
        """
        return ["FICTION_BOOK", self.isbn, self.title, self.author, str(self.is_borrowed), self.genre]


class NonFictionBook(Book):
    """
    Represents a non-fiction book, inheriting from Book.
    Adds a subject_area attribute specific to non-fiction books.
    
    Attributes:
        subject_area (str): The subject area of the non-fiction book (e.g., "Science")
    """
    
    def __init__(self, title: str, author: str, isbn: str, subject_area: str, is_borrowed: bool = False):
        """
        Initializes a new NonFictionBook instance.
        
        Args:
            title: The title of the book
            author: The author of the book
            isbn: The unique ISBN identifier
            subject_area: The subject area of the non-fiction book
            is_borrowed: Whether the book is currently borrowed (defaults to False)
        """
        super().__init__(title, author, isbn, is_borrowed)
        self.subject_area = subject_area

    def __str__(self) -> str:
        """Returns a string representation including the book's subject area."""
        return f"{super().__str__()}, Subject Area: {self.subject_area}"

    def to_csv_row(self) -> List[str]:
        """
        Converts the non-fiction book's data to a CSV row format.
        
        Returns:
            List[str]: A list of strings representing the book's data in CSV format,
                      including the subject area information
        """
        return ["NON_FICTION_BOOK", self.isbn, self.title, self.author, str(self.is_borrowed), self.subject_area]


class Member:
    """
    Represents a library member who can borrow books.
    
    Attributes:
        member_id (str): Unique identifier for the member
        name (str): The member's name
        borrowed_books (List[Book]): List of Book objects currently borrowed
        _borrowed_books_isbns (List[str]): List of ISBNs of borrowed books (for CSV storage)
    
    Methods:
        __str__: Returns a formatted string representation of the member
        to_csv_row: Converts member data to CSV format for storage
    """
    
    def __init__(self, member_id: str, name: str, borrowed_books_isbns: Optional[List[str]] = None):
        """
        Initializes a new Member instance.
        
        Args:
            member_id: Unique identifier for the member
            name: The member's name
            borrowed_books_isbns: List of ISBNs of books currently borrowed (optional)
        """
        self.member_id = member_id
        self.name = name
        # Store ISBNs temporarily until Book objects are loaded
        self._borrowed_books_isbns: List[str] = borrowed_books_isbns if borrowed_books_isbns is not None else []
        # This will be populated with actual Book objects after loading
        self.borrowed_books: List[Book] = []

    def __str__(self) -> str:
        """Returns a human-readable string representation of the member."""
        return f"Member ID: {self.member_id}, Name: {self.name}, Books Borrowed: {len(self.borrowed_books)}"

    def to_csv_row(self) -> List[str]:
        """
        Converts the member's data to a CSV row format.
        
        Returns:
            List[str]: A list of strings representing the member's data in CSV format,
                      including a semicolon-separated list of borrowed book ISBNs
        """
        # Update ISBN list from current Book objects before saving
        self._borrowed_books_isbns = [book.isbn for book in self.borrowed_books]
        return ["MEMBER", self.member_id, self.name, ";".join(self._borrowed_books_isbns)]


class Librarian:
    """
    The core class that manages all library operations and data persistence.
    
    Attributes:
        librarian_id (str): Unique identifier for the librarian
        name (str): The librarian's name
        books (List[Book]): List of all books in the library
        members (List[Member]): List of all library members
        CSV_FILE (str): Path to the CSV file for data storage
        HEADERS (List[str]): Column headers for the CSV file
    
    Methods:
        _load_data: Loads data from CSV file into memory
        _save_data: Saves current data to CSV file
        add_book: Adds a new book to the library
        add_member: Adds a new member to the library
        find_book: Finds a book by ISBN
        find_member: Finds a member by ID
        borrow_book: Handles book borrowing process
        return_book: Handles book return process
    """
    
    CSV_FILE = "data.csv"
    HEADERS = ["TYPE", "ID/ISBN", "TITLE/NAME", "AUTHOR/BORROWED_ISBNs", "IS_BORROWED", "GENRE"]

    def __init__(self, librarian_id: str, name: str):
        """
        Initializes a new Librarian instance and loads existing data.
        
        Args:
            librarian_id: Unique identifier for the librarian
            name: The librarian's name
        """
        self.librarian_id = librarian_id
        self.name = name
        self.books: List[Book] = []
        self.members: List[Member] = []
        self._load_data()  # Load existing data when Librarian is created

    def __str__(self) -> str:
        """Returns a human-readable string representation of the librarian."""
        return f"Librarian ID: {self.librarian_id}, Name: {self.name}"

    def _load_data(self) -> None:
        """
        Loads library data from the CSV file.
        
        Reads the CSV file and recreates the Book and Member objects in memory.
        Handles different book types (generic, fiction, non-fiction) appropriately.
        """
        self.books = []
        self.members = []
        # Temporary storage for member borrowed book ISBNs until Book objects are loaded
        member_borrowed_mapping: Dict[str, List[str]] = {}

        try:
            with open(self.CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row

                for row in reader:
                    row_type = row[0]
                    # Check row length before processing to avoid IndexError
                    if row_type == "BOOK" and len(row) >= 5:
                        # Create a generic Book instance
                        isbn, title, author, is_borrowed_str = row[1], row[2], row[3], row[4]
                        self.books.append(Book(title, author, isbn, is_borrowed=is_borrowed_str.lower() == 'true'))
                    elif row_type == "FICTION_BOOK" and len(row) >= 6:
                        # Create a FictionBook instance
                        isbn, title, author, is_borrowed_str, genre = row[1], row[2], row[3], row[4], row[5]
                        self.books.append(FictionBook(title, author, isbn, genre, is_borrowed=is_borrowed_str.lower() == 'true'))
                    elif row_type == "NON_FICTION_BOOK" and len(row) >= 6:
                        # Create a NonFictionBook instance
                        isbn, title, author, is_borrowed_str, subject_area = row[1], row[2], row[3], row[4], row[5]
                        self.books.append(NonFictionBook(title, author, isbn, subject_area, is_borrowed=is_borrowed_str.lower() == 'true'))
                    elif row_type == "MEMBER" and len(row) >= 4:
                        # Create a Member instance
                        member_id, name, borrowed_isbns_str = row[1], row[2], row[3]
                        borrowed_books_isbns = borrowed_isbns_str.split(';') if borrowed_isbns_str else []
                        member = Member(member_id, name, borrowed_books_isbns=borrowed_books_isbns)
                        self.members.append(member)
                        member_borrowed_mapping[member_id] = borrowed_books_isbns

            # After loading all books, connect members with their borrowed Book objects
            for member in self.members:
                if member.member_id in member_borrowed_mapping:
                    for isbn in member_borrowed_mapping[member.member_id]:
                        book = self.find_book(isbn)
                        if book:
                            member.borrowed_books.append(book)
                        else:
                            print(f"Warning: Book with ISBN {isbn} for member {member.name} not found during load.")
            print(f"Data loaded from {self.CSV_FILE}.")

        except FileNotFoundError:
            print(f"'{self.CSV_FILE}' not found. Starting with empty library.")
            # Create an empty CSV with headers if it doesn't exist
            self._write_headers_to_csv()
        except Exception as e:
            print(f"Error loading data: {e}")

    def _write_headers_to_csv(self) -> None:
        """Writes the CSV headers to the file if it doesn't exist."""
        with open(self.CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.HEADERS)

    def _save_data(self) -> None:
        """Saves all current library data to the CSV file."""
        try:
            with open(self.CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.HEADERS)  # Write header first

                # Write all books to CSV
                for book in self.books:
                    writer.writerow(book.to_csv_row())
                # Write all members to CSV
                for member in self.members:
                    writer.writerow(member.to_csv_row())
            print(f"Data saved to {self.CSV_FILE}.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_book(self, book: TBook) -> None:
        """
        Adds a new book to the library's collection.
        
        Args:
            book: The Book object to add (can be Book or any subclass)
        
        Note:
            Checks for duplicate ISBNs before adding.
            Automatically saves changes to CSV file.
        """
        if any(b.isbn == book.isbn for b in self.books):
            print(f"Warning: A book with ISBN {book.isbn} already exists in the library.")
            return
        self.books.append(book)
        print(f"Added book: {book.title}")
        self._save_data()  # Persist changes

    def add_member(self, member: Member) -> None:
        """
        Adds a new member to the library's records.
        
        Args:
            member: The Member object to add
        
        Note:
            Checks for duplicate member IDs before adding.
            Automatically saves changes to CSV file.
        """
        if any(m.member_id == member.member_id for m in self.members):
            print(f"Warning: A member with ID {member.member_id} already exists in the library.")
            return
        self.members.append(member)
        print(f"Added member: {member.name}")
        self._save_data()  # Persist changes

    def find_book(self, isbn: str) -> Optional[Book]:
        """
        Finds a book by its ISBN.
        
        Args:
            isbn: The ISBN to search for
        
        Returns:
            Optional[Book]: The Book object if found, None otherwise
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def find_member(self, member_id: str) -> Optional[Member]:
        """
        Finds a member by their ID.
        
        Args:
            member_id: The member ID to search for
        
        Returns:
            Optional[Member]: The Member object if found, None otherwise
        """
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def borrow_book(self, member_id: str, isbn: str) -> None:
        """
        Handles the process of a member borrowing a book.
        
        Args:
            member_id: ID of the member borrowing the book
            isbn: ISBN of the book to be borrowed
        
        Raises:
            MemberNotFoundException: If member doesn't exist
            BookNotFoundException: If book doesn't exist
            BookAlreadyBorrowedException: If book is already borrowed
        """
        try:
            member = self.find_member(member_id)
            if not member:
                raise MemberNotFoundException(f"Member with ID {member_id} not found.")

            book = self.find_book(isbn)
            if not book:
                raise BookNotFoundException(f"Book with ISBN {isbn} not found.")

            if book.is_borrowed:
                raise BookAlreadyBorrowedException(f"Book '{book.title}' (ISBN: {isbn}) is already borrowed.")

            if book in member.borrowed_books:
                raise BookAlreadyBorrowedException(f"Member {member.name} already has '{book.title}' (ISBN: {isbn}) borrowed.")

            # Update book and member records
            book.is_borrowed = True
            member.borrowed_books.append(book)
            print(f"'{book.title}' borrowed by {member.name}.")
            self._save_data()  # Persist changes

        except LibraryError as e:
            print(f"Error borrowing book: {e}. Please check the details and try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def return_book(self, member_id: str, isbn: str) -> None:
        """
        Handles the process of a member returning a book.
        
        Args:
            member_id: ID of the member returning the book
            isbn: ISBN of the book to be returned
        
        Raises:
            MemberNotFoundException: If member doesn't exist
            BookNotFoundException: If book doesn't exist
            BookNotBorrowedByMemberException: If member didn't borrow the book
        """
        try:
            member = self.find_member(member_id)
            if not member:
                raise MemberNotFoundException(f"Member with ID {member_id} not found.")

            book = self.find_book(isbn)
            if not book:
                raise BookNotFoundException(f"Book with ISBN {isbn} not found.")

            if not book.is_borrowed:
                raise BookNotAvailableException(f"Book '{book.title}' (ISBN: {isbn}) was not borrowed.")

            if book not in member.borrowed_books:
                raise BookNotBorrowedByMemberException(f"Book '{book.title}' (ISBN: {isbn}) was not borrowed by member {member.name}.")

            # Update book and member records
            book.is_borrowed = False
            member.borrowed_books.remove(book)
            print(f"'{book.title}' returned by {member.name}.")
            self._save_data()  # Persist changes

        except LibraryError as e:
            print(f"Error returning book: {e}. Please check the details and try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


# Main application execution
if __name__ == "__main__":
    """
    The main entry point of the program when run directly.
    
    Creates a Librarian instance and provides a menu-driven interface
    for interacting with the library system.
    """
    
    # Initialize the librarian - data will be loaded automatically
    name: str = input("Enter your name: ")
    my_librarian = Librarian("L001", name)
    print(f"\n{my_librarian}")
    print("-" * 30)
    
    # Add some initial books and members if the library is empty
    if not my_librarian.books and not my_librarian.members:
        print("\n--- Initializing Library with Dummy Data ---")
        # Create sample books of different types
        book1 = Book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "978-0345391803")
        book2 = FictionBook("Dune", "Frank Herbert", "978-0441172719", "Science Fiction")
        book3 = NonFictionBook("Cosmos", "Carl Sagan", "978-0345539434", "Astronomy")
        book4 = Book("Python Crash Course", "Eric Matthes", "978-1593279288")
        book5 = Book("Clean Code", "Robert C. Martin", "978-0132350884")

        # Add books to library
        my_librarian.add_book(book1)
        my_librarian.add_book(book2)
        my_librarian.add_book(book3)
        my_librarian.add_book(book4)
        my_librarian.add_book(book5)
        
        print("-" * 30)

        # Create sample members
        member1 = Member("M001", "Bob Johnson")
        member2 = Member("M002", "Carol White")
        member3 = Member("M003", "David Green")

        # Add members to library
        my_librarian.add_member(member1)
        my_librarian.add_member(member2)
        my_librarian.add_member(member3)
        
        print("-" * 30)
    else:
        print("\n--- Library loaded from existing data.csv ---")

    # Display current library state
    print("\n--- Current Books ---")
    for book in my_librarian.books:
        print(book)
    print("-" * 30)

    print("\n--- Current Members ---")
    for member in my_librarian.members:
        print(member)
    print("-" * 30)

    # Main menu loop
    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Display Books")
        print("6. Display Members")
        print("7. Display Current Borrowed Books")
        print("8. Display Current Library State")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":  # Add Book
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            book = Book(title, author, isbn)
            my_librarian.add_book(book)
            
        elif choice == "2":  # Add Member
            member_id = input("Enter member ID: ")
            name = input("Enter member name: ")
            member = Member(member_id, name)
            my_librarian.add_member(member)
            
        elif choice == "3":  # Borrow Book
            member_id = input("Enter member ID: ")
            isbn = input("Enter book ISBN: ")
            my_librarian.borrow_book(member_id, isbn)
            
        elif choice == "4":  # Return Book
            member_id = input("Enter member ID: ")
            isbn = input("Enter book ISBN: ")
            my_librarian.return_book(member_id, isbn)
            
        elif choice == "5":  # Display Books
            for book in my_librarian.books:
                print(book)
                
        elif choice == "6":  # Display Members
            for member in my_librarian.members:
                print(member)
                
        elif choice == "7":  # Display Current Borrowed Books
            for member in my_librarian.members:
                if member.borrowed_books:
                    print(f"Member {member.name} (ID: {member.member_id}) has borrowed the following books:")
                    for book in member.borrowed_books:
                        print(f"- {book.title} (ISBN: {book.isbn})")
                else:
                    print(f"Member {member.name} (ID: {member.member_id}) has not borrowed any books.")
                    
        elif choice == "8":  # Display Current Library State
            print("\n--- Current Library State ---")
            print("Books:")
            for book in my_librarian.books:
                print(book)
            print("\nMembers:")
            for member in my_librarian.members:
                print(member)
                
        elif choice == "9":  # Exit
            print("Exiting the Library Management System. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")
