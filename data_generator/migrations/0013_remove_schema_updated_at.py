# Generated by Django 3.2 on 2021-04-28 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_generator', '0012_dataset_task_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schema',
            name='updated_at',
        ),
    ]
