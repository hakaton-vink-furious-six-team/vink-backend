# Generated by Django 5.0.3 on 2024-03-29 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("user_profile", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "status",
                    models.CharField(
                        choices=[("open", "Открыт"), ("closed", "Закрыт")],
                        default="open",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("closed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "rating",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (0, "0"),
                            (1, "1"),
                            (2, "2"),
                            (3, "3"),
                            (4, "4"),
                            (5, "5"),
                        ],
                        default=3,
                        help_text="Оцените помощь нашего сотрудника по шкале от 0 до 5, где 0 - очень плохо, 5 - великолепно.",
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chats",
                        to="user_profile.userprofile",
                    ),
                ),
            ],
        ),
    ]
