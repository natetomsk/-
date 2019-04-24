from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='index'),
    path('bookss/', views.book_list, name='books'),
    path('books/', views.Books.as_view(), name='books'),
	path('books/reserved/', views.Books_Reserved.as_view(), name='books reserved'),
	path('books/available/', views.Books_Available.as_view(), name='books available'),
	path('authors/', views.Authors.as_view(), name='authors'),
	path('users/', views.Users.as_view(), name='users'),
	path('user_profile/', views.user_profile, name='user_profile'),
    #path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'), 
]