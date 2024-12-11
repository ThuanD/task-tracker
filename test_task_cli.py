import unittest
import os
import tempfile
import sys
import uuid
from unittest.mock import patch

# Import the TaskCLI class from the main script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from task_cli import TaskCLI


class TestTaskCLI(unittest.TestCase):
    def setUp(self):
        """Set up a temporary test environment."""
        # Create temporary files to store tasks
        self.temp_file = tempfile.mktemp()  # NOQA NOSONAR
        self.task_cli = TaskCLI(self.temp_file)

    def tearDown(self):
        """Clean up temporary files after testing."""
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def last_task_id(self):
        return list(self.task_cli.tasks.keys())[-1]

    def test_add_task(self):
        """Test the add task functionality."""
        initial_tasks_count = len(self.task_cli.tasks)

        # Add a task
        self.task_cli.add_task("Test task")

        # Check the number of tasks increased
        self.assertEqual(len(self.task_cli.tasks), initial_tasks_count + 1)

        # Check the properties of the new task
        new_task_id = self.last_task_id()
        new_task = self.task_cli.tasks[new_task_id]
        self.assertEqual(new_task["description"], "Test task")
        self.assertEqual(new_task["status"], "todo")
        self.assertIsNotNone(new_task["id"])
        self.assertIsNotNone(new_task["createdAt"])
        self.assertIsNotNone(new_task["updatedAt"])

    def test_update_task(self):
        """Check the task update function."""
        # Add a task
        self.task_cli.add_task("Original task")
        task_id = self.last_task_id()

        # Update task
        self.task_cli.update_task(task_id, "Updated task")

        # Check the updated task
        updated_task = self.task_cli.tasks[task_id]
        self.assertEqual(updated_task["description"], "Updated task")
        self.assertNotEqual(updated_task["createdAt"], updated_task["updatedAt"])

    def test_delete_task(self):
        """Test the delete task function."""
        # Add a task
        self.task_cli.add_task("Task to delete")
        initial_tasks_count = len(self.task_cli.tasks)
        task_id = self.last_task_id()

        # Delete task
        self.task_cli.delete_task(task_id)

        # Check deleted tasks
        self.assertEqual(len(self.task_cli.tasks), initial_tasks_count - 1)
        self.assertEqual(self.task_cli.tasks.get(task_id), None)

    def test_mark_task_status(self):
        """Test task status change functionality."""
        # Add a task
        self.task_cli.add_task("Status change task")
        task_id = self.last_task_id()

        # Check for in-progress status
        self.task_cli.mark_task_status(task_id, "in-progress")
        task = self.task_cli.tasks[task_id]
        self.assertEqual(task["status"], "in-progress")

        # Check the status is done
        self.task_cli.mark_task_status(task_id, "done")
        task = self.task_cli.tasks[task_id]
        self.assertEqual(task["status"], "done")

    def test_list_tasks_by_status(self):
        """Test the task listing function by status."""
        # Add tasks with different statuses
        self.task_cli.add_task("Todo task")
        self.task_cli.mark_task_status(self.last_task_id(), "todo")

        self.task_cli.add_task("In progress task")
        self.task_cli.mark_task_status(self.last_task_id(), "in-progress")

        self.task_cli.add_task("Done task")
        self.task_cli.mark_task_status(self.last_task_id(), "done")

        # Check to-do list
        todo_tasks = [
            task for task in self.task_cli.tasks.values() if task["status"] == "todo"
        ]
        self.assertEqual(len(todo_tasks), 1)
        self.assertEqual(todo_tasks[0]["description"], "Todo task")

        # Check in-progress task list
        in_progress_tasks = [
            task
            for task in self.task_cli.tasks.values()
            if task["status"] == "in-progress"
        ]
        self.assertEqual(len(in_progress_tasks), 1)
        self.assertEqual(in_progress_tasks[0]["description"], "In progress task")

        # Check done task list
        done_tasks = [
            task for task in self.task_cli.tasks.values() if task["status"] == "done"
        ]
        self.assertEqual(len(done_tasks), 1)
        self.assertEqual(done_tasks[0]["description"], "Done task")

    def test_load_and_save_tasks(self):
        """Test the task loading and saving functionality."""
        # Add a task
        self.task_cli.add_task("Persistent task")

        # Create a new TaskCLI object to reload from file
        new_task_cli = TaskCLI(self.temp_file)

        # Check that the task is saved and loaded correctly
        self.assertEqual(len(new_task_cli.tasks), 1)
        self.assertEqual(
            new_task_cli.tasks[self.last_task_id()]["description"], "Persistent task"
        )

    def test_error_handling(self):
        """Check error handling."""
        # Try updating a non-existent task
        with patch("builtins.print") as mock_print:
            non_existent_id = str(uuid.uuid4())
            self.task_cli.update_task(non_existent_id, "Should fail")
            mock_print.assert_called_once_with(
                f"Task with ID {non_existent_id} not found"
            )

        # Try deleting a non-existent task
        with patch("builtins.print") as mock_print:
            non_existent_id = str(uuid.uuid4())
            self.task_cli.delete_task(non_existent_id)
            mock_print.assert_called_once_with(
                f"Task with ID {non_existent_id} not found"
            )

        # Try marking a status with an ID that doesn't exist
        with patch("builtins.print") as mock_print:
            non_existent_id = str(uuid.uuid4())
            self.task_cli.mark_task_status(non_existent_id, "done")
            mock_print.assert_called_once_with(
                f"Task with ID {non_existent_id} not found"
            )


if __name__ == "__main__":
    unittest.main()
