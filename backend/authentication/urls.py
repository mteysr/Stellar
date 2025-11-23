from django.urls import path
from .views import (
    WalletConnectView, 
    VerifySignatureView, 
    WalletInfoView, 
    LogoutView,
    WalletBalanceView,
    SendPaymentView,
    TransactionHistoryView
)

urlpatterns = [
    path('connect/', WalletConnectView.as_view(), name='wallet-connect'),
    path('verify/', VerifySignatureView.as_view(), name='verify-signature'),
    path('wallet/', WalletInfoView.as_view(), name='wallet-info'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Stellar blockchain operations
    path('balance/', WalletBalanceView.as_view(), name='wallet-balance'),
    path('balance/<str:public_key>/', WalletBalanceView.as_view(), name='wallet-balance-by-key'),
    path('payment/', SendPaymentView.as_view(), name='send-payment'),
    path('transactions/', TransactionHistoryView.as_view(), name='transaction-history'),
    path('transactions/<str:public_key>/', TransactionHistoryView.as_view(), name='transaction-history-by-key'),
]
