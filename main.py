import json
import os

print("Welcome to Task & Library Manager!")

class Book:
    def __init__(self, title, author, year, status="Unread"):
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def mark_read(self):
        self.status = "Read"

    def mark_unread(self):
        self.status = "Unread"

    def to_dict(self):
        return {"title": self.title, "author": self.author, "year": self.year, "status": self.status}

    @staticmethod
    def from_dict(d):
        return Book(d["title"], d["author"], d["year"], d.get("status", "Unread"))

    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year}) - {self.status}"  


class Task:
    def __init__(self, title, description="", priority="Medium", due_date=None, done=False):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.done = done

    def mark_done(self):
        self.done = True

    def mark_undone(self):
        self.done = False

    def to_dict(self):
        return {"title": self.title, "description": self.description, "priority": self.priority,
                "due_date": self.due_date, "done": self.done}

    @staticmethod
    def from_dict(d):
        return Task(d["title"], d.get("description", ""), d.get("priority", "Medium"), d.get("due_date", None), d.get("done", False))

    def __str__(self):
        status = "Done" if self.done else "Not Done"
        return f"{self.title} [Priority: {self.priority}] - {status}"


LIBRARY_FILE = "library.json"
TASKS_FILE = "tasks.json"

library = []  
tasks = []    


def save_library():
    data = [b.to_dict() for b in library]
    try:
        with open(LIBRARY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Error saving library:", e)
    else:
        pass


def load_library():
    if not os.path.exists(LIBRARY_FILE):
        return
    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            library.append(Book.from_dict(item))
    except Exception as e:
        print("Error loading library:", e)


def save_tasks():
    data = [t.to_dict() for t in tasks]
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Error saving tasks:", e)
    else:
        pass


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            tasks.append(Task.from_dict(item))
    except Exception as e:
        print("Error loading tasks:", e)


def display_menu():
    print("\nMenu:")
    print("1. Manage Books")
    print("2. Manage Tasks")
    print("3. Statistics")
    print("4. Exit")
    return input("Choose an option (1-4): ").strip()


def book_menu():
    print("\nBook Menu:")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Update Book Status")
    print("5. Remove Book")
    print("6. Back to Main Menu")
    return input("Choose an option (1-6): ").strip()


def task_menu():
    print("\nTask Menu:")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Toggle Task Done/Undone")
    print("4. Remove Task")
    print("5. Back to Main Menu")
    return input("Choose an option (1-5): ").strip()


def add_book():
    title = input("Enter book title: ").strip()
    author = input("Enter book author: ").strip()
    year = input("Enter publication year: ").strip()
    if not title or not author or not year:
        print("Title, author and year are required.")
        return
    new_book = Book(title, author, year)
    library.append(new_book)
    save_library()
    print(f"Book {new_book} added successfully!")


def view_books():
    if not library:
        print("Library is empty!")
        return
    print("\nAll books in your library:")
    for i, book in enumerate(library, start=1):
        print(f"{i}. {book}")


def search_book():
    if not library:
        print("Library is empty!")
        return
    query = input("Enter title or author to search: ").strip().lower()
    if not query:
        print("Empty search.")
        return
    results = [b for b in library if query in b.title.lower() or query in b.author.lower()]
    if results:
        print("Search results:")
        for i, book in enumerate(results, start=1):
            print(f"{i}. {book}")
    else:
        print("No books found matching your search.")


def update_book_status():
    if not library:
        print("Library is empty!")
        return
    view_books()
    try:
        idx = int(input("Enter the number of the book to update status: ").strip()) - 1
    except ValueError:
        print("Please enter a valid number.")
        return
    if 0 <= idx < len(library):
        book = library[idx]
        choice = input("Enter new status (Read/Unread): ").strip().lower()
        if choice.startswith("r"):
            book.mark_read()
        elif choice.startswith("u"):
            book.mark_unread()
        else:
            print("Invalid status. Use Read or Unread.")
            return
        save_library()
        print(f"Updated: {book}")
    else:
        print("Invalid book number.")


def remove_book():
    if not library:
        print("Library is empty!")
        return
    view_books()
    try:
        idx = int(input("Enter the number of the book to remove: ").strip()) - 1
    except ValueError:
        print("Please enter a valid number.")
        return
    if 0 <= idx < len(library):
        removed = library.pop(idx)
        save_library()
        print(f"Removed: {removed}")
    else:
        print("Invalid book number.")


def add_task():
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title required.")
        return
    description = input("Enter description (optional): ").strip()
    priority = input("Enter priority (High/Medium/Low) [Medium]: ").strip().capitalize() or "Medium"
    due = input("Enter due date (optional): ").strip() or None
    t = Task(title, description, priority, due)
    tasks.append(t)
    save_tasks()
    print(f"Task added: {t}")


def view_tasks():
    if not tasks:
        print("No tasks.")
        return
    print("\nAll tasks:")
    for i, t in enumerate(tasks, start=1):
        print(f"{i}. {t}")


def toggle_task_done():
    if not tasks:
        print("No tasks.")
        return
    view_tasks()
    try:
        idx = int(input("Enter number of task to toggle done/undone: ").strip()) - 1
    except ValueError:
        print("Please enter a valid number.")
        return
    if 0 <= idx < len(tasks):
        t = tasks[idx]
        if t.done:
            t.mark_undone()
            print(f"Marked undone: {t.title}")
        else:
            t.mark_done()
            print(f"Marked done: {t.title}")
        save_tasks()
    else:
        print("Invalid task number.")


def remove_task():
    if not tasks:
        print("No tasks.")
        return
    view_tasks()
    try:
        idx = int(input("Enter number of task to remove: ").strip()) - 1
    except ValueError:
        print("Please enter a valid number.")
        return
    if 0 <= idx < len(tasks):
        removed = tasks.pop(idx)
        save_tasks()
        print(f"Removed task: {removed.title}")
    else:
        print("Invalid task number.")


def show_statistics():
    total_books = len(library)
    unread_books = sum(1 for b in library if b.status.lower() != "read")
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.done)
    print("\nStatistics:")
    print(f"Total books: {total_books}")
    print(f"Unread books: {unread_books}")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")


load_library()
load_tasks()


while True:
    option = display_menu()

    if option == "1":
        while True:
            book_choice = book_menu()

            if book_choice == "1":
                add_book()
            elif book_choice == "2":
                view_books()
            elif book_choice == "3":
                search_book()
            elif book_choice == "4":
                update_book_status()
            elif book_choice == "5":
                remove_book()
            elif book_choice == "6":
                break
            else:
                print("Invalid menu choice, try again.")

    elif option == "2":
        while True:
            t_choice = task_menu()
            if t_choice == "1":
                add_task()
            elif t_choice == "2":
                view_tasks()
            elif t_choice == "3":
                toggle_task_done()
            elif t_choice == "4":
                remove_task()
            elif t_choice == "5":
                break
            else:
                print("Invalid task choice, try again.")

    elif option == "3":
        show_statistics()

    elif option == "4":
        print("Saving data and exiting the program. Goodbye!")
        save_library()
        save_tasks()
        break

    else:
        print("Invalid option, please choose 1-4.")
