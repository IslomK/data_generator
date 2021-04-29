from django.db import models


class Schema(models.Model):
    COMMA = ","
    SEMICOLON = ";"
    SPACE = " "
    PIPE = "|"

    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'

    COLUMN_SEPARATORS = (
        (COMMA, 'Comma (,)'),
        (SEMICOLON, 'Semicolon (;)'),
        (SPACE, 'Space ( )'),
        (PIPE, 'Pipe (|)')
    )

    STRING_CHARACTERS = (
        (DOUBLE_QUOTE, 'Double quotes (")'),
        (SINGLE_QUOTE, "Single quote (') ")
    )

    name = models.CharField(max_length=256)
    column_separator = models.CharField(choices=COLUMN_SEPARATORS, default=COMMA, max_length=256)
    string_character = models.CharField(choices=STRING_CHARACTERS, max_length=256, blank=True, default=DOUBLE_QUOTE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SchemaField(models.Model):
    FULL_NAME = "full_name"
    JOB = "job"
    EMAIL = "email"
    DOMAIN_NAME = "domain_name"
    PHONE_NUMBER = "phone_number"
    COMPANY_NAME = "company_name"
    TEXT = "text"
    INTEGER = "integer"
    ADDRESS = "address"
    DATE = "date"

    FIELD_TYPES = (
        (FULL_NAME, 'Full name'),
        (JOB, 'Job'),
        (EMAIL, 'Email'),
        (DOMAIN_NAME, 'Domain name'),
        (COMPANY_NAME, 'Company name'),
        (TEXT, 'Text'),
        (PHONE_NUMBER, 'Phone number'),
        (INTEGER, 'Integer'),
        (ADDRESS, 'Address'),
        (DATE, 'Date')
    )

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, null=True, related_name='schema_fields')
    name = models.CharField(max_length=256)
    field_type = models.CharField(choices=FIELD_TYPES, max_length=256)
    order = models.IntegerField(null=True, blank=True)
    min_int = models.IntegerField(null=True, blank=True)
    max_int = models.IntegerField(null=True, blank=True)
    text_len = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.field_type}"


class Dataset(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.DO_NOTHING)
    row_number = models.IntegerField(null=True)
    path = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    task_id = models.CharField(null=True, max_length=256)

    def __str__(self):
        return f"{self.schema.name}, {self.row_number}"