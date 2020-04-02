from django.urls import path
from recipe.views import (
    index,
    RecipeCreate,
    RecipeUpdate,
    recipe_detail,
    like_recipe,
    unlike_recipe,
    list_of_recipes_with,
    search_recipe,
    delete_recipe,
    rate_recipe,
    )

urlpatterns = [
    path('', index, name='index'),
    path('add/', RecipeCreate.as_view(), name='recipe-add'),
    path('update/<slug:slug>/', RecipeUpdate.as_view(), name='update_recipe'),
    path('delete/<slug:slug>/', delete_recipe, name="delete_recipe"),
    path('detail/<slug:slug>/', recipe_detail, name="recipe_detail"),

    path('search/', search_recipe, name="search_recipe"),
    path(
        'list-of-recipes-with/<str:ingredient>/',
        list_of_recipes_with,
        name='list_of_recipes_with',
        ),

    path('like/', like_recipe, name="like_recipe"),
    path('unlike/<str:id>/', unlike_recipe, name="unlike_recipe"),
    path('rate/', rate_recipe, name="rate_recipe"),
]
