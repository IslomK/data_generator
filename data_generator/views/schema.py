from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError, transaction, IntegrityError
from django.shortcuts import render, redirect
from django.views import View

from data_generator.forms import SchemaForm, SchemaFieldFormSet, DatasetForm
from data_generator.models import Schema, SchemaField


class SchemaListView(LoginRequiredMixin, View):
    template_name = 'data_schemas.html'
    login_url = 'login'

    def get(self, request):

        try:
            data_schemas = Schema.objects.all()
        except DatabaseError as ex:
            raise ex

        return render(request, self.template_name, {"schemas": data_schemas})


class SchemaCreateView(LoginRequiredMixin, View):
    form = SchemaForm
    formset = SchemaFieldFormSet
    template_name = 'edit_schema.html'
    login_url = 'login'

    def get(self, request):
        return render(request, self.template_name, {"schema_form": self.form(), "schema_field_form": self.formset()})

    def post(self, request):
        schema_field_formset = self.formset(request.POST)
        schema_form = self.form(request.POST)

        if schema_form.is_valid() and schema_field_formset.is_valid():
            try:
                with transaction.atomic():

                    schema = Schema.objects.create(**schema_form.cleaned_data)

                    schema_fields = []

                    for schema_field_form in schema_field_formset:
                        if schema_field_form.has_changed():
                            cd = schema_field_form.cleaned_data

                            schema_fields.append(SchemaField(
                                name=cd.get('name'),
                                field_type=cd.get('field_type'),
                                order=cd.get('order'),
                                schema_id=schema.id
                            ))

                    SchemaField.objects.bulk_create(schema_fields)

            except (IntegrityError, DatabaseError) as ex:  # If the transaction failed
                messages.error(request, 'There was an error saving your schema.')
                raise ex
        else:
            return render(request, self.template_name,
                          {"schema_form": schema_form, "schema_field_form": schema_field_formset})

        return redirect('schemas')


class SchemaDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        try:
            Schema.objects.filter(id=pk).delete()
        except (IntegrityError, DatabaseError):  # If the transaction failed
            messages.error(request, 'There was an error saving your schema.')
            return

        return redirect('schemas')


class SchemaEditView(LoginRequiredMixin, View):
    form = SchemaForm
    formset = SchemaFieldFormSet
    template_name = 'edit_schema.html'
    login_url = 'login'

    def post(self, request, pk):
        try:
            schema = Schema.objects.get(id=pk)
        except Exception as ex:
            raise ex

        schema_field_formset = self.formset(request.POST, instance=schema)
        schema_form = self.form(request.POST, instance=schema)

        if schema_form.is_valid() and schema_field_formset.is_valid():
            try:
                with transaction.atomic():
                    schema_form.save()
                    schema_field_formset.save()
            except Exception as ex:
                raise ex
        else:
            return render(request, self.template_name,
                          {"schema_form": schema_form, "schema_field_form": schema_field_formset})

        return redirect('schemas')

    def get(self, request, pk):
        try:
            schema = Schema.objects.get(id=pk)
        except Exception as ex:
            raise ex

        return render(request, self.template_name, {"schema_form": self.form(instance=schema), "schema_field_form": self.formset(instance=schema)})


class SchemaDatasetCreate(LoginRequiredMixin, View):
    form = DatasetForm
    template_name = 'dataset_edit.html'
    login_url = 'login'

    def get(self, request, pk):
        try:
            schema = Schema.objects.get(id=pk)
        except Exception as ex:
            raise ex

        return render(request, self.template_name, {"form": self.form({"schema": schema})})
