# Generated by Django 4.1.2 on 2022-11-13 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='active_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.note'),
        ),
        migrations.AddField(
            model_name='profile',
            name='active_notepad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.notepad'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='premium',
            field=models.BooleanField(default=True),
        ),
    ]
