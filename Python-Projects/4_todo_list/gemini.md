# Project 4: To-Do List Application

This project is a significant step up. We're going to build an application that can remember data even after the program has stopped. We'll create a to-do list manager that saves your tasks to a file.

This project introduces several fundamental concepts:

1.  **Lists:** A list is a data structure that holds an ordered collection of items. We'll use a list to keep track of all our tasks.
2.  **File I/O (Input/Output):** We'll learn how to read from and write to a text file. This is how we'll make our task list persistent (i.e., it saves).
3.  **Functions:** To keep our code organized as it gets more complex, we'll group related code into functions.
4.  **The `os` module:** We'll use this module to check if our tasks file already exists.
5.  **`enumerate()`:** A handy function for getting both the index and the item when looping over a list.

## Code

```python
import os

FILENAME = "tasks.txt"

def load_tasks():
    """Loads tasks from the file."""
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        tasks = [line.strip() for line in f.readlines()]
    return tasks

def save_tasks(tasks):
    """Saves tasks to the file."""
    with open(FILENAME, "w") as f:
        for task in tasks:
            f.write(task + "\n")

def show_tasks(tasks):
    """Displays the list of tasks."""
    print("\n--- Your To-Do List ---")
    if not tasks:
        print("You have no tasks!")
    else:
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
    print("-----------------------\n")

def add_task(tasks):
    """Adds a new task to the list."""
    task = input("Enter a new task: ")
    tasks.append(task)
    save_tasks(tasks)
    print("Task added!")

def remove_task(tasks):
    """Removes a task from the list."""
    show_tasks(tasks)
    try:
        task_num = int(input("Enter the number of the task to remove: ") )
        if 1 <= task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            save_tasks(tasks)
            print(f"Removed task: '{removed_task}'")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    """Main function to run the to-do list app."""
    tasks = load_tasks()
    while True:
        print("What would you like to do?")
        print("1. View tasks")
        print("2. Add a task")
        print("3. Remove a task")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            show_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            remove_task(tasks)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
```

## How to Run the Code

1.  Navigate to the `4_todo_list` directory.
2.  Run the script: `python3 main.py`
