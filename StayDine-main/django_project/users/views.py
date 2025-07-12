import stripe
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
# from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PaymentForm
from .models import Payment
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core import signing
from django.http import HttpResponseBadRequest
# import razorpay

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('profile')  # redirect if user is already logged in

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form, 'title': 'Registration'})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been Updated!')
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents logout
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def email_redirect_view(request):
    messages.error(request, "You can't access the email management page.")
    return redirect('staydine-home')   


@login_required
def initiate_payment(request):
    signed_data = request.GET.get('data')
    if not signed_data:
        return HttpResponseBadRequest("Invalid request: Missing payment data.")

    try:
        data = signing.loads(signed_data)
        amount = data['amount']
        item_no = data.get('item_no')
        quantity = data.get('quantity')
        email = data.get('email')
    except signing.BadSignature:
        return HttpResponseBadRequest("Tampering detected in payment data.")

    # Just display the amount and order info
    return render(request, 'users/payment_instruction.html', {
        'amount': amount,
        'item_no': item_no,
        'quantity': quantity,
        'email': email,
    })



# using razopay
# @login_required
# def initiate_payment(request):
#     signed_data = request.GET.get('data')

#     try:
#         data = signing.loads(signed_data)
#         amount = int(float(data['amount']) * 100)  # Convert to paise
#         receipt = data['receipt']
#     except signing.BadSignature:
#         messages.error(request, "Invalid payment link.")
#         return redirect('staydine-restaurant')

#     razorpay_order = client.order.create({
#         'amount': amount,
#         'currency': 'INR',
#         'payment_capture': 1,
#         'receipt': receipt
#     })

#     return render(request, 'users/upi_payment.html', {
#         'order_id': razorpay_order['id'],
#         'amount': amount,
#         'razorpay_key_id': settings.RAZORPAY_KEY_ID,
#         'user': request.user
#     })
# @csrf_exempt
# def verify_payment(request):
#     if request.method == 'POST':
#         import json
#         data = json.loads(request.body)

#         # Required fields
#         razorpay_order_id = data.get('razorpay_order_id')
#         razorpay_payment_id = data.get('razorpay_payment_id')
#         razorpay_signature = data.get('razorpay_signature')

#         params_dict = {
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': razorpay_payment_id,
#             'razorpay_signature': razorpay_signature
#         }

#         try:
#             # Signature verification
#             client.utility.verify_payment_signature(params_dict)

#             # ✅ Save payment info or mark as paid in your DB
#             # Payment.objects.create(...)  # optional

#             return JsonResponse({'status': 'success'})
#         except errors.SignatureVerificationError:
#             return JsonResponse({'status': 'failed', 'reason': 'Signature mismatch'})

#     return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  
        user.delete()    
        messages.success(request, 'Your account has been deleted.')
        return redirect('login') 

def payment_success(request):
    transaction_id = request.GET.get('transaction_id')
    if transaction_id:
        payment = Payment.objects.filter(transaction_id=transaction_id).first()
        if payment:
            payment.status = 'Completed'
            payment.save()
            messages.success(request, "Payment was successful!")
    return render(request, 'users/payment_success.html')

def payment_confirm(request):
    return render(request, 'users/payment_confirm.html', {'title': 'Confirmation Page'})


