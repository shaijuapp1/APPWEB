from django.urls import path
from .views import test_req, get_stock_price, get_currency_exchange, get_mf_price, get_currency_rate, get_exchange_rate

urlpatterns = [
    path('stock/<str:exchange>/<str:symbol>/', get_stock_price),  # Updated path for exchange and symbol
    path('currency/<str:symbol>/', get_currency_exchange),  # Existing currency API
    path('mutualfund/<str:symbol>/', get_mf_price),  # New mutual fund NAV API
    path('currency_rate/<str:from_currency>/<str:to_currency>/', get_currency_rate),
    path('exchange-rate/', get_exchange_rate, name='exchange-rate'),
    path('test/', test_req, name='test'),
]
