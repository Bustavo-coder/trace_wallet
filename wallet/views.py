from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notification.services import create_transfer_notification
from .models import Wallet
from .serilizer import TransferSerializer
from .service.intra_transfer_service import intra_transfer


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
    _receiver = get_object_or_404(Wallet, wallet_number=receiver_wallet.wallet_number)
    transaction = intra_transfer(sender,_receiver,amount, idempotency_key,description)
    create_transfer_notification(receiver_wallet.user,amount)

    return Response({
        "amount" : transaction.amount,
        "status" : transaction.transaction_status,
        "reference" : transaction.reference,
        "description" : transaction.description,
        "created_at" : transaction.created_at,
    },status.HTTP_200_OK)
