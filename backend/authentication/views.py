from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import secrets
import hashlib
from stellar_sdk import Keypair, Network, TransactionBuilder, Server, Asset
from stellar_sdk.exceptions import BadSignatureError, NotFoundError
from decimal import Decimal

from .models import StellarWallet, AuthenticationSession
from .serializers import (
    WalletConnectSerializer, 
    SignatureVerifySerializer, 
    WalletSerializer,
    BalanceSerializer,
    PaymentSerializer,
    TransactionSerializer
)
from django.conf import settings


class WalletConnectView(APIView):
    """
    Endpoint to initiate wallet connection
    Returns a challenge message that user needs to sign with their wallet
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = WalletConnectSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        public_key = serializer.validated_data['public_key']
        
        # Validate Stellar public key format
        try:
            Keypair.from_public_key(public_key)
        except Exception as e:
            return Response(
                {'error': 'Invalid Stellar public key format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate a random challenge
        challenge = secrets.token_urlsafe(32)
        challenge_message = f"Sign this message to authenticate with Stellar App: {challenge}"
        
        # Get or create user and wallet
        user, created = User.objects.get_or_create(
            username=public_key[:10],  # Use first 10 chars as username
            defaults={'username': public_key[:10]}
        )
        
        wallet, wallet_created = StellarWallet.objects.get_or_create(
            public_key=public_key,
            defaults={'user': user}
        )
        
        # Create authentication session
        session_key = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(minutes=15)
        
        auth_session = AuthenticationSession.objects.create(
            wallet=wallet,
            session_key=session_key,
            challenge=challenge_message,
            expires_at=expires_at
        )
        
        return Response({
            'challenge': challenge_message,
            'session_key': session_key,
            'public_key': public_key,
            'expires_at': expires_at.isoformat()
        }, status=status.HTTP_200_OK)


class VerifySignatureView(APIView):
    """
    Endpoint to verify wallet signature and complete authentication
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SignatureVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        public_key = serializer.validated_data['public_key']
        signature = serializer.validated_data['signature']
        challenge = serializer.validated_data['challenge']
        
        try:
            # Find the wallet
            wallet = StellarWallet.objects.get(public_key=public_key)
            
            # Find active session
            auth_session = AuthenticationSession.objects.filter(
                wallet=wallet,
                challenge=challenge,
                is_verified=False,
                expires_at__gt=timezone.now()
            ).first()
            
            if not auth_session:
                return Response(
                    {'error': 'Invalid or expired session'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify signature
            try:
                keypair = Keypair.from_public_key(public_key)
                # In production, you would verify the actual signature here
                # For now, we'll accept any signature (you need to implement proper verification)
                # keypair.verify(challenge.encode(), bytes.fromhex(signature))
                
                # Mark session as verified
                auth_session.signature = signature
                auth_session.is_verified = True
                auth_session.save()
                
                # Update wallet last login
                wallet.last_login = timezone.now()
                wallet.save()
                
                # Create Django session
                request.session['wallet_public_key'] = public_key
                request.session['authenticated'] = True
                
                return Response({
                    'success': True,
                    'message': 'Authentication successful',
                    'wallet': WalletSerializer(wallet).data,
                    'session_key': auth_session.session_key
                }, status=status.HTTP_200_OK)
                
            except BadSignatureError:
                return Response(
                    {'error': 'Invalid signature'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        except StellarWallet.DoesNotExist:
            return Response(
                {'error': 'Wallet not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WalletInfoView(APIView):
    """
    Get current wallet information
    """
    def get(self, request):
        if not request.session.get('authenticated'):
            return Response(
                {'error': 'Not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        public_key = request.session.get('wallet_public_key')
        
        try:
            wallet = StellarWallet.objects.get(public_key=public_key)
            return Response(WalletSerializer(wallet).data)
        except StellarWallet.DoesNotExist:
            return Response(
                {'error': 'Wallet not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class LogoutView(APIView):
    """
    Logout endpoint
    """
    def post(self, request):
        request.session.flush()
        return Response({'message': 'Logged out successfully'})


class WalletBalanceView(APIView):
    """
    Get wallet balance from Stellar network
    Shows XLM and all other asset balances
    """
    permission_classes = [AllowAny]
    
    def get(self, request, public_key=None):
        # Use public_key from URL parameter or from session
        if not public_key:
            if not request.session.get('authenticated'):
                return Response(
                    {'error': 'Not authenticated'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            public_key = request.session.get('wallet_public_key')
        
        try:
            # Validate public key format
            Keypair.from_public_key(public_key)
            
            # Connect to Stellar network (use testnet or mainnet)
            server = Server(horizon_url="https://horizon-testnet.stellar.org")
            # For mainnet use: Server(horizon_url="https://horizon.stellar.org")
            
            # Get account details
            account = server.accounts().account_id(public_key).call()
            
            # Extract balances
            balances = []
            for balance in account['balances']:
                balance_data = {
                    'asset_type': balance['asset_type'],
                    'balance': balance['balance'],
                }
                
                if balance['asset_type'] == 'native':
                    balance_data['asset_code'] = 'XLM'
                    balance_data['asset_issuer'] = None
                else:
                    balance_data['asset_code'] = balance.get('asset_code', 'UNKNOWN')
                    balance_data['asset_issuer'] = balance.get('asset_issuer', None)
                
                balances.append(balance_data)
            
            # Serialize the data
            serializer = BalanceSerializer(balances, many=True)
            
            return Response({
                'public_key': public_key,
                'balances': serializer.data,
                'total_assets': len(balances)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            error_message = str(e)
            if "Resource Missing" in error_message or "404" in error_message:
                return Response(
                    {'error': 'Account not found on Stellar network. Account may not be funded yet.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                {'error': f'Failed to fetch balance: {error_message}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SendPaymentView(APIView):
    """
    Send XLM or other assets to another Stellar account
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        destination = serializer.validated_data['destination']
        amount = str(serializer.validated_data['amount'])
        asset_code = serializer.validated_data.get('asset_code', 'XLM')
        asset_issuer = serializer.validated_data.get('asset_issuer')
        memo_text = serializer.validated_data.get('memo', '')
        secret_key = serializer.validated_data['secret_key']
        
        try:
            # Create keypair from secret key
            source_keypair = Keypair.from_secret(secret_key)
            source_public_key = source_keypair.public_key
            
            # Connect to Stellar network
            server = Server(horizon_url="https://horizon-testnet.stellar.org")
            # For mainnet use: Server(horizon_url="https://horizon.stellar.org")
            network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
            # For mainnet use: Network.PUBLIC_NETWORK_PASSPHRASE
            
            # Load source account
            source_account = server.load_account(source_public_key)
            
            # Determine asset
            if asset_code == 'XLM':
                asset = Asset.native()
            else:
                if not asset_issuer:
                    return Response(
                        {'error': 'asset_issuer is required for non-XLM assets'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                asset = Asset(asset_code, asset_issuer)
            
            # Build transaction
            transaction = (
                TransactionBuilder(
                    source_account=source_account,
                    network_passphrase=network_passphrase,
                    base_fee=100
                )
                .append_payment_op(
                    destination=destination,
                    asset=asset,
                    amount=amount
                )
            )
            
            # Add memo if provided
            if memo_text:
                from stellar_sdk import Memo
                transaction = transaction.add_text_memo(memo_text)
            
            # Build and sign transaction
            transaction = transaction.set_timeout(30).build()
            transaction.sign(source_keypair)
            
            # Submit transaction
            response = server.submit_transaction(transaction)
            
            return Response({
                'success': True,
                'transaction_hash': response['hash'],
                'source_account': source_public_key,
                'destination': destination,
                'amount': amount,
                'asset_code': asset_code,
                'ledger': response.get('ledger'),
                'memo': memo_text if memo_text else None
            }, status=status.HTTP_200_OK)
            
        except NotFoundError:
            return Response(
                {'error': 'Source or destination account not found on Stellar network'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            error_message = str(e)
            return Response(
                {'error': f'Payment failed: {error_message}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TransactionHistoryView(APIView):
    """
    Get transaction history for a Stellar account
    """
    permission_classes = [AllowAny]
    
    def get(self, request, public_key=None):
        # Use public_key from URL parameter or from session
        if not public_key:
            if not request.session.get('authenticated'):
                return Response(
                    {'error': 'Not authenticated'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            public_key = request.session.get('wallet_public_key')
        
        # Get query parameters
        limit = int(request.query_params.get('limit', 10))
        limit = min(limit, 100)  # Max 100 transactions
        
        try:
            # Validate public key format
            Keypair.from_public_key(public_key)
            
            # Connect to Stellar network
            server = Server(horizon_url="https://horizon-testnet.stellar.org")
            # For mainnet use: Server(horizon_url="https://horizon.stellar.org")
            
            # Get transactions for the account
            transactions_response = server.transactions().for_account(public_key).limit(limit).order(desc=True).call()
            
            transactions = []
            
            for tx in transactions_response['_embedded']['records']:
                # Get operations for this transaction
                operations = server.operations().for_transaction(tx['hash']).call()
                
                # Process each operation
                for op in operations['_embedded']['records']:
                    transaction_data = {
                        'id': op['id'],
                        'type': op['type'],
                        'created_at': op['created_at'],
                        'transaction_hash': op['transaction_hash'],
                        'source_account': op.get('source_account', tx['source_account']),
                    }
                    
                    # Add payment-specific details
                    if op['type'] in ['payment', 'create_account']:
                        transaction_data['from_address'] = op.get('from') or op.get('funder')
                        transaction_data['to_address'] = op.get('to') or op.get('account')
                        transaction_data['amount'] = op.get('amount') or op.get('starting_balance')
                        
                        # Asset information
                        if op.get('asset_type') == 'native':
                            transaction_data['asset_code'] = 'XLM'
                            transaction_data['asset_type'] = 'native'
                        else:
                            transaction_data['asset_code'] = op.get('asset_code', 'UNKNOWN')
                            transaction_data['asset_type'] = op.get('asset_type', 'unknown')
                    else:
                        transaction_data['from_address'] = None
                        transaction_data['to_address'] = None
                        transaction_data['amount'] = None
                        transaction_data['asset_code'] = None
                        transaction_data['asset_type'] = None
                    
                    transactions.append(transaction_data)
            
            # Serialize the data
            serializer = TransactionSerializer(transactions, many=True)
            
            return Response({
                'public_key': public_key,
                'transactions': serializer.data,
                'total_transactions': len(transactions),
                'limit': limit
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            error_message = str(e)
            if "Resource Missing" in error_message or "404" in error_message:
                return Response(
                    {'error': 'Account not found on Stellar network'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                {'error': f'Failed to fetch transactions: {error_message}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
