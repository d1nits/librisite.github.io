from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    path('reviews/', views.review_list, name='review_list'),
    path('book/<slug:book_slug>/review/add/', views.review_create, name='review_create'),
    path('review/<int:pk>/', views.review_detail, name='review_detail'),
    path('review/<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('books/', views.book_list, name='book_list'),
    path('book/add/', views.book_create, name='book_create'),
    path('book/<slug:slug>/', views.book_detail, name='book_detail'),
    path('review/add/', views.review_create, name='review_create'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('selections/', views.selection_list, name='selection_list'),
    path('selection/create/', views.create_selection, name='selection_create'),
    path('selection/<int:pk>/', views.selection_detail, name='selection_detail'),
    path('selection/<int:pk>/edit/', views.edit_selection, name='selection_edit'),
    path('selection/<int:pk>/delete/', views.delete_selection, name='selection_delete'),
    path('home/', views.home, name='home'),
    path('homepage/', views.homepage, name='homepage'),
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
