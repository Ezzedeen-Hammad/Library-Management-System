# Library Management System

from tkinter import *
from tkinter import messagebox
import os


# Check if the file exists
if not os.path.exists("booksInfo.txt"):
    # If the file does not exist, create the file and write some initial data to it
    with open("booksInfo.txt", "w") as f:
        f.write()

elif not os.path.exists("borrowedInfo.txt"):
    # If the file does not exist, create the file and write some initial data to it
    with open("borrowedInfo.txt", "w") as f:
        f.write()


# Create the main window
root = Tk()
root.title("Library Management System")


# function to check if a serial number is valid (5 digits)
def is_valid_serial(serial):
    if len(serial) != 5:
        return False
    if not serial.isdigit():
        return False
    return True

# function to check if a user has borrowed more than 3 books


def has_borrowed_too_many(user_id):
    borrowed = 0
    with open("borrowedInfo.txt", "r") as f:
        for line in f:
            serial, user = line.strip().split("|")
            if user == user_id:
                borrowed += 1
    return borrowed >= 3

# function to check if a user has already borrowed a copy of a specific book


def has_already_borrowed(user_id, book_serial):
    with open("borrowedInfo.txt", "r") as f:
        for line in f:
            serial, user = line.strip().split("|")
            if user == user_id and serial == book_serial:
                return False
    return True


# function to check if a book has available copies in the library
def has_available_copies(book_serial):
    with open("booksInfo.txt", "r") as f:
        for line in f:
            serial, title, authors, price, available, borrowed = line.strip().split("|")
            if serial == book_serial and int(available) > 0:
                return True
    return False


# Read the contents of the "booksInfo.txt" file into a list of dictionaries


def readBooksInfo():
    books = []
    with open("booksInfo.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            serial, title, authors, price, available, borrowed = line.strip().split("|")
            book = {
                "serial": serial,
                "title": title,
                "authors": authors,
                "price": price,
                "available": available,
                "borrowed": borrowed
            }
            books.append(book)
    return books

# Write the contents of the list of dictionaries to the "booksInfo.txt" file


def writeBooksInfo(books):
    # Open the "booksInfo.txt" file in write mode
    with open("booksInfo.txt", "w") as f:
        # Write each book in the list to the file
        for book in books:
            f.write(
                f"{book['serial']}|{book['title']}|{(book['authors'])}|{book['price']}|{book['available']}|{book['borrowed']}\n")


# Read the contents of the "borrowedInfo.txt" file into a list of dictionaries


def readBorrowedInfo():
    borrowed = []
    with open("borrowedInfo.txt", "r") as file:
        for line in file:
            serial, user = line.strip().split("|")
            info = {
                "serial": serial,
                "user": user,
            }
            borrowed.append(info)
    return borrowed

# Write the contents of the list of dictionaries to the "borrowedInfo.txt" file


def writeBorrowedInfo(borrowed):
    with open("borrowedInfo.txt", "w") as file:
        for info in borrowed:
            file.write(
                ([info["serial"], info["user"]]) + "\n")


# Define the function that will be called when the button is clicked
def displayBooks():
    # Read the list of books from the "booksInfo.txt" file
    books = readBooksInfo()
    # Create an empty string to store the information for all books
    book_info = ""
    # Iterate over the list of books and build the string
    for book in books:
        book_info += f"Serial number: {book['serial']}\nTitle: {book['title']}\nAuthors: {book['authors']}\nPrice: {book['price']}\nTotal copies: {book['available'] + book['borrowed']}\n\n"
    # Display the book information in a message box
    messagebox.showinfo("Books", book_info)


# Create the button
button = Button(root, text="Display Books", command=displayBooks)
button.pack()


resultLabel = Label(root, text="")
resultLabel.pack()


# Define the search function
def searchBook():
    # Read the list of books from the "booksInfo.txt" file
    books = readBooksInfo()
    # Get the search term and search type from the entries
    term = searchEntry.get()
    search_type = searchType.get()
    # Initialize a list to store the matching books
    matches = []
    # Iterate through the books
    for book in books:
        # Check if the search term matches the title
        if (search_type == "title" and term.lower() in book["title"].lower()):
            # If the search term matches, add the book to the list of matches
            matches.append(book)
            # Check if the search term matches the author
        elif (search_type == "author" and term.lower() in book["authors"].lower()):
            # If the search term matches, add the book to the list of matches
            matches.append(book)
    # Initialize a string to store the book information
    book_info = ""
    # Iterate through the matching books
    for book in matches:
        # Add the book's information to the string
        book_info += f"Serial number: {book['serial']}\nTitle: {book['title']}\nAuthors: {book['authors']}\nPrice: {book['price']}\nTotal copies: {book['available'] + book['borrowed']}\n\n"
    # If the book_info string is not empty, display it in a message box
    if book_info:
        messagebox.showinfo("Books", book_info)
    # If the book_info string is empty, display an error message
    else:
        messagebox.showerror("Error", "No matching books found.")


# Create the search entry and the option buttons
searchEntry = Entry(root)
searchType = StringVar()
titleButton = Radiobutton(
    root, text="Title", variable=searchType, value="title")
authorButton = Radiobutton(
    root, text="Author", variable=searchType, value="author")

# Create the search button
searchButton = Button(root, text="Search", command=searchBook)

# Pack the search entry, option buttons, and search button
searchEntry.pack()
titleButton.pack()
authorButton.pack()
searchButton.pack()


# Create the result label
resultLabel = Label(root, text="")
resultLabel.pack()


# Add a new book to the library
def addBook():
    # Get the serial number, title, authors, price, and number of available copies from the user
    serial = serialEntry.get()
    title = titleEntry.get()
    authors = authorsEntry.get()
    price = priceEntry.get()
    available = availableEntry.get()
    # Validate the input
    if len(serial) != 5:
        messagebox.showerror(
            "Error", "Invalid serial number. The serial number must be 5 digits.")
        return
    if not title:
        messagebox.showerror(
            "Error", "Invalid title. The title cannot be empty.")
        return
    if not authors:
        messagebox.showerror(
            "Error", "Invalid authors. At least one author must be entered.")
        return
    try:
        price = float(price)
        if price <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid price. The price must be a positive number.")
        return
    try:
        available = int(available)
        if available < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid number of available copies. The number of available copies must be a positive integer.")
        return
    # Read the list of books
    books = readBooksInfo()
    # Check if the serial number is already used
    for book in books:
        if book["serial"] == serial:
            messagebox.showerror(
                "Error", "Invalid serial number. The serial number is already used.")
            return
    # Add the new book to the list of books
    books.append({
        "serial": serial,
        "title": title,
        "authors": authors,
        "price": price,
        "available": available,
        "borrowed": 0
    })
    # Write the updated list of books to the "booksInfo.txt" file
    writeBooksInfo(books)
    # Display a message indicating that the new book has been added successfully
    messagebox.showinfo("Success", "The new book has been added successfully.")


# Create the add frame
addFrame = Frame(root)
serialLabel = Label(addFrame, text="Serial Number:")
serialEntry = Entry(addFrame)
titleLabel = Label(addFrame, text="Title:")
titleEntry = Entry(addFrame)
authorsLabel = Label(
    addFrame, text="Authors(add comma between authors):")
authorsEntry = Entry(addFrame)
priceLabel = Label(addFrame, text="Price:")
priceEntry = Entry(addFrame)
availableLabel = Label(addFrame, text="Available Copies:")
availableEntry = Entry(addFrame)
addButton = Button(addFrame, text="Add", command=addBook)
serialLabel.pack(side="left")
serialEntry.pack(side="left")
titleLabel.pack(side="left")
titleEntry.pack(side="left")
authorsLabel.pack(side="left")
authorsEntry.pack(side="left")
priceLabel.pack(side="left")
priceEntry.pack(side="left")
availableLabel.pack(side="left")
availableEntry.pack(side="left")
addButton.pack(side="left")
addFrame.pack()

# function to remove a book


def removeBook():
    serial = removeEntry.get()
    if len(serial) != 5:
        messagebox.showerror(
            "Erorr", "Invalid serial number. Serial number should be 5 digits.")
        return
    with open("booksInfo.txt", "r") as f:
        lines = f.readlines()
    found = False
    for line in lines:
        existing_serial, title, authors, price, available, borrowed = line.strip().split("|")
        if existing_serial == serial:
            found = True
            if int(borrowed) > 0:
                messagebox.showerror("Erorr",
                                     "Cannot remove book. There are borrowed copies of this book.")
                return
            lines.remove(line)
            break
    if not found:
        messagebox.showerror(
            "Erorr", "Book with this serial number does not exist.")
        return
    with open("booksInfo.txt", "w") as f:
        f.writelines(lines)
    messagebox.showinfo("Success", "Book removed successfully.")


# Create the remove frame
removeFrame = Frame(root)
removeLabel = Label(removeFrame, text="Enter serial number:")
removeEntry = Entry(removeFrame)
removeButton = Button(removeFrame, text="Remove", command=removeBook)
removeLabel.pack(side="left")
removeEntry.pack(side="left")
removeButton.pack(side="left")
removeFrame.pack()


# function to borrow a book

def borrowBook():
    serial = borrowEntry.get()
    if len(serial) != 5:
        messagebox.showerror(
            "Erorr", "Invalid serial number. Serial number should be 5 digits.")
        return
    user_id = userEntry.get()
    if has_borrowed_too_many(user_id):
        messagebox.showerror(
            "Erorr", "Cannot borrow book. User has already borrowed 3 books.")
        return
    if has_already_borrowed(serial, user_id):
        messagebox.showerror(
            "Erorr", "Cannot borrow book. User has already borrowed a copy of this book.")
        return
    if not has_available_copies(serial):
        messagebox.showerror(
            "Erorr", "Cannot borrow book. There are no available copies in the library.")
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
        f.write(f"{serial}|{user_id}\n")
    messagebox.showinfo("Success", "Book borrowed successfully.")


# Create the borrow frame
borrowFrame = Frame(root)
borrowLabel = Label(borrowFrame, text="Enter serial number:")
borrowEntry = Entry(borrowFrame)
userLabel = Label(borrowFrame, text="Enter user ID:")
userEntry = Entry(borrowFrame)
borrowButton = Button(borrowFrame, text="Borrow", command=borrowBook)
borrowLabel.pack(side="left")
borrowEntry.pack(side="left")
userLabel.pack(side="left")
userEntry.pack(side="left")
borrowButton.pack(side="left")
borrowFrame.pack()


# Return a borrowed book

def returnBook():
    serial = returnEntry.get()
    if not is_valid_serial(serial):
        messagebox.showerror(
            "Erorr", "Invalid serial number. Serial number should be 5 digits.")
        return
    user_id = returnUserEntry.get()
    found = False
    with open("borrowedInfo.txt", "r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        existing_serial, existing_user = lines[i].strip().split("|")
        if existing_user == user_id and existing_serial == serial:
            found = True
            lines.remove(lines[i])
            break
    if not found:
        messagebox.showerror(
            "Erorr", "No matching record found. User has not borrowed this book or entered an invalid serial number.")
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
    messagebox.showinfo("Sucsess", "Book returned successfully.")


# Create the return frame
returnFrame = Frame(root)
returnLabel = Label(returnFrame, text="Enter serial number:")
returnEntry = Entry(returnFrame)
returnUserLabel = Label(returnFrame, text="Enter user ID:")
returnUserEntry = Entry(returnFrame)
returnButton = Button(returnFrame, text="Return", command=returnBook)
returnLabel.pack(side="left")
returnEntry.pack(side="left")
returnUserLabel.pack(side="left")
returnUserEntry.pack(side="left")
returnButton.pack(side="left")
returnFrame.pack()

# Create the exit frame
exitFrame = Frame(root)
exitButton = Button(exitFrame, text="exit", command=root.quit)
exitButton.pack(side="bottom")
exitFrame.pack()


# create function to clear all the Entries

def clear():
    searchEntry.delete(0, END)
    serialEntry.delete(0, END)
    titleEntry.delete(0, END)
    authorsEntry.delete(0, END)
    priceEntry.delete(0, END)
    availableEntry.delete(0, END)
    removeEntry.delete(0, END)
    borrowEntry.delete(0, END)
    userEntry.delete(0, END)
    returnEntry.delete(0, END)
    returnUserEntry.delete(0, END)


# create a clear frame
clearFrame = Frame(root)
clearButton = Button(root, text='clear', command=clear)
clearButton.pack(side="top")
clearFrame.pack()

# Run the main loop
root.mainloop()
