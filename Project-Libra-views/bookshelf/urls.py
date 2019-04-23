from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='index'),
    path('books/', views.Books.as_view(), name='books'),
	path('authors/', views.Authors.as_view(), name='authors'),
	path('users/', views.Users.as_view(), name='users'),
	path('user_profile/', views.user_profile, name='user_profile'),
    #path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'), 
]