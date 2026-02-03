from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import thread_create, thread_edit, thread_delete, thread_detail, thread_list

app_name = 'forum'  

urlpatterns = [
    path('forum/', thread_list, name='thread_list'), 
    path('forum/create/', thread_create, name='thread_create'),  
    path('forum/<int:thread_id>/delete/', thread_delete, name='thread_delete'),  
    path('forum/<int:thread_id>/edit/', thread_edit, name='thread_edit'),
    path('forum/<int:thread_id>/', thread_detail, name='thread_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)