from django.contrib import admin

# Register your models here.
from blog.models.blog import Blog
from product.models.Subcategory import Subcategory
from product.models.address import Address
from product.models.booklet import Booklet
from product.models.cart import Cart
from product.models.category import Category
from product.models.contact import Contact_us
from product.models.coupon import Coupon
from product.models.header_image import header_image
from product.models.order import Order, Transaction
from product.models.products import Product, Images
from product.models.message import SMS
from product.models.franchisses import Franchisses
from product.models.rating import Rating, Review
from product.models.store import Store

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Cart)
admin.site.register(header_image)
admin.site.register(SMS)
admin.site.register(Franchisses)
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(Images)
admin.site.register(Address)
admin.site.register(Booklet)
admin.site.register(Transaction)
admin.site.register(Store)
admin.site.register(Blog)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Contact_us)

