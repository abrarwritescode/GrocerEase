
from django.http import JsonResponse
from projects.imports import *

def check_voucher(request):
    vouchercode = request.GET.get('vouchercode', '')
    try:
        voucher = VoucherCode.objects.get(vouchercode=vouchercode)
        discount_percentage = voucher.voucher_percentage
        return JsonResponse({'valid': True, 'voucher_percentage': voucher.voucher_percentage})
    except VoucherCode.DoesNotExist:
        return JsonResponse({'valid': False})
