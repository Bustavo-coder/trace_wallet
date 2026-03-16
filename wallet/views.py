from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Wallet
from .serilizer import TransferSerializer, DepositSerializer
from service.transfer_service import create_transfer
from service.deposit_service import deposit_service
from service.fund_wallet_service import fund_wallet_onboard


# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_wallet(request):
    sender = request.user.wallet
    serializer = TransferSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    amount = serializer.validated_data['amount']
    idempotency_key = serializer.validated_data['idempotency_key']
    description = serializer.validated_data['description']
    receiver_wallet = serializer.validated_data['receiver_wallet']
    _receiver = get_object_or_404(Wallet, wallet_number=receiver_wallet)
    transaction = create_transfer(sender,_receiver,amount, idempotency_key,description)

    return Response({
        "amount" : transaction.amount,
        "status" : transaction.transaction_status,
        "reference" : transaction.reference,
        "description" : transaction.description,
        "created_at" : transaction.created_at,
    },status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_wallet(request):
    wallet = request.user.wallet
    serializer = DepositSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    amount = serializer.validated_data['amount']
    idempotency_key = serializer.validated_data['idempotency_key']
    transaction = deposit_service(wallet,amount,idempotency_key)
    return Response({
        "amount" : transaction.amount,
        "status" : transaction.transaction_status,
        "reference" : transaction.reference,
        "description" : transaction.description,
        "created_at" : transaction.created_at,
    },status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fund_wallet(request):
    serializer = DepositSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = request.user
    amount = serializer.validated_data['amount']
    payment = fund_wallet_onboard(user, amount)

    return Response(payment,status=status.HTTP_200_OK)

