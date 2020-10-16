import json
from .models import Product,Order,OrderItem

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('cart:',cart)
    items = []
    order = {'total_cart_price':0,  'total_cart_item':0,'ordered':False}
    cartItems = order['total_cart_item']
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total']+= total
            order['get_cart_items']+= cart[i]['quantity']
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
            items.append(item)

            
            
        except:
            pass

    return {
        'cartItems':cartItems,
        'order':order,
        'items':items,
        }


def cartData(request):
    if user.is_authenticated:
        user = request.user
        order,created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {
        'cartItems':cartItems,
        'order':order,
        'items':items,
        }