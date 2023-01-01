# Library Management System


# function to check if a serial number is valid (5 digits)


def is_valid_serial(serial):
    if len(serial) != 5:
        return False
    if not serial.isdigit():
        return False
    return True

# function to check if a price is valid (float positive number)


def is_valid_price(price):
    try:
        price = float(price)
        if price <= 0:
            return False
        return True
    except:
        return False

# function to check if a number of copies is valid (positive integer)


def is_valid_copies(copies):
    try:
        copies = int(copies)
        if copies <= 0:
            return False
        return True
    except:
        return False

# function to check if a user has borrowed more than 3 books


def has_borrowed_too_many(user_id):
    borrowed = 0
    with open("borrowedInfo.txt", "r") as f:
        for line in f:
            user, book, serial = line.strip().split("|")
            if user == user_id:
                borrowed += 1
    return borrowed >= 3

# function to check if a user has already borrowed a copy of a specific book


def has_already_borrowed(user_id, book_serial):
    with open("borrowedInfo.txt", "r") as f:
        for line in f:
            user, book, serial = line.strip().split("|")
            if user == user_id and serial == book_serial:
                return True
    return False

# function to check if a book has available copies in the library


def has_available_copies(book_serial):
    with open("booksInfo.txt", "r") as f:
        for line in f:
            serial, title, authors, price, available, borrowed = line.strip().split("|")
            if serial == book_serial and int(available) > 0:
                return True
    return False

# function to display all books in the library


def display_all_books():
    with open("booksInfo.txt", "r") as f:
        for line in f:
            serial, title, authors, price, available, borrowed = line.strip().split("|")
            print("="*31)
            print(f"Serial Number: {serial}")
            print(f"Title: {title}")
            print(f"Number of Authors: {len(authors.split('&'))}")
            print(f"Price: {price}")
            print(f"Total Number of available Copies : {int(available)}")
            print(f"Total Number of borrowed Copies : {int(borrowed)}")
            print("="*31)


# function to search for books by title or authors


def search_book():
    # Read the contents of the booksInfo.txt file and search for a book based on the title or author name provided by the user
    search_term = input(
        'Enter (t) to search by title or (a) to search by author name: ')
    with open('booksInfo.txt', 'r') as f:
        for line in f:
            serial_number, title, authors, price, available_copies, borrow_books = line.strip().split('|')
            if search_term.lower() == 't':
                search_by_title = input('Enter the title: ')
                if search_by_title.lower() in title.lower():
                    print("="*31)
                    print(f'Serial number: {serial_number}')
                    print(f'Title: {title}')
                    print(f'Authors: {authors}')
                    print(f'Price: {price}')
                    print(f'Copies: {available_copies}')
                    print(f'Copies: {borrow_books}')
                    print("="*31)
            elif search_term.lower() == 'a':
                search_by_author = input('Enter author name: ')
                if search_by_author.lower() in authors.lower():
                    print("="*31)
                    print(f'Serial number: {serial_number}')
                    print(f'Title: {title}')
                    print(f'Authors: {authors}')
                    print(f'Price: {price}')
                    print(f'Copies: {available_copies}')
                    print(f'Copies: {borrow_books}')
                    print("="*31)
            else:
                print('No matched record found')


# function to add a new book


def add_book():
    serial = input("Enter book serial number: ")
    if not is_valid_serial(serial):
        print("Invalid serial number. Serial number should be 5 digits.")
        return
    with open("booksInfo.txt", "r") as f:
        for line in f:
            existing_serial, title, authors, price, available, borrowed = line.strip().split("|")
            if existing_serial == serial:
                print("Book with this serial number already exists.")
                return
    title = input("Enter book title: ")
    authors = input("Enter book authors (separated by '&'): ")
    price = input("Enter book price: ")
    if not is_valid_price(price):
        print("Invalid price. Price should be a positive number.")
        return
    copies = input("Enter number of copies: ")
    if not is_valid_copies(copies):
        print("Invalid number of copies. Number of copies should be a positive integer.")
        return
    with open("booksInfo.txt", "a") as f:
        f.write(f"{serial}|{title}|{authors}|{price}|{copies}|0\n")
    print("Book added successfully.")


# function to remove a book


def remove_book():
    serial = input("Enter book serial number: ")
    if not is_valid_serial(serial):
        print("Invalid serial number. Serial number should be 5 digits.")
        return
    with open("booksInfo.txt", "r") as f:
        lines = f.readlines()
    found = False
    for line in lines:
        existing_serial, title, authors, price, available, borrowed = line.strip().split("|")
        if existing_serial == serial:
            found = True
            if int(borrowed) > 0:
                print("Cannot remove book. There are borrowed copies of this book.")
                return
            print(f"Serial Number: {existing_serial}")
            print(f"Title: {title}")
            print(f"Number of Authors: {len(authors.split('&'))}")
            print(f"Price: {price}")
            print(
                f"Total Number of Copies (available in library + borrowed): {int(available) + int(borrowed)}")
            confirm = input(
                "Are you sure you want to remove this book? (y/n) ")
            if confirm.lower() != "y":
                return
            lines.remove(line)
            break
    if not found:
        print("Book with this serial number does not exist.")
        return
    with open("booksInfo.txt", "w") as f:
        f.writelines(lines)
    print("Book removed successfully.")

# function to borrow a book


# function to borrow a book
def borrow_book():
    serial = input("Enter book serial number: ")
    if not is_valid_serial(serial):
        print("Invalid serial number. Serial number should be 5 digits.")
        return
    user_id = input("Enter user id: ")
    if has_borrowed_too_many(user_id):
        print("Cannot borrow book. User has already borrowed 3 books.")
        return
    if has_already_borrowed(user_id, serial):
        print("Cannot borrow book. User has already borrowed a copy of this book.")
        return
    if not has_available_copies(serial):
        print("Cannot borrow book. There are no available copies in the library.")
        return
    with open("booksInfo.txt", "r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        existing_serial, title, authors, price, available, borrowed = lines[i].strip(
        ).split("|")
        if existing_serial == serial:
            available = str(int(available) - 1)
            borrowed = str(int(borrowed) + 1)
            lines[i] = f"{serial}|{title}|{authors}|{price}|{available}|{borrowed}\n"
            break
    with open("booksInfo.txt", "w") as f:
        f.writelines(lines)
    with open("borrowedInfo.txt", "a") as f:
        f.write(f"{user_id}|{title}|{serial}\n")
    print("Book borrowed successfully.")

# function to return a book


def return_book():
    serial = input("Enter book serial number: ")
    if not is_valid_serial(serial):
        print("Invalid serial number. Serial number should be 5 digits.")
        return
    user_id = input("Enter user id: ")
    found = False
    with open("borrowedInfo.txt", "r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        existing_user, title, existing_serial = lines[i].strip().split("|")
        if existing_user == user_id and existing_serial == serial:
            found = True
            lines.remove(lines[i])
            break
    if not found:
        print("No matching record found. User has not borrowed this book or entered an invalid serial number.")
        return
    with open("borrowedInfo.txt", "w") as f:
        f.writelines(lines)
    with open("booksInfo.txt", "r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        existing_serial, title, authors, price, available, borrowed = lines[i].strip(
        ).split("|")
        if existing_serial == serial:
            available = str(int(available) + 1)
            borrowed = str(int(borrowed) - 1)
            lines[i] = f"{serial}|{title}|{authors}|{price}|{available}|{borrowed}\n"
            break
    with open("booksInfo.txt", "w") as f:
        f.writelines(lines)
    print("Book returned successfully.")


# main function to run the library management system

while True:
    print("Library Management System")
    print("1. Display all books")
    print("2. Search for books")
    print("3. Add a new book")
    print("4. Remove a book")
    print("5. Borrow a book")
    print("6. Return a book")
    print("7. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        display_all_books()
    elif choice == "2":
        search_book()
    elif choice == "3":
        add_book()
    elif choice == "4":
        remove_book()
    elif choice == "5":
        borrow_book()
    elif choice == "6":
        return_book()
    elif choice == "7":
        break
    else:
        print("Invalid choice.")


# run the library management system
