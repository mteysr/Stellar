from rest_framework import serializers
from .models import StellarWallet


class WalletConnectSerializer(serializers.Serializer):
    """Serializer for wallet connection"""
    public_key = serializers.CharField(max_length=56)
    

class SignatureVerifySerializer(serializers.Serializer):
    """Serializer for signature verification"""
    public_key = serializers.CharField(max_length=56)
    signature = serializers.CharField()
    challenge = serializers.CharField()


class WalletSerializer(serializers.ModelSerializer):
    """Serializer for Stellar wallet"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = StellarWallet
        fields = ['id', 'username', 'public_key', 'created_at', 'last_login']
        read_only_fields = ['id', 'created_at', 'last_login']


class BalanceSerializer(serializers.Serializer):
    """Serializer for account balance"""
    asset_code = serializers.CharField()
    asset_type = serializers.CharField()
    balance = serializers.CharField()
    asset_issuer = serializers.CharField(required=False, allow_null=True)


class PaymentSerializer(serializers.Serializer):
    """Serializer for payment transactions"""
    destination = serializers.CharField(max_length=56, help_text="Destination Stellar address")
    amount = serializers.DecimalField(max_digits=20, decimal_places=7, help_text="Amount to send")
    asset_code = serializers.CharField(default='XLM', help_text="Asset code (default: XLM)")
    asset_issuer = serializers.CharField(required=False, allow_null=True, help_text="Asset issuer (for custom assets)")
    memo = serializers.CharField(required=False, allow_blank=True, max_length=28, help_text="Optional memo")
    secret_key = serializers.CharField(write_only=True, help_text="Sender's secret key for signing")
    
    def validate_destination(self, value):
        """Validate destination address format"""
        if not value.startswith('G'):
            raise serializers.ValidationError("Invalid Stellar public key format")
        if len(value) != 56:
            raise serializers.ValidationError("Stellar public key must be 56 characters")
        return value
    
    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value


class TransactionSerializer(serializers.Serializer):
    """Serializer for transaction history"""
    id = serializers.CharField()
    type = serializers.CharField()
    created_at = serializers.DateTimeField()
    transaction_hash = serializers.CharField()
    source_account = serializers.CharField()
    from_address = serializers.CharField(required=False, allow_null=True)
    to_address = serializers.CharField(required=False, allow_null=True)
    amount = serializers.CharField(required=False, allow_null=True)
    asset_code = serializers.CharField(required=False, allow_null=True)
    asset_type = serializers.CharField(required=False, allow_null=True)
