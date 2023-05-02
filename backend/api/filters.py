from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef

import django_filters
from recipes.models import Favorite, Ingredient, Recipe, Shopping, Tag

User = get_user_model()


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = django_filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            subquery = Favorite.objects.filter(
                recipe=OuterRef('pk'), user=self.request.user
            )
            return queryset.annotate(is_favorited=Exists(subquery))
        else:
            return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        subquery = Shopping.objects.filter(
            recipe=OuterRef('pk'), user=self.request.user
        )
        queryset = queryset.annotate(
            is_in_shopping_cart=Exists(subquery)
        )
        if value:
            return queryset.filter(shopping__user=self.request.user)
        else:
            return queryset
