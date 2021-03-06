from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('data_generator.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'data_generator.views.handler404'
handler500 = 'data_generator.views.handler500'

