"""myproj1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib.auth.views import login_required
from .views import BookDetail, AddBookDataView, UpdateBookForm, download

urlpatterns = [
    path('add_book/', login_required(AddBookDataView.as_view()), name='add_book'),
    path('update/<int:pk>/', login_required(UpdateBookForm.as_view()), name='update_book' ),
    path('<slug:book_name>/', login_required(BookDetail.as_view()), name='book_detail'),
    path('r^download/(?P<path>\w+)$/', login_required(download), name='download'),
    ]
