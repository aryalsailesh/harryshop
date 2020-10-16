from django.db import models
from django.conf import settings
from account.models import Profile
from django.shortcuts import reverse
from mptt.models import MPTTModel
from taggit.managers import TaggableManager
from treewidget.fields import TreeForeignKey,TreeManyToManyField

# Create your models here.

class Category(MPTTModel):
  name = models.CharField(max_length=50, unique=True)
  parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete=models.CASCADE)
  slug = models.SlugField()

  class MPTTMeta:
    order_insertion_by = ['name']

  class Meta:
    unique_together = (('parent', 'slug',))
    verbose_name_plural = 'categories'

  def get_slug_list(self):
    try:
      ancestors = self.get_ancestors(include_self=True)
    except:
      ancestors = []
    else:
      ancestors = [ i.slug for i in ancestors]
    slugs = []
    for i in range(len(ancestors)):
      slugs.append('/'.join(ancestors[:i+1]))
    return slugs

  def __str__(self):
    return self.name
    
    def get_absolute_url(self):
        return reverse('product:category',kwargs={
            'slug':self.slug
        })

class Product(models.Model):
    category = TreeManyToManyField(Category)
    tags = TaggableManager()
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    price = models.DecimalField(max_digits=20,decimal_places=2)
    image = models.ImageField(upload_to='product/%Y/%m/%d',blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    available_quantity = models.IntegerField()

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.name
    
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def get_absolute_url(self):
        return reverse('product:product-detail',args=[self.slug])
    
    def add_to_cart(self):
        return reverse('product:add-to-cart',kwargs={
            'slug':self.slug
        })
    
    def remove_from_cart(self):
        return reverse('product:remove-from-cart',kwargs={
            'slug':self.slug
        })
    
    def remove_single_item_from_cart(self):
        return reverse('product:remove-single-item-from-cart',kwargs={
            'slug':self.slug
        })

METHOD = (
    ('Cash on delivery', 'Cash on delivery'),
    ('esewa','esewa'),
)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    payment = models.CharField(max_length=50,choices=METHOD,null=True,blank=True)
    address = models.ForeignKey('Checkout',on_delete=models.CASCADE,null=True,blank=True)
    ordered_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-ordered_date']

    def __str__(self):
        return f'{self.quantity} of {self.product}'
    
    def get_total(self):
        return self.product.price * self.quantity
    
    def get_cart(self):
        return self.quantity
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment = models.CharField(max_length=50,choices=METHOD,default='Cash on delivery')
    
    def __str__(self):
        return self.user.username

    def total_cart_item(self):
        total = 0
        for order_product in self.order.all():
            total += order_product.get_cart()
        return total
    
    def total_cart_price(self):
        total = 0
        for order_product in self.order.all():
            total += order_product.get_total()
        return total

class Checkout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    appartment = models.CharField(max_length=50,blank=True,null=True) 
    tol = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    

    

    def __str__(self):
        return f'Checkout for user {self.user.username}'