import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from recipe.forms import RatingForm
from recipe.models import Ingredients, Rating, Recipe

# Create your views here.
STATUS = "published"

def index(request):
    context = dict()
    recipes = Recipe.objects.filter(
        status=STATUS,
    ).order_by('-createt_at')

    most_ingredients = Ingredients.objects.annotate(
        recipe_count=Count('recipe')
    ).order_by('-recipe_count')[:5]

    context['recipe_count'] = recipes.count()

    paginator = Paginator(recipes, 2)
    page = request.GET.get('page', 1)
    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    
    context["recipes"] = recipes
    context['most_ingredients'] = most_ingredients
    return render(request, 'recipe/index.html', context)


class RecipeCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['name', 'image', 'description', 'difficulty', 'ingredients']
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    success_url = "/"
    success_message = "Your recipe saved succesfully"

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.owner = self.request.user
        recipe.status = STATUS
        recipe.save()
        recipe.slug = slugify(recipe.name) + "-" + str(recipe.pk)
        recipe.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('index'))


class RecipeUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['name', 'image', 'description', 'difficulty', 'ingredients']
    template_name_suffix = '_update_form'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    success_url = "/user/recipe-list/"
    success_message = "Your recipe updated succesfully"


def recipe_detail(request, slug):
    context = dict()
    recipe = get_object_or_404(Recipe, slug=slug)
    rating_form = RatingForm()
    context['rating_form'] = rating_form
    context['recipe'] = recipe
    return render(request, 'recipe/detail.html', context)


@login_required()
def like_recipe(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        recipe = get_object_or_404(Recipe, slug=slug)

        if recipe.likes.filter(id=user.id).exists():
            recipe.likes.remove(user)
        else:
            recipe.likes.add(user)

    ctx = {'likes_count': recipe.total_likes}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


@login_required()
def unlike_recipe(request, id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=id)
    recipe.likes.remove(user)
    messages.success(request, "Recipe removed successfully")
    return redirect("user_like_recipe_list")


def list_of_recipes_with(request, ingredient):
    context = dict()
    recipes = Recipe.objects.filter(ingredients__name=ingredient)
    most_ingredients = Ingredients.objects.annotate(
        recipe_count=Count('recipe')
    ).order_by('-recipe_count')[:5]

    context['recipes'] = recipes
    context['title'] = ingredient
    context['most_ingredients'] = most_ingredients
    return render(request, 'recipe/list_of_recipes_with.html', context)


def search_recipe(request):
    context = dict()
    search_query = request.GET.get('q', None)
    recipes = Recipe.objects.filter(Q(name__contains=search_query) | Q(
        ingredients__name__contains=search_query)).distinct()
    context['title'] = search_query
    context['recipes'] = recipes
    return render(request, 'recipe/search_result.html', context)


@login_required()
def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, owner=request.user)
    if recipe:
        recipe.status = "deleted"
        recipe.save()
        messages.info(request, "Your recipe deleted succesfully.")
        return redirect('user_recipe_list')

    return 404


@login_required()
def rate_recipe(request):
    if request.method == 'POST':
        context = dict()
        user = request.user
        slug = request.POST.get('slug', None)
        point = request.POST.get('point', None)
        recipe = Recipe.objects.get(slug=slug)
        
        if not Rating.objects.filter(owner=user, recipe=recipe).exists():
            Rating.objects.create(owner=user, recipe=recipe, rate=point)
            rating = recipe.rating_set.first().rating_avg()
            context['rating'] = rating
            context['point'] = point
            return HttpResponse(json.dumps(context), content_type='application/json')
        context['error'] = "You have already rated this recipe."
        return HttpResponse(json.dumps(context), content_type='application/json')
        

def error_404_view(request, exception):
    return render(request,'base/page-404.html')  