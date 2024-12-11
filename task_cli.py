import sys
import os
import json
import uuid
from datetime import datetime


class TaskCLI:
    def __init__(self, file_path="tasks.json"):
        self.file_path: str = file_path
        self.tasks: dict = self.load_tasks()

    def load_tasks(self) -> dict:
        """Load tasks from JSON file or create an empty list if file doesn't exist."""
        try:
            if not os.path.exists(self.file_path):
                return {}
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def save_tasks(self) -> None:
        """Save tasks to JSON file."""
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.tasks, f, indent=2)
        except IOError as e:
            print(f"Error saving tasks: {e}")
            sys.exit(1)

    def add_task(self, description) -> None:
        """Add a new task."""
        task = {
            "id": str(uuid.uuid4()),
            "description": description,
            "status": "todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
        }
        self.tasks[task["id"]] = task
        self.save_tasks()
        print(f"Task added successfully (ID: {task['id']})")

    def update_task(self, task_id, new_description) -> None:
        """Update an existing task."""
        task = self.tasks.get(task_id)
        if not task:
            print(f"Task with ID {task_id} not found")
            return
        task["description"] = new_description
        task["updatedAt"] = datetime.now().isoformat()
        self.save_tasks()
        print(f"Task {task_id} updated successfully")

    def delete_task(self, task_id) -> None:
        """Delete a task."""
        task = self.tasks.get(task_id)
        if not task:
            print(f"Task with ID {task_id} not found")
            return
        del self.tasks[task_id]
        self.save_tasks()
        print(f"Task {task_id} deleted successfully")

    def mark_task_status(self, task_id, status):
        """Mark task status as to-do, in-progress, or done."""
        valid_statuses = ["todo", "in-progress", "done"]
        if status not in valid_statuses:
            print(f"Invalid status. Must be one of {valid_statuses}")
            return

        task = self.tasks.get(task_id)
        if not task:
            print(f"Task with ID {task_id} not found")
            return
        task["status"] = status
        task["updatedAt"] = datetime.now().isoformat()
        self.save_tasks()
        print(f"Task {task_id} marked as {status}")

    def list_tasks(self, filter_status=None):
        """List tasks, optionally filtered by status."""
        filtered_tasks = self.tasks.values()
        if filter_status:
            filtered_tasks = [
                task for task in filtered_tasks if task["status"] == filter_status
            ]

        if not filtered_tasks:
            print("No tasks found.")
            return

        print(
            "{:<40} {:<15} {:<15} {:<25} {:<25}".format(
                "ID", "Description", "Status", "Created At", "Updated At"
            )
        )
        print("-" * 120)
        for task in filtered_tasks:
            print(
                "{:<40} {:<15} {:<15} {:<25} {:<25}".format(
                    task["id"],
                    (
                        task["description"][:38] + "..."
                        if len(task["description"]) > 40
                        else task["description"]
                    ),
                    task["status"],
                    task["createdAt"],
                    task["updatedAt"],
                )
            )


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        sys.exit(1)

    task_cli = TaskCLI()
    command = sys.argv[1]

    try:
        if command == "add" and len(sys.argv) > 2:
            task_cli.add_task(" ".join(sys.argv[2:]))
        elif command == "update" and len(sys.argv) > 3:
            task_cli.update_task(sys.argv[2], " ".join(sys.argv[3:]))
        elif command == "delete" and len(sys.argv) == 3:
            task_cli.delete_task(sys.argv[2])
        elif command == "mark-in-progress" and len(sys.argv) == 3:
            task_cli.mark_task_status(sys.argv[2], "in-progress")
        elif command == "mark-done" and len(sys.argv) == 3:
            task_cli.mark_task_status(sys.argv[2], "done")
        elif command == "list":
            if len(sys.argv) == 2:
                task_cli.list_tasks()
            elif len(sys.argv) == 3:
                valid_filters = ["todo", "in-progress", "done"]
                if sys.argv[2] in valid_filters:
                    task_cli.list_tasks(sys.argv[2])
                else:
                    print(f"Invalid filter. Must be one of {valid_filters}")
                    sys.exit(1)
        else:
            print(
                "Invalid command. Available commands: add, update, delete, mark-in-progress, mark-done, list"
            )
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
