# Generated by Django 3.2 on 2021-04-23 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_generator', '0007_alter_schemafield_schema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schema',
            name='row_number',
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_number', models.IntegerField(null=True)),
                ('path', models.CharField(blank=True, max_length=256, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='data_generator.schema')),
            ],
        ),
    ]
