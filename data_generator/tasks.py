from __future__ import absolute_import, unicode_literals

import csv
import logging
import tempfile

from celery import Task
from django.db import DatabaseError
from django.utils import timezone
from django.core.files.storage import DefaultStorage
from faker import Faker

from data_generator.models import Schema, SchemaField
from data_generator.models.schema import Dataset
from planeks.celery import app
from storages.backends.s3boto3 import S3Boto3Storage

from planeks.storages import PublicMediaStorage

logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=20)
def generate_data(self: Task, schema_id, row_number):

    try:
        schema = Schema.objects.get(id=schema_id)
    except DatabaseError as ex:
        logger.error("Could not find schema with id - {}".format(schema_id))
        raise ex

    try:
        dataset = Dataset.objects.create(
            schema_id=schema_id,
            row_number=row_number,
            task_id=self.request.id,
        )
    except DatabaseError as ex:
        logger.error("Could not find schema with id - {}".format(schema_id))
        raise ex

    methods = {}
    headers = []

    for schema_field in schema.schema_fields.all().order_by('order'):
        headers.append(schema_field.name)

        if schema_field.field_type == SchemaField.INTEGER:
            arguments = {
                "max_value": schema_field.max_int,
                "min_value": schema_field.min_int,
                "step": 1
            }

        elif schema_field.field_type == SchemaField.TEXT:
            arguments = {
                "max_nb_chars": schema_field.text_len
            }

        elif schema_field.field_type == SchemaField.DATE:
            arguments = {
                "date_start": schema_field.start_date,
                "date_end": schema_field.end_date
            }
        else:
            arguments = {}

        methods.update({
            get_fake_type(schema_field.field_type): arguments
        })

    media_storage = DefaultStorage()

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        with open(temp_file.name, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=schema.column_separator, quotechar=schema.string_character,
                                quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(headers)

            for i in range(0, row_number):
                self.update_state(state='IN PROGRESS', meta={"progress": round((i/row_number) * 100)})
                writer.writerow([method(**arguments) for method, arguments in methods.items()])

            csv_file.close()

        filename = f'{schema.id}_{dataset.id}_{row_number}".csv'
        media_storage.save(filename, temp_file)
        dataset.path = media_storage.url(filename)

    dataset.finished_at = timezone.now()
    dataset.save()

    self.update_state(state='FINISHED', meta={"progress": 100})


def get_fake_type(field_type):
    fake = Faker()

    fake_types = {
        SchemaField.ADDRESS: fake.address,
        SchemaField.PHONE_NUMBER: fake.phone_number,
        SchemaField.DATE: fake.date_between_dates,
        SchemaField.INTEGER: fake.pyint,
        SchemaField.TEXT: fake.text,
        SchemaField.JOB: fake.job,
        SchemaField.COMPANY_NAME: fake.company,
        SchemaField.DOMAIN_NAME: fake.domain_name,
        SchemaField.EMAIL: fake.ascii_email,
        SchemaField.FULL_NAME: fake.name
    }

    return fake_types.get(field_type)