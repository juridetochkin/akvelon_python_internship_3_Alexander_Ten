from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TransactionViewSet, GetIncomeSumView, GetOutcomeSumView

# from django.conf.urls import url
# from .schema import schema_view


router = SimpleRouter()
router.register('transactions', TransactionViewSet)

urlpatterns = [
    path('income/', GetIncomeSumView.as_view()),
    path('outcome/', GetOutcomeSumView.as_view()),
    path('', include(router.urls), name='transactions'),
]

# urlpatterns += [
#     url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
# ]
