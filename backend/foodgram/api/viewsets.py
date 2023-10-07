from rest_framework import mixins, viewsets


class ListViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    '''
    Вьюсет, который обеспечивает действие `list`.
    '''
    pass


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    '''
    Вьюсет, который обеспечивает действия `create` и 'destroy'.
    '''
    pass