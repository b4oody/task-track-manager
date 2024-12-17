import json
from django.core.management.base import BaseCommand
from taskhub.models import Position, Worker, Team, Project, Task, Commentary, TaskType

class Command(BaseCommand):
    help = "Import mock data from JSON file"

    def handle(self, *args, **kwargs):
        # Path to your mock_data.json file
        file_path = "fixture_data.json"  # Помістіть JSON у корінь вашого проєкту або змініть шлях

        with open(file_path, "r") as file:
            data = json.load(file)

        # Create positions
        for position_data in data["positions"]:
            Position.objects.update_or_create(id=position_data["id"], defaults=position_data)

        # Create task types
        for task_type_data in data["task_types"]:
            TaskType.objects.update_or_create(id=task_type_data["id"], defaults=task_type_data)

        # Create users
        for user_data in data["users"]:
            position_id = user_data.pop("position_id")
            position = Position.objects.get(id=position_id)
            Worker.objects.update_or_create(
                id=user_data["id"],
                defaults={**user_data, "position": position}
            )

        # Create teams
        for team_data in data["teams"]:
            member_ids = team_data.pop("members")
            team, created = Team.objects.update_or_create(
                id=team_data["id"],
                defaults=team_data
            )
            team.members.set(member_ids)

        # Create projects
        for project_data in data["projects"]:
            team_id = project_data.pop("team_id")
            team = Team.objects.get(id=team_id)
            Project.objects.update_or_create(
                id=project_data["id"],
                defaults={**project_data, "team": team}
            )

        # Create tasks
        for task_data in data["tasks"]:
            task_type_id = task_data.pop("task_type_id")
            project_id = task_data.pop("project_id")
            assignees = task_data.pop("assignees")
            task_type = TaskType.objects.get(id=task_type_id)
            project = Project.objects.get(id=project_id)
            task, created = Task.objects.update_or_create(
                id=task_data["id"],
                defaults={**task_data, "task_type": task_type, "project": project}
            )
            task.assignees.set(assignees)

        # Create commentaries
        for commentary_data in data["commentaries"]:
            worker_id = commentary_data.pop("worker_id")
            task_id = commentary_data.pop("task_id")
            worker = Worker.objects.get(id=worker_id)
            task = Task.objects.get(id=task_id)
            Commentary.objects.update_or_create(
                id=commentary_data["id"],
                defaults={**commentary_data, "worker": worker, "task": task}
            )

        self.stdout.write(self.style.SUCCESS("Mock data successfully imported!"))
