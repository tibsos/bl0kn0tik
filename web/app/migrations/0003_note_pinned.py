# Generated by Django 4.1.2 on 2022-11-14 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_notepad_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='pinned',
            field=models.BooleanField(default=False),
        ),
    ]
