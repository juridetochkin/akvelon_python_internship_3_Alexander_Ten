from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TransactionViewSet, GetIncomeSumView, GetOutcomeSumView

router = SimpleRouter()
router.register('transactions', TransactionViewSet)

urlpatterns = [
    path('income/', GetIncomeSumView.as_view()),
    path('outcome/', GetOutcomeSumView.as_view()),
    path('', include(router.urls), name='transactions'),
]
