from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TransactionViewSet, GetIncomeSumView, GetOutcomeSumView

router = SimpleRouter()
router.register('transactions', TransactionViewSet)

urlpatterns = [
    path('income/', GetIncomeSumView.as_view(), name='income'),
    path('outcome/', GetOutcomeSumView.as_view(), name='outcome'),
    path('', include(router.urls), name='transactions'),
]
