from django.contrib import admin

from data_generator.models import Schema, SchemaField
from data_generator.models.schema import Dataset

admin.site.register(Schema)
admin.site.register(SchemaField)
admin.site.register(Dataset)