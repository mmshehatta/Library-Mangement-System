

from django.urls import path
from . import views
app_name='lms_app'

urlpatterns = [
    path('', views.index , name='index'),
    path('books', views.books , name='books'),
    path('update/<int:id>', views.update , name='update'),
    path('delete/<int:id>', views.delete , name='delete'),
]