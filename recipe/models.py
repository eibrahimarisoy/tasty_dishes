from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
# Create your models here.
DEFAULT_STATUS = "draft"
STATUS = [
    # left side: DB
    # right side: human-readable name
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('deleted', 'Deleted'),
]

DEFAULT_DIFFICULTY = "easy"
DIFFICULTIES = [
    ('easy', 'Easy'),
    ('moderate', 'Moderate'),
    ('hard', 'Hard'),
]

DEFAULT_POINT = "5"
POINTS = [
    (5, '5'),
    (4, '4'),
    (3, '3'),
    (2, '2'),
    (1, '1'),
]


class Ingredient(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        default=DEFAULT_STATUS,
        choices=STATUS,
        max_length=15,
        verbose_name="Status"
    )
    name = models.CharField(max_length=100, verbose_name="Recipe Name")
    slug = models.SlugField(
        max_length=200,
    )
    description = RichTextField(verbose_name="Description")
    difficulty = models.CharField(
        max_length=10,
        default=DEFAULT_DIFFICULTY,
        choices=DIFFICULTIES,
        verbose_name="Difficulty",
    )
    image = models.ImageField(verbose_name="Image")
    ingredients = models.ManyToManyField(
        Ingredient,
        help_text="Hold down the Ctrl (Windows) / Command (Mac) button to select multiple options.")
    likes = models.ManyToManyField(User, related_name='likes')

    createt_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rate = models.IntegerField(
        choices=POINTS,
        default=DEFAULT_POINT,
        )

    def rating_avg(self):
        sum = Rating.objects.filter(
            recipe=self.recipe
            ).aggregate(total=Sum('rate')).get('total')
        counts = Rating.objects.filter(recipe=self.recipe).count()
        return sum / counts
