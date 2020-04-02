from django.contrib import admin
from recipe.models import Recipe, Ingredient, Rating

# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'status',)
    list_filter = ('status',)
    list_editable = ('status',)



admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Rating)