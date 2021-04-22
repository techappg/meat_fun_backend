from django.urls import path

from storeheaderimages.api.store_header_images_api import *

urlpatterns = [
    path('store-header-image', StoreHeaderImages.as_view()),
    path('store-header/<storeid>', StoreHeaderImagesGet.as_view()),
    path('store-header-delete/<pk>', StoreHeaderImagesDelete.as_view()),
    path('store-header-read/<pk>', StoreHeaderImagesRead.as_view()),
    path('store-header-Patch/<pk>', StoreHeaderImagesPatch.as_view()),
    path('hared-images/randem', StoreHeaderImagesRandem.as_view()),
]
