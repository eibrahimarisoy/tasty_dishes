from django.urls import path
from user.views import (
    user_login,
    user_register,
    user_logout,
    user_like_recipe_list,
    user_recipe_list,
    user_profile,
    update_user_profile,
    change_password,
    )


urlpatterns = [
    path('register/', user_register, name="user_register"),
    path('login/', user_login, name="user_login"),
    path('logout/', user_logout, name="user_logout"),
    path('profile/', user_profile, name="user_profile"),
    path('update-profile/', update_user_profile, name="update_user_profile"),
    path('change-password/', change_password, name="change_password"),

    path('recipe-list/', user_recipe_list, name="user_recipe_list"),
    path(
        'like-recipe-list/',
        user_like_recipe_list,
        name="user_like_recipe_list"
        ),
]
