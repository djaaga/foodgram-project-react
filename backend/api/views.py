from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Exists, OuterRef
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .mixins import ListRetrieveViewSet
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from recipes.models import Favorite, Ingredient, Recipe, Shopping, Tag
from .serializers import (IngredientSerializer, RecipeFollowSerializer,
                          RecipeGetSerializer, RecipeSerializer, TagSerializer)
from .utils import delete, post


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(shopping__user=self.request.user)

        is_favorited = self.request.query_params.get('is_favorited', 0)
        """Переменная is_in_shopping_cart используется в get_queryset()методе
        для фильтрации набора запросов на основе того,
        находится ли рецепт в корзине покупок
        аутентифицированного пользователя."""
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )

        if is_favorited is not None and int(is_favorited) == 1:
            subquery = Favorite.objects.filter(
                recipe=OuterRef('pk'), user=self.request.user
            )
            queryset = queryset.annotate(is_favorited=Exists(subquery))
        if is_in_shopping_cart is not None and int(is_in_shopping_cart) == 1:
            subquery = Shopping.objects.filter(
                recipe=OuterRef('pk'), user=self.request.user
            )
            queryset = queryset.filter(
                shopping__user=self.request.user).annotate(
                is_in_shopping_cart=Exists(subquery)
            )

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('Рецепт успешно удален',
                        status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipeSerializer

    @action(detail=True, methods=['POST', 'DELETE'],)
    def favorite(self, request, pk):
        if self.request.method == 'POST':
            return post(request, pk, Favorite, RecipeFollowSerializer)
        return delete(request, pk, Favorite)

    @action(detail=True, methods=['POST', 'DELETE'],)
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return post(request, pk, Shopping, RecipeFollowSerializer)
        return delete(request, pk, Shopping)
