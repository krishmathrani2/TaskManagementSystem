from app import create_app, db
from app.models import User, Project, Task
from datetime import datetime

app = create_app()
app.app_context().push()

db.session.query(Task).delete()
db.session.query(Project).delete()
db.session.query(User).delete()
db.session.commit()

user = User(username='admin', email='admin@example.com')
user.set_password('password')
db.session.add(user)
db.session.commit()

projects = [
    Project(name='Website Redesign', description='Complete overhaul of the corporate website to improve user experience and modernize the design.', user_id=user.id),
    Project(name='Mobile App Development', description='Development of a new mobile application to complement our web services and increase user engagement.', user_id=user.id),
    Project(name='Marketing Campaign', description='Launch a marketing campaign to promote our new product line and increase brand awareness.', user_id=user.id)
]

for project in projects:
    db.session.add(project)
db.session.commit()

tasks = [
    Task(name='Wireframe Design', description='Create wireframes for the new website layout, focusing on user-friendly navigation.', deadline=datetime.strptime('2024-06-15', '%Y-%m-%d'), priority='High', status='In Progress', user_id=user.id, project_id=projects[0].id),
    Task(name='User Testing', description='Conduct user testing sessions to gather feedback on the new website design.', deadline=datetime.strptime('2024-07-01', '%Y-%m-%d'), priority='Medium', status='To Do', user_id=user.id, project_id=projects[0].id),
    Task(name='API Integration', description='Integrate third-party APIs to enhance the functionality of the mobile app.', deadline=datetime.strptime('2024-06-20', '%Y-%m-%d'), priority='High', status='To Do', user_id=user.id, project_id=projects[1].id),
    Task(name='Social Media Ads', description='Design and schedule social media ads for the upcoming marketing campaign.', deadline=datetime.strptime('2024-06-25', '%Y-%m-%d'), priority='Medium', status='In Progress', user_id=user.id, project_id=projects[2].id),
    Task(name='Backend Development', description='Develop the backend services for the mobile app, ensuring scalability and security.', deadline=datetime.strptime('2024-06-30', '%Y-%m-%d'), priority='High', status='In Progress', user_id=user.id, project_id=projects[1].id)
]

for task in tasks:
    db.session.add(task)
db.session.commit()

print("Example data has been added to the database.")
