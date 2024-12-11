# Task CLI: Command-Line Task Management Application

## Description

Task CLI is a simple, powerful task management application written in Python. It allows you to manage tasks directly from the command line, store tasks in a JSON file, and provides essential features for task tracking and management.

_Note: This project is part of the Roadmap Projects: https://roadmap.sh/projects/task-tracker_

## Features

- ✅ Add new tasks
- ✏️ Update existing tasks
- 🗑️ Delete tasks
- 📌 Mark task status (Todo, In Progress, Done)
- 📋 List all tasks
- 🔍 Filter tasks by status

## System Requirements

- Python 3.7+
- Operating System: Linux, macOS, Windows

## Installation

### Option 1: Direct Usage

1. Clone the repository:
```bash
git clone https://github.com/ThuanD/task-tracker.git
cd task-cli
```

2. Make the script executable:
```bash
chmod +x task_cli.py
```

3. Run directly:
```bash
python task_cli.py add "Your task description"
```

### Option 2: Global Installation

1. Clone the repository
```bash
git clone https://github.com/ThuanD/task-tracker.git
cd task-cli
```

2. Create a symbolic link:
```bash
chmod +x task_cli.py
ln -s $(pwd)/task_cli.py /usr/local/bin/task-cli
```

## Usage

### Adding Tasks
```bash
task-cli add "Buy groceries"
```

### Updating Tasks
```bash
task-cli update <task-id> "Buy groceries and cook dinner"
```

### Deleting Tasks
```bash
task-cli delete <task-id>
```

### Marking Task Status
```bash
task-cli mark-in-progress <task-id>
task-cli mark-done <task-id>
```

### Listing Tasks
```bash
# List all tasks
task-cli list

# List tasks by status
task-cli list todo
task-cli list in-progress
task-cli list done
```

## Project Structure
```
task-cli/
│
├── task_cli.py         # Main application script
├── test_task_cli.py    # Unit tests
└── README.md           # Project documentation
```

## Running Tests

To run the unit tests:
```bash
python -m unittest test_task_cli.py
```

## Task Properties

Each task includes:
- `id`: Unique identifier
- `description`: Task description
- `status`: Current status (`todo`, `in-progress`, `done`)
- `createdAt`: Creation timestamp
- `updatedAt`: Last update timestamp

## Limitations

- No cloud synchronization
- Single-user local storage
- Relies on JSON file for persistence

## Future Improvements

- [ ] Add priority levels
- [ ] Implement due dates
- [ ] Create web/mobile interfaces
- [ ] Add task categories/tags

## Technologies Used

- Python 3
- Standard Library Modules:
    - `json` for data storage
    - `os` for file operations
    - `uuid` for unique identifiers
    - `datetime` for timestamps

## Troubleshooting

- Ensure Python 3.7+ is installed
- Check file permissions
- Verify JSON file integrity
- Restart application if unexpected behavior occurs

## License

This project is open-source.

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact & Support

Found an issue? Please open a GitHub issue with detailed information.

Project Link: [https://github.com/ThuanD/task-tracker](https://github.com/ThuanD/task-tracker)