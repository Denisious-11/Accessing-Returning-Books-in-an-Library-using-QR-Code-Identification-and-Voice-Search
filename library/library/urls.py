"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from library_app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    ##########login start
    url(r'^$',show_index),
    url(r'^show_index', show_index, name="show_index"),
    url(r'^check_login', check_login, name="check_login"),
    url(r'^logout',logout,name="logout"),
    url(r'^register',register,name="register"),
    url(r'^find_login',find_login,name="find_login"),
    ##########login end

    ################Admin start
    url(r'^show_home_admin',show_home_admin,name="show_home_admin"),
    url(r'^show_request_admin',show_request_admin,name="show_request_admin"),
    url(r'^approve',approve,name="approve"),
    url(r'^reject',reject,name="reject"),
    url(r'^view_users_admin',view_users_admin,name="view_users_admin"),
    url(r'^view_add_book_admin',view_add_book_admin,name="view_add_book_admin"),
    url(r'^add_book',add_book,name="add_book"),
    url(r'^view_books_admin',view_books_admin,name="view_books_admin"),
    url(r'^edit',edit,name="edit"),
    url(r'^delete',delete,name="delete"),
    url(r'^get_issue_requests_admin',get_issue_requests_admin,name="get_issue_requests_admin"),
    url(r'^accept',accept,name="accept"),
    url(r'^deny',deny,name="deny"),
    url(r'^view_issue_details_admin',view_issue_details_admin,name="view_issue_details_admin"),
    url(r'^get_return_requests_admin',get_return_requests_admin,name="get_return_requests_admin"),
    url(r'^verify',verify,name="verify"),
    url(r'^view_return_details_admin',view_return_details_admin,name="view_return_details_admin"),
    url(r'^get_user_details',get_user_details,name="get_user_details"),
    url(r'^update_user_details',update_user_details,name="update_user_details"),
    url(r'^search_book_user',search_book_user,name="search_book_user"),
    url(r'^request_book',request_book,name="request_book"),
    url(r'^get_my_books',get_my_books,name="get_my_books"),
    url(r'^get_info',get_info,name="get_info"),
    url(r'^return_book',return_book,name="return_book"),
    url(r'^get_my_return_books',get_my_return_books,name="get_my_return_books"),
    url(r'^display_admin_scan_book',display_admin_scan_book,name="display_admin_scan_book"),
    url(r'^admin_scan_book',admin_scan_book,name="admin_scan_book"),

]
