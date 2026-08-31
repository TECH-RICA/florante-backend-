from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teammember",
            name="image",
            field=models.URLField(
                blank=True,
                help_text="URL of the member's photo (upload from the admin panel).",
            ),
        ),
        migrations.AddField(
            model_name="teammember",
            name="portfolio_url",
            field=models.URLField(blank=True, help_text="Link to the member's portfolio."),
        ),
    ]