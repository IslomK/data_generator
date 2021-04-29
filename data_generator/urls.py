from django.urls import path
from data_generator import views
from django.contrib.auth import logout


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('schemas/', views.SchemaListView.as_view(), name='schemas'),
    path('datasets/', views.DatasetListView.as_view(), name='datasets'),
    path('datasets/add/', views.DatasetEditView.as_view(), name='dataset_create'),
    path('schemas/add/', views.SchemaCreateView.as_view(), name='schema_create'),
    path('schemas/<int:pk>/dataset/add/', views.SchemaDatasetCreate.as_view(), name='schema_dataset_create'),
    path('schemas/delete/<int:pk>/', views.SchemaDeleteView.as_view(), name='schema_delete'),
    path('schemas/edit/<int:pk>/', views.SchemaEditView.as_view(), name='schema_edit'),
]