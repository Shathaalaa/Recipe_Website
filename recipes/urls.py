from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.user_login,name="login"),
    path('', views.recipe_list, name='recipe_list'),
    path('<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('category/<str:category>/', views.recipe_list, name='recipe_by_category'),
    path('add-recipe/', views.add_recipe, name = "add_recipe"),
    path('<int:recipe_id>/add-comment/', views.add_comment, name='add_comment'),
    path('<int:recipe_id>/like-ajax/', views.like_recipe_ajax, name='like_recipe_ajax')
]
