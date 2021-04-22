from django.core.management.base import BaseCommand
from django.utils import timezone

from product.models.Subcategory import Subcategory
from product.models.category import Category
from product.models.products import Product
from product.models.store import Store


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        import requests

        # api-endpoint
        URL = "http://213.136.68.196:809/api/values/Getrecord/9999"

        data_responce = requests.get(url=URL).json()

        # print(data_responce['Table'])

        for qs in data_responce['Table']:
            print(qs['ItemCode'])
            try:
                # store = Store.objects.get(store_name=qs['OutletName_vch'])
                store = Store.objects.get(store_name="THE QUICK FORK")
            except Exception as ex:
                print(ex)
                store = Store.objects.create(store_name=qs['OutletName_vch'], city="test", state="test",
                                             address="test", storeId=int(qs['pk_OutletGUID_num']))

            if qs['MainHead'] == "RAW FOOD":

                try:
                    category = Category.objects.get(name=qs['CategoryName'])
                except Exception as ex:
                    print(ex)
                    category = Category.objects.create(name=qs['CategoryName'])

                product = Product.objects.filter(name=qs['ItemName']).first()

                print(product)
                if store.store_name == "THE QUICK FORK" and qs['OutletName_vch'] == "THE QUICK FORK":
                    if product:
                        Product.objects.create(name=qs['ItemName'], category=category, description=product.description,
                                               price=qs['ItemPrice'], quantity_type=qs['ItemType'],
                                               product_code=int(qs['ItemCode']), productUsage=product.productUsage,
                                               default_image=product.default_image, store=store,
                                               quantity=product.quantity,
                                               )
                    else:
                        Product.objects.create(name=qs['ItemName'], category=category, description="test",
                                               price=qs['ItemPrice'], quantity_type=qs['ItemType'],
                                               product_code=int(qs['ItemCode']), productUsage="test",
                                               store=store
                                               )
                else:
                    pass

            if qs['CategoryName'] == qs['MainHead']:
                if qs['MainHead'] == "CHUTNEY_SAUCES":
                    name = "Chutney & Spices"
                else:
                    name = qs['MainHead']
                try:
                    category = Category.objects.get(name=name)
                except Exception as ex:
                    print(ex)
                    category = Category.objects.create(name=name)

                product = Product.objects.filter(name=qs['ItemName']).first()

                print(product)
                if store.store_name == "THE QUICK FORK" and qs['OutletName_vch'] == "THE QUICK FORK":
                    if product:
                        Product.objects.create(name=qs['ItemName'], category=category, description=product.description,
                                               price=qs['ItemPrice'], quantity_type=qs['ItemType'],
                                               product_code=int(qs['ItemCode']), productUsage=product.productUsage,
                                               default_image=product.default_image, store=store,
                                               quantity=product.quantity,
                                               )
                    else:
                        Product.objects.create(name=qs['ItemName'], category=category, description="test",
                                               price=qs['ItemPrice'], quantity_type=qs['ItemType'],
                                               product_code=int(qs['ItemCode']), productUsage="test",
                                               store=store
                                               )
                else:
                    pass

            if qs['CategoryName'] != qs['MainHead']:
                if qs['MainHead'] == "CHUTNEY_SAUCES":
                    name = "Chutney & Spices"
                else:
                    name = qs['MainHead']
                try:
                    category = Category.objects.get(name=name)
                except Exception as ex:
                    print(ex)
                    category = Category.objects.create(name=name)

                try:
                    subcategory = Subcategory.objects.get(name=qs['CategoryName'], category=category)
                except Exception as ex:
                    print(ex)
                    subcategory = Subcategory.objects.create(name=qs['CategoryName'], category=category)

                product = Product.objects.filter(name=qs['ItemName']).first()

                print(product)
                if store.store_name == "THE QUICK FORK" and qs['OutletName_vch'] == "THE QUICK FORK":
                    if product:
                        Product.objects.create(name=qs['ItemName'], category=category, description=product.description,
                                               price=qs['ItemPrice'], quantity_type=qs['ItemType'],
                                               product_code=int(qs['ItemCode']), productUsage=product.productUsage,
                                               default_image=product.default_image, store=store,
                                               quantity=product.quantity, subcategory=subcategory,
                                               )
                    else:
                        Product.objects.create(name=qs['ItemName'], category=category, description="test",
                                               price=qs['ItemPrice'], quantity_type=qs['ItemType'],
                                               product_code=int(qs['ItemCode']), productUsage="test",
                                               store=store, subcategory=subcategory,
                                               )
                else:
                    pass

        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)