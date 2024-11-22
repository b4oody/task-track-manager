# Generated by Django 5.1.3 on 2024-11-21 23:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskhub", "0002_alter_worker_position"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="worker",
            options={"verbose_name": "Worker", "verbose_name_plural": "Workers"},
        ),
        migrations.AlterField(
            model_name="project",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[
                    ("urgent", "Urgent"),
                    ("high", "High"),
                    ("medium", "Medium"),
                    ("low", "Low"),
                ],
                db_index=True,
                default="U",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name="Commentary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("commentary_content", models.TextField()),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commentaries",
                        to="taskhub.task",
                    ),
                ),
                (
                    "worker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commentaries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]