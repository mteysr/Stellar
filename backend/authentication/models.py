from django.db import models
from django.contrib.auth.models import User


class StellarWallet(models.Model):
    """Model to store Stellar wallet information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stellar_wallet')
    public_key = models.CharField(max_length=56, unique=True)  # Stellar public key (G...)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stellar_wallets'
        
    def __str__(self):
        return f"{self.user.username} - {self.public_key}"


class AuthenticationSession(models.Model):
    """Model to store authentication sessions"""
    wallet = models.ForeignKey(StellarWallet, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=255, unique=True)
    challenge = models.TextField()  # Challenge message for signature verification
    signature = models.TextField(null=True, blank=True)  # User's signature
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'authentication_sessions'
        
    def __str__(self):
        return f"Session for {self.wallet.public_key}"
