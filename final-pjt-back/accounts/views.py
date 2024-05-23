from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm, CustomUserCreationForm
from finlife.models import DepositProducts, SavingProducts

# from .forms import UserForm


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('mainpage:mainpage')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('mainpage:mainpage')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('mainpage:mainpage')


def signup(request):
    if request.user.is_authenticated:
        return redirect('mainpage:mainpage')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mainpage:mainpage')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def delete(request):
    request.user.delete()
    return redirect('mainpage:mainpage')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mainpage:mainpage')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
        # 'user_pk': request.user.pk,  # 현재 로그인된 사용자의 pk를 컨텍스트에 추가
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('mainpage:mainpage')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


@login_required
def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    enrolled_deposit_products = person.enrolled_deposit_products.all()
    enrolled_saving_products = person.enrolled_saving_products.all()
    
    context = {
        'person': person,
        'enrolled_deposit_products': enrolled_deposit_products,
        'enrolled_saving_products': enrolled_saving_products,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def compare_products(request):
    deposit_product_ids = request.POST.getlist('deposit_products')
    saving_product_ids = request.POST.getlist('saving_products')

    deposit_products = DepositProducts.objects.filter(id__in=deposit_product_ids)
    saving_products = SavingProducts.objects.filter(id__in=saving_product_ids)

    context = {
        'deposit_products': deposit_products,
        'saving_products': saving_products,
    }
    return render(request, 'accounts/compare.html', context)
