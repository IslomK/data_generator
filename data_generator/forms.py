from django import forms
from django.forms.models import inlineformset_factory

from data_generator.models import Schema, SchemaField


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ['name', 'column_separator', 'string_character']


class SchemaFieldForm(forms.ModelForm):
    class Meta:
        model = SchemaField
        exclude = ['id', 'schema_id', 'created_at', 'updated_at']


class DatasetForm(forms.Form):
    row_number = forms.IntegerField(min_value=5, required=True)
    schema = forms.ModelChoiceField(queryset=Schema.objects.all(), required=True)


SchemaFieldFormSet = inlineformset_factory(Schema,
                                           SchemaField,
                                           form=SchemaFieldForm,
                                           fields=['name', 'field_type', 'max_int', 'min_int', 'text_len', 'order',
                                                   'start_date', 'end_date'])