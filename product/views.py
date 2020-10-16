from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CheckoutForm,SearchForm,OrderForm
from django.views.generic import ListView,DetailView,View
from .models import Checkout,Product,Order,OrderItem,Profile,Category
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
import json
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
import requests 
from .filters import ProductFilter


# Create your views here.

# class ProductListView(ListView):
#     template_name = 'product/home.html'
    
#     def get(self,request,category_slug=None,tag_slug=None):
#         category = None
#         tag = None
#         categories = Category.objects.all()
#         categories = categories.filter(parent=None)
#         products = Product.objects.filter(available=True)
#         if category_slug:
#             category = get_object_or_404(Category,slug=category_slug)
#             products = products.filter(category=category)
        
#         if tag_slug:
#             tag = get_object_or_404(Tag,slug=tag_slug)
#             products = products.filter(tags__in=[tag])
        
        
        
#         return render(
#             request,'product/home.html',{
#                 'category':category,
#                 'categories':categories,
#                 'products':products,
#                 'tag':tag,
                
#             }
#         )

def homepage(request):
    context = {

    }
    return render(request,'homepage.html',context)

def product_list(request,category_slug=None,tag_slug=None):
    category = None
    tag = None
    categories = Category.objects.all()
    categories = categories.filter(parent=None)
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
    
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        products = products.filter(tags__in=[tag])
    
    
    myfilter = ProductFilter(request.GET, queryset=products)
    products = myfilter.qs

    paginator = Paginator(products,12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    

    

    return render(
        request,'product/home.html',{
            'category':category,
            'categories':categories,
            'products':products,
            'tag':tag,
            'page':page,
            'myfilter':myfilter
            
        }
    )

# class ProductDetailView(DetailView):
#     def get(self,request,slug,*args,**kwargs):
#         products = get_object_or_404(Product,slug=slug)
#         context = {
#             'products':products,
#         }
#         return render(request,'product/product.html',context)

def product_detail(request,slug):
    products = get_object_or_404(Product,slug=slug)
    products_tags_ids = products.tags.values_list('id',flat=True)
    similar_products = Product.objects.filter(tags__in=products_tags_ids).exclude(id=products.id)
    similar_products = similar_products.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]

    context = {
        'products': products,
        'similar_products':similar_products,
    }
    return render(request,'product/product.html',context)



def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)

    try:
        instance = Category.objects.get(parent=parent,slug=category_slug[-1])
    except:
        instance = get_object_or_404(Product, slug = category_slug[-1])
        return render(request, "product/product.html", {'instance':instance})
    else:
        return render(request, 'product/categories.html', {'instance':instance})
 


def search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.annotate(search=SearchVector('name','description'),).filter(search=query)
    return render(request,'product/search.html',{
        'query':query,
        'form':form,
        'results':results,
    })


def add_to_cart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    order_items,created = OrderItem.objects.get_or_create(user=request.user,ordered=False,product=product)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        orders = order_qs[0]
        if orders.order.filter(product__slug=product.slug).exists():
            order_items.quantity += 1
            order_items.save()
            return redirect('product:cart')
            
        else:
            orders.order.add(order_items)
            if order_items.quantity <= 0:
                order_items.quantity += 1
                
                order_items.save()
                return redirect('product:cart')

                
            
    else:
        order_date = timezone.now()
        orders = Order.objects.create(user=request.user,ordered=False)
        orders.order.add(order_items)
        messages.info(request,'Item Added to cart.')
    
    return redirect('product:cart')


def remove_from_cart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    order_items = OrderItem.objects.filter(user=request.user,ordered=False,product=product)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        orders = order_qs[0]
        if orders.order.filter(product__slug=product.slug).exists():
            order_items = OrderItem.objects.filter(user=request.user,product=product)[0]
            if order_items.quantity  >= 1:
                order_items.delete()
                return redirect('product:product-detail',slug=slug)
        else:
            messages.info(request,'You don\'t have any Items in cart.')
            return redirect('product:product-detail',slug=slug)
    else:
            messages.info(request,'You don\'t have any Items in cart.')
            return redirect('product:product-detail',slug=slug)
                       

def remove_single_item_from_cart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    order_items = OrderItem.objects.filter(user=request.user,ordered=False,product=product)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        orders = order_qs[0]
        if orders.order.filter(product__slug=product.slug).exists():
            order_items = OrderItem.objects.filter(user=request.user,ordered=False,product=product)[0]
            if order_items.quantity > 1:
                order_items.quantity -= 1
                order_items.save()
                messages.info(request,'Order items is reduced by One')
                return redirect('product:cart')
            if order_items.quantity == 1:
                order_items.delete()
                messages.info(request,'All the item in cart has been removed.')
                return redirect('product:cart')
        else:
            return redirect('/cart/')

class CartView(View):
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            
            try:
                value = self.request.COOKIES.get('cart')
                orders = Order.objects.get(user=self.request.user,ordered=False)
                
                
                context = {
                    'object':orders,
                    'value':value,
                }
                return render(self.request,'product/cart.html',context)
            except ObjectDoesNotExist:
                messages.info(self.request,'You don\'t have any items in your cart. Add some products to the cart.')
                return render(self.request,'product/cart.html')
            
        else:
            try:
                cart = json.loads(self.request.COOKIES['cart'])
                
            except:
                cart = {}
            print(cart)
            item = []
            grand_total = 0
            cart_items = 0
            for i,j in cart.items():
                product = Product.objects.get(id=i)
                total = product.price * j['quantity']
                cart_items += cart[i]['quantity']

                products = {
                    'product': {
                        'id':product.id,
                        'slug':product.slug,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL,

                    },
                    'quantity':j['quantity'],
                    'get_total':total,
                }
                grand_total += total
                
                item.append(products)
                


           
            return render(self.request,'product/cart.html',{
                'items': item,
                'grand_total': grand_total,
                'cart_items':cart_items

            })


@login_required
def chekout(request):
    
    checkout = Checkout.objects.get_or_create(user=request.user)
    try:
        orders = Order.objects.get(user=request.user,ordered=False)
    except ObjectDoesNotExist:
        messages.error(request,'You don\'t have item in your cart')
        return redirect('/')
    if request.method == 'POST' and orders.order.exists():
        form = CheckoutForm(data=request.POST,instance=request.user.checkout)
        p_form = OrderForm(data=request.POST)
        
        if form.is_valid() and p_form.is_valid():
            pm = p_form.cleaned_data.get('payment')
            form.save()

            if pm == 'esewa':
                return redirect(reverse('product:esewa-request') + "?o_id=" + str(orders.id))
            else:
                orders.ordered = True
                order_items = orders.order.all()
                order_items.update(ordered=True,payment='Cash on delivery',address=request.user.checkout)
                for item in order_items:
                    item.save()
                orders.save()
                messages.success(request,'Your order has been placed and will be delivered very soon.')
                return redirect('/')
    else:
        form = CheckoutForm(instance=request.user.checkout)
        p_form = OrderForm()
    return render(request,'product/checkout.html',{
        'form':form,
        'p_form':p_form,
        'orders':orders
    })

class Esewa(View):
    def get(self,*args, **kwargs):
        o_id = self.request.GET.get('o_id')
        orders = Order.objects.get(id=o_id)

        context = {
            'orders':orders
        }
        return render(self.request,'product/esewarequest.html',context)

class EsewaVerify(View):
    def get(self,request,*args,**kwargs):
        import xml.etree.ElementTree as ET
        oid = request.GET.get('oid')
        amt = request.GET.get('amt')
        refId = request.GET.get('refId')
        

        url ="https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'epay_payment',
            'rid': refId,
            'pid':oid,
        }
        resp = requests.post(url, d)
        root = ET.fromstring(resp.content)
        status = root[0].text.strip()
        print(status)
        if status == 'Success':
            orders = Order.objects.get(user=request.user,ordered=False)
            checkout = Checkout.objects.get(user=request.user)
            orders.ordered = True
            orders.payment = 'esewa'
            order_items = orders.order.all()
            order_items.update(ordered=True,payment='esewa',address=request.user.checkout)
            for item in order_items:
                item.save()
            orders.save()
            messages.success(request,'Order has been placed and will be shipped soon !!!')
            return redirect('/')
        else:
            
            messages.error(request,'Payment is not successful and order has not been placed.')
            return redirect('/cart/')

def add_to_database(request):
     
    try:
        cart = json.loads(request.COOKIES['cart'])
    except ObjectDoesNotExist:
        cart = {}
                
    print(cart)
    items = []
    order = {'total_cart_price':0,  'total_cart_item':0,'ordered':False}
    cartItems = order['total_cart_item']
    for i in cart:
        
        
        product = Product.objects.get(id=i)
        total = (product.price * cart[i]['quantity'])
        cartItems += cart[i]['quantity']

        order['total_cart_price']+= total
        order['total_cart_item']+= cart[i]['quantity']
        item = {
            'product':{
                'id':product.id,
                'slug':product.slug,
                'name':product.name,
                'price':product.price,
                'imageURL':product.imageURL,
                },
            'quantity':cart[i]['quantity'],
            'get_total':total,
            }
        items.append(item)
        
        
    return redirect('/product/checkout/',{
        'items':items,
        'cartItems':cartItems,
        'order':order,
    })


