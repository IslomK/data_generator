from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet

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
        fields = ['name', 'field_type', 'max_int', 'min_int', 'text_len', 'order',
                  'start_date', 'end_date']

    def clean(self):
        cd = self.cleaned_data
        field_type = cd.get('field_type')

        if field_type == SchemaField.INTEGER:
            if not bool(cd.get("max_int") and ("min_int")):
                self.add_error("max_int", "Minimum and maximum for integers are required")

        if field_type == SchemaField.TEXT:
            if not cd.get("text_len"):
                self.add_error("text_len", "Maximum number of chars is required")

        if field_type == SchemaField.DATE:
            if not (cd.get('start_date') and cd.get('end_date')):
                self.add_error("start_date", "Start date and end date are required")

        return cd


class DatasetForm(forms.Form):
    row_number = forms.IntegerField(min_value=5, required=True)
    schema = forms.ModelChoiceField(queryset=Schema.objects.all(), required=True)

    def clean(self):
        cd = self.cleaned_data
        schema = cd.get('schema')
        if not schema.schema_fields.all().exists():
            self.add_error("schema", "Schema should contain at least one field")
        return cd


class SchemaFieldFormset(inlineformset_factory(Schema, SchemaField, form=SchemaFieldForm)):
    def clean(self):
        super(SchemaFieldFormset, self).clean()

        if any(self.errors):
            return

        for form in self.forms:
            cd = form.cleaned_data
            field_type = cd.get('field_type')

            if field_type == SchemaField.INTEGER:
                if not bool(cd.get("max_int") and ("min_int")):
                    form.add_error("max_int", "Minimum and maximum for integers are required")

            if field_type == SchemaField.TEXT:
                if not cd.get("text_len"):
                    form.add_error("text_len", "Maximum number of chars is required")

            if field_type == SchemaField.DATE:
                if not bool(cd.get('start_date') and cd.get('end_date')):
                    form.add_error("start_date", "Start date and end date are required")

