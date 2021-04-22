from django.conf.urls import url
from django.urls import path, include

from product.api.Category_like_api import Category_like_ViewSet
from product.api.Coupon_api import Coupon_View, apply_Coupon_View
from product.api.Franchisses_api import franchissesApi, franchissesGet
from product.api.Order_api import Order_View, Transaction_views, Update_status_View, user_order_views, \
    get_order_id_ListView, store_order_list_views
from product.api.Rating_api import rating_ViewSet, Review_ViewSet, Rating_count_View, Rating_get_count_View
from product.api.Subcategory_like_api import Subcategory_like_ViewSet
from product.api.address_api import Address_View, Update_Address_View, Get_Address_View
from product.api.booklet_api import Booklet_View, get_Booklet_View, delete_Booklet_View
from product.api.contact_api import Contact_ViewSet, Career_ViewSet
from product.api.demo_product import DemoProducts, DemoTrendingProducts, Time, DemoProductFilter
from product.api.graph_api import get_user_View, get_user_day_View, get_order_month_View, get_order_day_View, \
    store_order_month_View, store_order_day_View, tranding_order_count_View, pending_order_View, today_order_View, \
    month_revenue_View, day_revenue_View, store_revenue_month_View, store_day_revenue_View, StoreMonthSaleView
from product.api.map_api import g_map_View
from product.api.paytm_pay_api import PaytemProductView, StatusPaytemProductView, CallBackView
from product.api.paytm_refund import PaytmRefund
from product.api.pos_api import PosTaxGet, PosCatGet, PosProductPost
from product.api.product_api import ProductListView, productDetailView, addproductView, UpdateproductView, \
    delete_productView, AdminProductListView, store_ProductListView, store_product_updateView, tranding_ListView, \
    PosProductProductView, PosEnableProductView, TrandingStoreListView
from product.api.Subcategory_api import SubcategoryViewSet
from product.api.category_api import CategoryViewSet
from product.api.add_to_cart_api import AddToCartView, cartView, delete_cartView, cart_update_View
from product.api.header_image_api import header_imageViewSet
from rest_framework.routers import DefaultRouter

from product.api.store_api import get_store_View

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('Subcategory', SubcategoryViewSet, basename='Subcategory')
router.register('Banner-images', header_imageViewSet, basename='Banner-images')
router.register('store', get_store_View, basename='store')
router.register('rating', rating_ViewSet, basename='rating')
router.register('Review', Review_ViewSet, basename='Review')
router.register('Contact', Contact_ViewSet, basename='Contact')
router.register('Career', Career_ViewSet, basename='Career')


urlpatterns = [
    path('', include(router.urls)),
    path('products-list/',ProductListView.as_view()),
    path('admin-products-list/', AdminProductListView.as_view()),
    path('products-detial/<pk>',productDetailView.as_view()),
    path('add-products/',addproductView.as_view()),
    path('Update-products/<pk>', UpdateproductView.as_view()),
    path('products-delete/<pk>',delete_productView.as_view()),
    path('add-to-cart/', AddToCartView.as_view()),
    path('cart-view/<store_id>', cartView.as_view()),

    path('cart-delete/<pk>',delete_cartView.as_view()),
    path('franchisses/',franchissesApi.as_view()),
    path('franchisses/<pk>', franchissesGet.as_view()),
    path('Order/', Order_View.as_view()),
    path('Order-Status/<pk>', Update_status_View.as_view()),
    path('address/', Address_View.as_view()),
    path('address-List/', Get_Address_View.as_view()),
    path('address-update/<pk>', Update_Address_View.as_view()),
    path('Category-like/', Category_like_ViewSet.as_view()),
    path('cart-update/<pk>', cart_update_View.as_view()),
    path('Transaction-Callback/', Transaction_views.as_view()),
    path('Booklet/', Booklet_View.as_view()),
    path('Booklet-list/', get_Booklet_View.as_view()),
    path('Booklet-delete/<perfix>', delete_Booklet_View.as_view()),
    path('user-order/', user_order_views.as_view()),
    path('store-product-list/', store_ProductListView.as_view()),
    path('store-product/<pk>', store_product_updateView.as_view()),
    path('Rating-count/<product_id>/<star>', Rating_count_View.as_view()),
    path('user-order/<pk>', get_order_id_ListView.as_view()),
    path('Tranding-Products/', tranding_ListView.as_view()),
    path('Coupon/', Coupon_View.as_view()),
    path('Coupon-Apply/', apply_Coupon_View.as_view()),

    path('User-Count/Month', get_user_View.as_view()),
    path('User-Count/day', get_user_day_View.as_view()),
    path('Order-Count/Month', get_order_month_View.as_view()),
    path('Order-Count/day', get_order_day_View.as_view()),
    path('Store-Count/Month/<pk>', store_order_month_View.as_view()),
    path('Store-Count/day/<pk>', store_order_day_View.as_view()),
    path('Tranding-Order-Count/', tranding_order_count_View.as_view()),
    path('Pending-Order/', pending_order_View.as_view()),
    path('Today-Order/', today_order_View.as_view()),
    path('Monthly-Revenue/', month_revenue_View.as_view()),
    path('Day-Revenue/', day_revenue_View.as_view()),
    path('Store-Month-Revenue/', store_revenue_month_View.as_view()),
    path('Store-Day-Revenue/', store_day_revenue_View.as_view()),

    path('Google-map/', g_map_View.as_view()),
    path('Store-Order-list/', store_order_list_views.as_view()),
    path('Rating-Products/<product_id>', Rating_get_count_View.as_view()),
    path('product-update-pos', PosProductProductView.as_view()),
    path('product-disenable/<pk>', PosEnableProductView.as_view()),

    path('paytm-order', PaytemProductView.as_view()),
    path('callback', CallBackView.as_view()),
    path('paytem-status', StatusPaytemProductView.as_view()),

    path('store-tranding-product/<store_id>', TrandingStoreListView.as_view()),
    path('all-month-store-revenue', StoreMonthSaleView.as_view()),
    path('demo-products', DemoProducts.as_view()),
    path('demo-trending-products', DemoTrendingProducts.as_view()),
    path('time', Time.as_view()),
    path('demo-product-filter', DemoProductFilter.as_view()),
    path('cancel-order', PaytmRefund.as_view()),

    path('pos-tax', PosTaxGet.as_view()),
    path('pos-category', PosCatGet.as_view()),
    path('pos-product-create', PosProductPost.as_view()),
]