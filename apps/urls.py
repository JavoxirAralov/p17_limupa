from django import views
from django.conf import urls
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path, include

from apps.views import IndexView, CustomLoginView, RegisterFormView, BlogDetailView, BlogListView, ProcessEmailView

urlpatterns = [
    path('', IndexView.as_view(), name='index_page'),
    path('blog-list', BlogListView.as_view(), name='blog_list_page'),
    path('blog-detail/<int:pk>', BlogDetailView.as_view(), name='blog_detail_page'),
    path('logout', LogoutView.as_view(next_page='index_page'), name='logout'),
    path('login', CustomLoginView.as_view(), name='login_page'),
    path('register', RegisterFormView.as_view(), name='register_page'),
    path('', IndexView.as_view(), name='index_page'),
    path('process_email/', ProcessEmailView.as_view(), name='process_email'),
]


def page_404(request, *args, **kwargs):
    return render(request, 'apps/404.html', status=404)


urls.handler404 = 'apps.urls.page_404'
