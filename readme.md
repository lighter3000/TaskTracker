# Task Tracker

Track your tasks easily with TaskTracker! This command-line tool lets you add, update, delete, and list tasks, helping you stay organized.


## Description

TaskTracker is a simple task management system written in Python. It is part of the roadmap.sh project and provides a way to track tasks with a variety of statuses (`todo`, `in-progress`, `done`) using a JSON file for persistence.

## Getting Started

### Dependencies

Before running the program, ensure you have the following installed:
* Python 3.x
* Any OS that supports Python (Windows, macOS, Linux)
* Libraries
  * json (part of Python's standard library)

### Installing

1. Clone the repository
```
git clone <repository-url>
```

2. The `tasks.json` file will be created automatically after you `add` something after executing the program

### Executing program

Run the program using Python
```bash
python main.py
```

Once the program starts, you will see a prompt:

```bash
TaskTracker>
```

You can now begin to interact with the toll by typing commands

## Available Commands

Here is a list of commands you can use in TaskTracker:

* `add 'task'`: Adds a new task.
* `update [taskId] [newDescription]`: Updates the description of a task by its ID. 
* ``delete [taskId]``: Deletes a task by its ID. 
* ``list [status]``: Lists all tasks or tasks filtered by their status (`todo`, `in-progress`, `done`, or `all` (or nothing)). 
* ``mark_in_progress [taskId]``: Marks a task as in-progress. 
* ``mark_done [taskId]``: Marks a task as done. 
* ``help``: Shows the list of available commands. 
* ``quit or exit``: Exits the TaskTracker program.


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project

This project is from [roadmap.sh](https://roadmap.sh/projects/task-tracker)