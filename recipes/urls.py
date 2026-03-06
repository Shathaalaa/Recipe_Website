from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.user_login,name="login")
]
