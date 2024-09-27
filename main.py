import cmd
import datetime
import os
import json
import shlex


# Task Tracker


class TaskTracker(cmd.Cmd):
    prompt = "TaskTracker> "
    intro = "Welcome to TaskTracker! Type help to list commands."

    def __init__(self):
        super().__init__()
        self.current_directory = os.getcwd()

    def do_hello(self, line):
        print("Hello World!")

    # First add it in progress # if no json file exist, create it
    def do_add(self, arg):

        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"taskcounter": 0, "tasks": []}

        current_id = data["taskcounter"]+1

        task = shlex.split(arg)

        new_task = {
            "id": current_id,
            "description": task[0],
            "status": "todo",
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now()
        }

        data["tasks"].append(new_task)

        data["taskcounter"] += 1

        with open("tasks.json", "w") as outfile:
            json.dump(data, outfile, indent=4, default=str)

        print(f"Task added successfully: {new_task['id']}")

    # Mark here a task as in progress or done
    def do_update(self, arg):
        args = shlex.split(arg)
        print(args)
        if len(args) != 2:
            print("Not enough arguments given")
            return
        id, new_task = args

        print(f"Update task {id}: {new_task}")
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File does not exist")
            return

        task_found = False
        for task in data["tasks"]:
            print(f'{task["id"]} and {id}')
            if int(task["id"]) == int(id):
                task["description"] = new_task
                task_found = True
                task["updatedAt"] = datetime.datetime.now()
                break

        if task_found:
            print(f"Task updated successfully: {id}")
        else:
            print(f"Task {id} does not exist")


        with open("tasks.json", "w") as outfile:
            json.dump(data, outfile, indent=4, default=str)

    def do_delete(self, id):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File does not exist")
            return

        task_found = False
        for task in data["tasks"]:
            print(f'{task["id"]} and {id}')
            if int(task["id"]) == int(id):
                task_found = True
                data["tasks"].remove(task)
                break

        if task_found:
            print(f"Task deleted successfully: {id}")
        else:
            print(f"Task {id} does not exist")

        with open("tasks.json", "w") as outfile:
            json.dump(data, outfile, indent=4)

    def do_mark_in_progress(self, id):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File does not exist")
            return

        task_found = False
        for task in data["tasks"]:
            if int(task["id"]) == int(id):
                task_found = True
                task["status"] = "in-progress"
                break

        if task_found:
            print(f'Task updated successfully: {id} - {task["status"]}')
        else:
            print(f'Task {id} does not exist')

        with open("tasks.json", "w") as outfile:
            json.dump(data, outfile, indent=4)


    def do_mark_completed(self, id):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File does not exist")
            return

        task_found = False
        for task in data["tasks"]:
            if int(task["id"]) == int(id):
                task_found = True
                task["status"] = "completed"
                break

        if task_found:
            print(f'Task updated successfully: {id} - {task["status"]}')
        else:
            print(f'Task {id} does not exist')

        with open("tasks.json", "w") as outfile:
            json.dump(data, outfile, indent=4)


    # Display all task that are either: done, not done, in progress, all
    def do_list(self, status):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File does not exist")
            return


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
            # print all
            for task in data["tasks"]:
                print(f'{task["id"]}: {task["description"]} - {task["status"]}')

        else:
            print(f"Status: {status} is invalid")
    def do_quit(self, arg):
        return True

    def do_help(self, arg):
        print("""
        add 'task' - Adds a new task. 
        update [taskId] [newDescription] - Updates a task.
        delete [taskId] - Deletes a task.
        list [status](optional) - List all tasks or all task with the given status.
        quit - Quit the program.
        help - Print this help.
        """)


class Task():
    def __init__(self, id, description, status, createdAt, updatedAt):
        self.id = id
        self.description = description
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt


if __name__ == '__main__':
    TaskTracker().cmdloop()
