from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

base = [
    url(r'^chat/', include('chat.urls')),
    url(r'^admin/', admin.site.urls),
]
user_uploads = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = base + user_uploads
