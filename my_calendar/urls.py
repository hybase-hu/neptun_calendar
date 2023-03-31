from django.urls import path

from my_calendar.views import  login_view, register_view, calendar_view, calendar_update, logout_view

app_name="calendar"

urlpatterns = [
    path("login",login_view,name="login"),
    path("register",register_view,name="register"),
    path("logout",logout_view,name="logout"),
    path("update",calendar_update,name="update"),
    path("",calendar_view,name="calendar"),
]