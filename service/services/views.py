from django.db.models import Prefetch, F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet

from services.models import Subscription
from services.serializers import SubscriptionSerializer
from clients.models import Client


# Create your views here.


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all()\
        .prefetch_related(Prefetch('client', queryset=Client.objects.all().select_related('user')
                                   .only('company_name', 'user__email')),
                          Prefetch('plan'))
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        response_data = {
            'result': response.data,
            'total_amount': queryset.aggregate(total=Sum('price')).get('total')
        }
        response.data = response_data
        return response
