from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from taskhub.models import Team, Project, Task, TaskType, Position
from datetime import timedelta

User = get_user_model()


class ProfileContextTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create position for workers
        cls.position = Position.objects.create(name="Developer")

        # Create workers
        cls.worker1 = User.objects.create_user(
            username="worker1", password="password", position=cls.position
        )
        cls.worker2 = User.objects.create_user(
            username="worker2", password="password", position=cls.position
        )

        # Create task types
        cls.task_type = TaskType.objects.create(name="Bug Fix")

        # Create teams
        cls.team1 = Team.objects.create(name="Team A")
        cls.team1.members.add(cls.worker1)

        cls.team2 = Team.objects.create(name="Team B")
        cls.team2.members.add(cls.worker2)

        # Create projects
        cls.project1 = Project.objects.create(
            name="Project 1",
            team=cls.team1,
            deadline=timezone.now() + timedelta(days=10),  # 10 days from now
        )
        cls.project2 = Project.objects.create(
            name="Project 2",
            team=cls.team1,
            deadline=timezone.now() - timedelta(days=10),  # 10 days ago
            is_completed=True,
        )

        cls.project3 = Project.objects.create(
            name="Project 3",
            team=cls.team2,
            deadline=timezone.now() + timedelta(days=5),  # 5 days from now
        )

        # Create tasks
        cls.task1 = Task.objects.create(
            name="Task 1",
            description="Active task",
            deadline=timezone.now() + timedelta(days=5),
            is_completed=False,
            task_type=cls.task_type,
            project=cls.project1,
        )
        cls.task2 = Task.objects.create(
            name="Task 2",
            description="Completed task",
            deadline=timezone.now() - timedelta(days=5),
            is_completed=True,
            task_type=cls.task_type,
            project=cls.project1,
        )
        cls.task3 = Task.objects.create(
            name="Task 3",
            description="Active task in another project",
            deadline=timezone.now() + timedelta(days=5),
            is_completed=False,
            task_type=cls.task_type,
            project=cls.project3,
        )

        # Assign tasks to workers
        cls.task1.assignees.add(cls.worker1)
        cls.task2.assignees.add(cls.worker1)
        cls.task3.assignees.add(cls.worker2)

    def test_profile_context_worker1(self):
        # Log in as worker1
        self.client.login(username="worker1", password="password")

        # Get the profile page
        response = self.client.get(reverse("profile"))

        # Check that the response is OK
        self.assertEqual(response.status_code, 200)

        # Check context data
        self.assertEqual(response.context["worker"], self.worker1)
        self.assertEqual(
            response.context["active_tasks"], 1
        )  # Worker1 has 1 active task
        self.assertEqual(
            response.context["finished_tasks"], 1
        )  # Worker1 has 1 completed task
        self.assertEqual(
            response.context["active_projects"], 1
        )  # Worker1 is assigned to 1 active project (Project 1)
        self.assertEqual(
            response.context["finished_projects"], 1
        )  # Worker1 is assigned to 1 finished project (Project 2)

    def test_profile_context_worker2(self):
        # Log in as worker2
        self.client.login(username="worker2", password="password")

        # Get the profile page
        response = self.client.get(reverse("profile"))

        # Check that the response is OK
        self.assertEqual(response.status_code, 200)

        # Check context data for worker2
        self.assertEqual(response.context["worker"], self.worker2)
        self.assertEqual(
            response.context["active_tasks"], 1
        )  # Worker2 has 1 active task
        self.assertEqual(
            response.context["finished_tasks"], 0
        )  # Worker2 has no completed tasks
        self.assertEqual(
            response.context["active_projects"], 1
        )  # Worker2 is assigned to 1 active project (Project 3)
        self.assertEqual(
            response.context["finished_projects"], 0
        )  # Worker2 has no finished projects

    def test_profile_context_no_tasks(self):
        # Create a worker with no tasks assigned
        worker3 = User.objects.create_user(
            username="worker3", password="password", position=self.position
        )

        # Log in as worker3
        self.client.login(username="worker3", password="password")

        # Get the profile page
        response = self.client.get(reverse("profile"))

        # Check that the response is OK
        self.assertEqual(response.status_code, 200)

        # Check context data for worker3
        self.assertEqual(response.context["worker"], worker3)
        self.assertEqual(response.context["active_tasks"], 0)  # Worker3 has no tasks
        self.assertEqual(response.context["finished_tasks"], 0)  # Worker3 has no tasks
        self.assertEqual(
            response.context["active_projects"], 0
        )  # Worker3 has no active projects
        self.assertEqual(
            response.context["finished_projects"], 0
        )  # Worker3 has no finished projects
