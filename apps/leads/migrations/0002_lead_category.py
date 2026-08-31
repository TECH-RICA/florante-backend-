from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leads", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lead",
            name="category",
            field=models.CharField(
                choices=[("individual", "Individual"), ("organization", "Organization")],
                default="organization",
                max_length=20,
            ),
        ),
    ]