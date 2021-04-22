from docutils.nodes import status
from requests import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from product.models.cart import Cart
from product.models.coupon import Coupon
from product.models.order import Order
from product.models.store import Store
from product.serializer.copon_serializer import coupon_Serializer, apply_coupon_Serializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


class Coupon_View(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = coupon_Serializer

    def post(self, request, format=None):
        serializer = coupon_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = self.request.user
        order = Order.objects.filter(user=user, order_status=True).values('coupon')
        coupon = Coupon.objects.filter()
        # number_of_coupon
        serializer = coupon_Serializer(coupon, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class apply_Coupon_View(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = apply_coupon_Serializer

    def post(self, request, format=None):
        serializer = apply_coupon_Serializer(data=request.data)
        user = self.request.user
        if serializer.is_valid():
            coupon = serializer.data.get('add_coupon')
            try:
                code = Coupon.objects.get(coupon_code=coupon)
            except:
                return_response = dict()
                data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "massage": "Coupon dose not exists",
                }
                return_response['data'] = data
                return Response(return_response, status.HTTP_400_BAD_REQUEST)

            cart = Cart.objects.filter(user=user, ordered=False)
            total = 0

            for t in cart:
                total += t.get_final_amount()
                print(t.get_final_amount())

            real_amount = int(total)

            if cart is None:
                return_response = dict()
                data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "massage": "Cart Is None",
                }
                return_response['data'] = data
                return Response(return_response, status.HTTP_400_BAD_REQUEST)

            count_coupon = Order.objects.filter(user=user, order_status=True, coupon=code).count()

            if code.minimum_amount >= real_amount:
                print(code.minimum_amount)
                return_response = dict()
                data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "massage": "amount less then min amount",
                }
                return_response['data'] = data
                return Response(return_response, status.HTTP_400_BAD_REQUEST)

            if code.number_of_coupon == count_coupon:
                return_response = dict()
                data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "massage": "All coupon are used",
                }
                return_response['data'] = data
                return Response(return_response, status.HTTP_400_BAD_REQUEST)

            if code.product_master_key:

                for ss in cart:
                    if ss.item.master_key == code.product_master_key:
                        pass
                    else:
                        return_response = dict()
                        data = {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "massage": " Not applicable all product ",
                        }
                        return_response['data'] = data
                        return Response(return_response, status.HTTP_400_BAD_REQUEST)

                if code.discount_amount:
                    dis = real_amount - code.discount_amount
                    final_response = dict()
                    data = {
                        "status": "add successfully",
                        "coupon": coupon,
                        "amount": real_amount,
                        "discount": code.discount_amount,
                        "total": dis,
                    }
                    final_response['data'] = data

                    return Response(final_response, status.HTTP_200_OK)

                if code.discount_percent:
                    dis = code.discount_percent / 100
                    final = int(dis * real_amount)
                    total = real_amount - final
                    final_response = dict()
                    data = {
                        "status": "add successfully",
                        "coupon": coupon,
                        "amount": real_amount,
                        "discount": final,
                        "total": total,
                    }
                    final_response['data'] = data

                    return Response(final_response, status.HTTP_200_OK)
                else:
                    return_response = dict()
                    data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "massage": "somethings went wrong",
                    }
                    return_response['data'] = data
                    return Response(return_response, status.HTTP_400_BAD_REQUEST)

            if code.category:

                for ss in cart:
                    if ss.item.category == code.category:
                        pass
                    else:
                        return_response = dict()
                        data = {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "massage": "Not applicable all items ",
                        }
                        return_response['data'] = data
                        return Response(return_response, status.HTTP_400_BAD_REQUEST)

                if code.discount_amount:
                    dis = real_amount - code.discount_amount
                    final_response = dict()
                    data = {
                        "status": "add successfully",
                        "coupon": coupon,
                        "amount": real_amount,
                        "discount": code.discount_amount,
                        "total": dis,
                    }
                    final_response['data'] = data

                    return Response(final_response, status.HTTP_200_OK)

                if code.discount_percent:
                    dis = code.discount_percent / 100
                    final = int(dis * real_amount)
                    total = real_amount - final
                    final_response = dict()
                    data = {
                        "status": "add successfully",
                        "coupon": coupon,
                        "amount": real_amount,
                        "discount": final,
                        "total": total,
                    }
                    final_response['data'] = data

                    return Response(final_response, status.HTTP_200_OK)


            if code.subcategory:
                for ss in cart:
                    print(ss.item.subcategory)
                    if ss.item.subcategory == code.subcategory:
                        pass
                    else:
                        return_response = dict()
                        data = {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "massage": "Not applicable all items ",
                        }
                        return_response['data'] = data
                        return Response(return_response, status.HTTP_400_BAD_REQUEST)

                if code.discount_amount:
                    dis = real_amount - code.discount_amount
                    final_response = dict()
                    data = {
                        "status": "add successfully",
                        "coupon": coupon,
                        "amount": real_amount,
                        "discount": code.discount_amount,
                        "total": dis,
                    }
                    final_response['data'] = data

                    return Response(final_response, status.HTTP_200_OK)

                if code.discount_percent:
                    dis = code.discount_percent / 100
                    final = int(dis * real_amount)
                    total = real_amount - final
                    final_response = dict()
                    data = {
                        "status": "add successfully",
                        "coupon": coupon,
                        "amount": real_amount,
                        "discount": final,
                        "total": total,
                    }
                    final_response['data'] = data

                    return Response(final_response, status.HTTP_200_OK)

            if code.store:
                for ss in cart:
                    if ss.item.store == code.store:
                        pass
                    else:
                        return_response = dict()
                        data = {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "massage": "Not applicable all items ",
                        }
                        return_response['data'] = data
                        return Response(return_response, status.HTTP_400_BAD_REQUEST)

                if code.discount_amount:
                    dis = real_amount - code.discount_amount
                    final_response = dict()
                    data = {
                        "status": "add successfully",
                        "coupon": coupon,
                        "amount": real_amount,
                        "discount": code.discount_amount,
                        "total": dis,
                    }
                    final_response['data'] = data

                    return Response(final_response, status.HTTP_200_OK)

                if code.discount_percent:
                    dis = code.discount_percent / 100
                    final = int(dis * real_amount)
                    total = real_amount - final
                    final_response = dict()
                    data = {
                        "status": "add successfully",
                        "coupon": coupon,
                        "amount": real_amount,
                        "discount": final,
                        "total": total,
                    }
                    final_response['data'] = data

                    return Response(final_response, status.HTTP_200_OK)

            if code.coupon_for == "First user":

                qs = Order.objects.filter(user=user, order_status=True).values('coupon__coupon_code')
                for q in qs:
                    print(q['coupon__coupon_code'])
                    if q['coupon__coupon_code'] == code.coupon_code:
                        return_response = dict()
                        data = {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "massage": "coupon already used ",
                        }
                        return_response['data'] = data
                        return Response(return_response, status.HTTP_400_BAD_REQUEST)

                if code.discount_amount:
                    dis = real_amount - code.discount_amount
                    final_response = dict()
                    data = {
                        "status": "add successfully",
                        "coupon": coupon,
                        "amount": real_amount,
                        "discount": code.discount_amount,
                        "total": dis,
                    }
                    final_response['data'] = data

                    return Response(final_response, status.HTTP_200_OK)

                if code.discount_percent:
                    dis = code.discount_percent / 100
                    final = int(dis * real_amount)
                    total = real_amount - final
                    final_response = dict()
                    data = {
                        "status": "add successfully",
                        "coupon": coupon,
                        "amount": real_amount,
                        "discount": final,
                        "total": total,
                    }
                    final_response['data'] = data

                    return Response(final_response, status.HTTP_200_OK)
            else:
                return_response = dict()
                data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "massage": "Emoty cart ",
                }
                return_response['data'] = data
                return Response(return_response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

