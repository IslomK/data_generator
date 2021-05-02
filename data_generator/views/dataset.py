import csv
import logging
import tempfile

import boto3

from celery.result import AsyncResult
from celery.exceptions import CeleryError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.views import View


from data_generator.forms import DatasetForm
from data_generator.models.schema import Dataset
from data_generator.tasks import generate_data
from planeks import settings
from planeks.storages import PublicMediaStorage

logger = logging.getLogger(__name__)


class DatasetEditView(LoginRequiredMixin, View):
    login_url = 'login'

    form = DatasetForm
    template_name = 'dataset_edit.html'

    def get(self, request):
        return render(request, self.template_name, {"form": self.form()})

    def post(self, request):

        form = self.form(request.POST)

        if form.is_valid():
            schema = form.cleaned_data.get('schema')
            row_number = form.cleaned_data.get('row_number')

            try:
                logger.info(
                    "Starting to generate dataset for schema - {}, row_number - {}".format(schema.id, row_number))
                generate_data.delay(schema.id, row_number)
            except CeleryError as ex:
                logger.error("Could not start the task. Error - {}".format(ex))
                raise ex

        else:
            return render(request, self.template_name, {"form": form})

        return redirect('datasets')


class DatasetListView(LoginRequiredMixin, View):
    template_name = 'datasets.html'
    login_url = 'login'

    def get(self, request):
        try:
            datasets = Dataset.objects.all()
        except DatabaseError as ex:
            raise ex

        resp = []
        for dataset in datasets:
            task = {
                "dataset_id": dataset.id,
                "schema": dataset.schema.name,
                "task_id": dataset.task_id,
                "created_at": dataset.created_at,
                "finished_at": dataset.finished_at,
                "row_number": dataset.row_number,
                "path": dataset.path
            }
            if dataset.task_id:
                result = AsyncResult(dataset.task_id)
                progress = None
                if result.info and result.status != 'FAILURE':
                    progress = result.info.get('progress')

                task.update({
                    "progress": progress,
                    "status": result.status
                })

            resp.append(task)

        return render(request, self.template_name, {"datasets": resp})
