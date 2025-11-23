from django.contrib import admin
from .models import StellarWallet, AuthenticationSession


@admin.register(StellarWallet)
class StellarWalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'public_key', 'created_at', 'last_login']
    search_fields = ['public_key', 'user__username']
    readonly_fields = ['created_at', 'last_login']


@admin.register(AuthenticationSession)
class AuthenticationSessionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'is_verified', 'created_at', 'expires_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['wallet__public_key', 'session_key']
    readonly_fields = ['created_at']
