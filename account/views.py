from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm,CheckoutEditForm
from .models import Profile
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from product.models import Order,Product,OrderItem,Checkout
from django.core.exceptions import ObjectDoesNotExist
import json
from .filters import OrderItemFilter,UserFilter

# Create your views here.



@login_required
def dashbord(request):
    
    try:
        order = OrderItem.objects.filter(user=request.user,ordered=True)
        profile = Profile.objects.get(user=request.user)
        checkout = Checkout.objects.filter(user=request.user)
        
        context= {
            
            'object':order,
            'profile':profile,
            'address':checkout,
            'section':'dashboard'
        }
        
        return render(request,'account/dashboard.html', context)
    except ObjectDoesNotExist:
        return render(request,
        'account/dashboard.html',{
            'section':'dashboard',
        
            
        })



# def register(request):
#     cart = request.COOKIES.get('cart')
#     print(cart)
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(
#                 user_form.cleaned_data['password']
#             )
#             new_user.save()
#             return render(request,'account/register_done.html',{
#                 'new_user':new_user
#             })
#     else:
#         user_form = UserRegistrationForm()
#     return render(request,'account/register.html',{
#         'user_form':user_form
#     })

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account/acc_active_email.html',{
                'user':user,
                
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject,message,to=[to_email])
            email.send()
            return render(request,'registration/confirm.html')
    else:
        form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form':form})


def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request,'Your account has been created.')
        return redirect('/')
    else:
        return render(request,'account/acc_active_email.html',{'uidb64':uidb64,'token':token})


@login_required
def edit(request):
    profile = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile updated Successfully!!!')
            return redirect('/account/profile/')
            
        
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request,'account/edit.html',{
        'user_form':user_form,
        'profile_form':profile_form,
    })
@login_required
def a_edit(request):
    checkout = Checkout.objects.get_or_create(user=request.user)
    if request.method =="POST":
        a_fom = CheckoutEditForm(instance=request.user.checkout,data=request.POST)
        if a_fom.is_valid():
            a_fom.save()
            messages.success(request,'Address updated !!!')
            return redirect('/account/profile/')
    else:
        a_fom = CheckoutEditForm(instance=request.user.checkout)
    return render(request,'account/address.html',{'a_form':a_fom})


def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                    username=cd['username'],
                    password=cd['password'])
            if user is not None:
                if user.is_active and user.is_staff:
                    login(request, user)
                    return redirect('admin-home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'adminpages/admin_login.html', {'form': form})

@login_required
def admin_home(request):
    orders = OrderItem.objects.all()
    myfilter = OrderItemFilter(request.GET,queryset=orders)
    orders = myfilter.qs
    context = {
        'object':orders,
        'myfilter':myfilter
    }
    return render(request,'adminpages/admin_home.html',context)

@login_required
def admin_order_detail(request,id):
    orders = OrderItem.objects.filter(pk=id)
   
    context = {
        'object':orders
    }
    return render(request,'adminpages/order_detail.html',context)


@login_required
def user_list(request):
    users = Profile.objects.all()
    search = User.objects.all()
    myfilter = UserFilter(request.GET,queryset=search)
    search = myfilter.qs
    context = {
        'users':users,
        'search':search,
        'myfilter':myfilter
    }
    return render(request,'adminpages/staff_list.html',context)

@login_required
def user_detail(request,id):
    user = User.objects.filter(pk=id)
    profile = Profile.objects.filter(user__in=user)
    address = Checkout.objects.filter(user__in=user)
    context = {
        'user':user,
        'profile':profile,
        'address':address
    }
    return render(request,'adminpages/user_detail.html',context)


def contact(request):
    return  render(request,'contact.html')

