import cmd      # Importing the cmd module for creating a command-line interface
import datetime # Importing datetime for handling task creating and update timestamps
import os       # Importing os for interacting with the operating system, such as file paths
import json     # Importing json to handle JSON data manipulation for storing tasks
import shlex    # Importing shlex for safely parsing command arguments


# Task Tracker

# TaskTracker class inherits from cmd.Cmd to provide an interactive command-line interface
class TaskTracker(cmd.Cmd):
    # Setting the command prompt and intro message for the user
    prompt = "TaskTracker> "
    intro = "Welcome to TaskTracker! Type help to list commands."

    def __init__(self):
        super().__init__()
        self.current_directory = os.getcwd() # Store the current working directory


    # Method to add a new task; creates a tasks.json file if it doesn't exist
    def do_add(self, arg):
        # Try to open tasks.json, create a new task list if it doesn't exist
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"taskcounter": 0, "tasks": []} # Initialize task data if no file exists

        current_id = data["taskcounter"]+1 # increment task ID for new tasks

        task = shlex.split(arg) # Split task description from arguments safely

        # Create a new task with detaisl including creation and update timestamps
        new_task = {
            "id": current_id,
            "description": task[0],
            "status": "todo",       # Set default status to 'todo'
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now()
        }

        data["tasks"].append(new_task)  # Append the new task to the list

        data["taskcounter"] += 1 # Increment task counter

        self.write_data(data) # Write update data back to tasks.json

        print(f"Task added successfully: {new_task['id']}") # Confirm task addition


    # Method to update an existing task's description
    def do_update(self, arg):
        args = shlex.split(arg) # Split arguments into a list
        print(args)
        if len(args) != 2: # Check for sufficient arguments
            print("Not enough arguments given")
            return
        id, new_task = args # Extract task ID and new description from arguments

        data = self.read_data() # Read the current task data
        task_found = False # Flag to check if task is found

        # Iterate through tasks to find the matching task by ID
        for task in data["tasks"]:
            if int(task["id"]) == int(id):
                task["description"] = new_task # Update task description
                task_found = True
                task["updatedAt"] = datetime.datetime.now() # Update timestamp
                break

        if task_found:
            print(f"Task updated successfully: {id}") # Confirm task update
        else:
            print(f"Task {id} does not exist") # Print error if task is not found

        self.write_data(data) # Write updated data back to tasks.json

    # Method to delete a task by its ID
    def do_delete(self, id):
        data = self.read_data() # Read current task data
        task_found = False # Flag to check if task is found

        # Iterate through tasks to find the one to delete
        for task in data["tasks"]:
            if int(task["id"]) == int(id):
                task_found = True
                data["tasks"].remove(task) # Remove the task from the list
                break

        data["taskcounter"] -= 1 # Decrement the task counter if task is deleted
        if task_found:
            print(f"Task deleted successfully: {id}") # Confirm task deletion
        else:
            print(f"Task {id} does not exist") # Print error if task is not found

        self.write_data(data) # Write updated data back to tasks.json

    def do_mark_in_progress(self, id):
        self.mark(id, "in-progress") # Use mark method to update the status


    def do_mark_done(self, id):
        self.mark(id, "done") # Use mark method to update the status

    # Helper method to update the status of a task
    def mark(self, id, status):
        if not status:
            status = "Unknown" # Default to unknown status if not provided

        data = self.read_data() # Read current task data
        task_found = False # Flag to check if task is found

        # Iterate through tasks to find the matching task by ID
        for task in data["tasks"]:
            if int(task["id"]) == int(id):
                task_found = True
                task["status"] = status # Update the task status
                break

        if task_found:
            print(f'Task updated successfully: {id} - {task["status"]}') # Confirm update
        else:
            print(f'Task {id} does not exist') # Print error if task is not found

        self.write_data(data) # Write updated data back to tasks.json



    # Method to list tasks based on their status
    def do_list(self, status):
        data = self.read_data() # Read current task data

        # Print tasks based on their status
        if status == "done":
            print(f"Status: done")
            for task in data["tasks"]:
                if task["status"] == "done":
                    print(f'{task["id"]}: {task["description"]}')

        elif status == "todo":
            print(f"Status: todo")
            for task in data["tasks"]:
                if task["status"] == "todo":
                    print(f'{task["id"]}: {task["description"]}')

        elif status == "in-progress":
            print(f"Status: in-progress")
            for task in data["tasks"]:
                if task["status"] == "in-progress":
                    print(f'{task["id"]}: {task["description"]}')
        elif status == "" or status == "all":
            # Print all tasks regardless of status
            for task in data["tasks"]:
                print(f'{task["id"]}: {task["description"]} - {task["status"]}')

        else:
            print(f"Status: {status} is invalid") # Print error for invalid status

    # Exit commands to quit the application
    def do_quit(self, arg):
        return True # Return True to exit the command loop

    def do_exit(self, arg):
        return True # Return True to exit the command loop

    # Help method to display available commands
    def do_help(self, arg):
        print("""
        add 'task' - Adds a new task. 
        update [taskId] [newDescription] - Updates a task.
        delete [taskId] - Deletes a task.
        list [status](optional) - List all tasks or all task with the given status.
        mark_done - Marks a task as done.
        mark_in_progress - Marks a task as in-progress.
        quit - Quit the program.
        exit - exits the program.
        help - Print this help.
        """)

    # Post-command method to refresh task IDs and update data after every command
    def postcmd(self, stop, line):
        # After command execution
        self.refresh_json_numbers() # Ensure task IDs are consistent
        return stop  # Control whether to continue or stop the command loop

    # Helper method to refresh task IDs and update task counter
    def refresh_json_numbers(self):
        data = self.read_data() # Read current task data
        # Re-assign task IDs sequentially starting from 1
        for index, task in enumerate(data["tasks"], start=1):
            task["id"] = index
        data["taskcounter"] = len(data["tasks"]) # Update task counter

        self.write_data(data) # Write updated data back to tasks.json

    # Helper method to write data to tasks.json
    def write_data(self, data):
        # write
        with open("tasks.json", "w") as outfile:
            json.dump(data, outfile, indent=4, default=str) # Write JSON data to file

    # Helper method to read data from tasks.json
    def read_data(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f) # Load task data from file
        except FileNotFoundError:
            print("File does not exist") # Error message if file is not found
            return None
        return data # Return task data

# Main entry point of the program
if __name__ == '__main__':
    TaskTracker().cmdloop() # Start the command loop for user interaction
