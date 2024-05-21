from app import create_app, db
from app.models import Project, Task

app = create_app()

with app.app_context():
    projects = Project.query.all()
    tasks = Task.query.all()
    
    print("Projects:")
    for project in projects:
        print(f"Project ID: {project.id}, Name: {project.name}, Description: {project.description}")

    print("\nTasks:")
    for task in tasks:
        print(f"Task ID: {task.id}, Name: {task.name}, Description: {task.description}, Project ID: {task.project_id}, Deadline: {task.deadline}, Status: {task.status}")
