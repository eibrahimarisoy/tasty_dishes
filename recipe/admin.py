from django.contrib import admin
from recipe.models import Recipe, Ingredients, Rating

# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'status',)
    list_filter = ('status',)
    list_editable = ('status',)



admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients)
admin.site.register(Rating)