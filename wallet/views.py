from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notification.services import create_transfer_notification
from .models import Wallet
from .serilizer import TransferSerializer, DepositSerializer
from .service.deposit_service import deposit
from .service.intra_transfer_service import intra_transfer
from service.transfer_service import create_transfer


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
    idempotency_key =serializer.validated_data['idempotency_key']
    transaction = deposit(wallet,amount,idempotency_key)
    create_transfer_notification(request.user,amount)
    return Response({
        "amount" : transaction.amount,
        "status" : transaction.transaction_status,
        "reference" : transaction.reference,
        "description" : transaction.description,
        "created_at" : transaction.created_at,
    },status.HTTP_200_OK)

