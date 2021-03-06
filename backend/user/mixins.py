from rest_framework import mixins, viewsets


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """ -- Используется для user.views.py UserViewSet -- """
    pass
