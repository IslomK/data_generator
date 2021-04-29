# Generated by Django 3.2 on 2021-04-21 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_generator', '0002_schema_schemafield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schema',
            name='column_separator',
            field=models.IntegerField(blank=True, choices=[(1, 'Comma (,)'), (2, 'Dot (.)')], null=True),
        ),
        migrations.AlterField(
            model_name='schema',
            name='string_character',
            field=models.IntegerField(blank=True, choices=[(1, 'Double quotes (" ")'), (2, "Single quote (') ")], default=1),
        ),
    ]
