from django.contrib.auth.models import User
from django.db.models.fields import DateField
from django.db.models.functions import TruncMonth, TruncDay
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Count, Sum
from datetime import date, timezone, timedelta, datetime

from backend_roc.utils.permissions import Is_admin
from product.models.order import Order
from product.models.store import Store
from product.serializer.graph_serializer import Count_Serializer, StoreMonthSaleSerializer

from django.db.models import Q


class get_user_View(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = Count_Serializer

    def post(self, request):
        serializer = Count_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            start_date = serializer.data.get('start_date')
            end_data = serializer.data.get('end_data')

            if start_date and end_data is not None:
                queryset = User.objects.filter(is_active=True, date_joined__range=[start_date, end_data]).annotate(month=TruncMonth('date_joined', DateField())).values('month').annotate(total=Count('id'))
                final_response = dict()
                final_response['data'] = []

                total = 0
                for qs in queryset:
                    total = total + qs['total']
                    data = {
                        "month": qs['month'],
                        "total": qs['total'],
                        "all_total": total,
                    }
                    final_response['data'].append(data)
                return Response(final_response, status.HTTP_200_OK)
            else:
                queryset = User.objects.filter(is_active=True).annotate(month=TruncMonth('date_joined', DateField())).values('month').annotate(total=Count('id'))

                final_response = dict()

                final_response['data'] = []
                total = 0
                for qs in queryset:
                    total = total + qs['total']
                    data = {
                        "month": qs['month'],
                        "total": qs['total'],
                        "all_total": total,
                    }
                    final_response['data'].append(data)
                return Response(final_response, status.HTTP_200_OK)


class get_user_day_View(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = Count_Serializer

    def post(self, request):
        serializer = Count_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            start_date = serializer.data.get('start_date')
            end_data = serializer.data.get('end_data')
            if start_date and end_data is not None:
                queryset = User.objects.filter(date_joined__range=[start_date, end_data]).annotate(day=TruncDay('date_joined', DateField())).values('day').annotate(total=Count('id'))
                final_response = dict()
                # data = {
                #     "users": queryset,
                # }
                final_response['data'] = queryset
                return Response(final_response, status.HTTP_200_OK)
            else:
                queryset = User.objects.annotate(day=TruncDay('date_joined', DateField())).values('day').annotate(total=Count('id'))
                final_response = dict()
                # print(queryset)
                # data = {
                #     "users": queryset,
                # }
                final_response['data'] = queryset
                return Response(final_response, status.HTTP_200_OK)


class get_order_month_View(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = Count_Serializer

    def post(self, request):
        serializer = Count_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            start_date = serializer.data.get('start_date')
            end_data = serializer.data.get('end_data')
            if start_date and end_data is not None:
                queryset = Order.objects.filter(created_at__range=[start_date, end_data], order_status=True).annotate(month=TruncMonth('created_at', DateField())).values('month').annotate(total=Count('id'))
                final_response = dict()
                final_response['data'] = []

                total = 0
                for qs in queryset:
                    total = total + qs['total']
                    data = {
                        "month": qs['month'],
                        "total": qs['total'],
                        "all_total": total,
                    }
                    final_response['data'].append(data)
                return Response(final_response, status.HTTP_200_OK)
            else:
                queryset = Order.objects.filter(order_status=True).annotate(month=TruncMonth('created_at', DateField())).values('month').annotate(total=Count('id'))
                final_response = dict()
                final_response['data'] = []
                total = 0
                for qs in queryset:
                    total = total + qs['total']
                    data = {
                        "month": qs['month'],
                        "total": qs['total'],
                        "all_total": total,
                    }
                    final_response['data'].append(data)
                return Response(final_response, status.HTTP_200_OK)


class get_order_day_View(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = Count_Serializer

    def post(self, request):
        serializer = Count_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            start_date = serializer.data.get('start_date')
            end_data = serializer.data.get('end_data')
            if start_date and end_data is not None:
                date = datetime.strptime(end_data, "%Y-%m-%d").date()
                modified_date = date + timedelta(days=1)
                queryset = Order.objects.filter(created_at__range=[start_date, modified_date], order_status=True).annotate(day=TruncDay('created_at', DateField())).values('day').annotate(total=Count('id'))
                final_response = dict()
                # data = {
                #     "users": queryset,
                # }
                final_response['data'] = queryset
                return Response(final_response, status.HTTP_200_OK)
            else:
                queryset = Order.objects.filter(order_status=True).annotate(day=TruncDay('created_at', DateField())).values('day').annotate(total=Count('id'))
                final_response = dict()
                # print(queryset)
                # data = {
                #     "users": queryset,
                # }
                final_response['data'] = queryset
                return Response(final_response, status.HTTP_200_OK)


class store_order_month_View(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = Count_Serializer

    def post(self, request, pk=None):
        serializer = Count_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            start_date = serializer.data.get('start_date')
            end_data = serializer.data.get('end_data')
            if start_date and end_data is not None:
                date = datetime.strptime(end_data, "%Y-%m-%d").date()
                modified_date = date + timedelta(days=1)
                queryset = Order.objects.filter(items__item__store__id=pk,
                                                created_at__range=[start_date, modified_date],
                                                order_status=True
                                                ).annotate(month=TruncMonth('created_at', DateField())).values('month').annotate(total=Count('id'))
                final_response = dict()
                final_response['data'] = []

                total = 0
                for qs in queryset:
                    total = total + qs['total']
                    data = {
                        "month": qs['month'],
                        "total": qs['total'],
                        "all_total": total,
                    }
                    final_response['data'].append(data)
                return Response(final_response, status.HTTP_200_OK)
            else:
                queryset = Order.objects.filter(
                    items__item__store__id=pk,
                    order_status=True
                ).annotate(month=TruncMonth('created_at', DateField())).values('month').annotate(total=Count('id'))
                final_response = dict()
                final_response['data'] = []
                total = 0
                for qs in queryset:
                    total = total + qs['total']
                    data = {
                        "month": qs['month'],
                        "total": qs['total'],
                        "all_total": total,
                    }
                    final_response['data'].append(data)
                return Response(final_response, status.HTTP_200_OK)


class store_order_day_View(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = Count_Serializer

    def post(self, request, pk=None):
        serializer = Count_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            start_date = serializer.data.get('start_date')
            end_data = serializer.data.get('end_data')
            if start_date and end_data is not None:
                date = datetime.strptime(end_data, "%Y-%m-%d").date()
                modified_date = date + timedelta(days=1)
                queryset = Order.objects.filter(items__item__store__id=pk, created_at__range=[start_date, modified_date], order_status=True).annotate(day=TruncDay('created_at', DateField())).values('day').annotate(total=Count('id'))
                final_response = dict()
                # data = {
                #     "users": queryset,
                # }
                final_response['data'] = queryset
                return Response(final_response, status.HTTP_200_OK)
            else:
                queryset = Order.objects.filter(items__item__store__id=pk, order_status=True).annotate(day=TruncDay('created_at', DateField())).values('day').annotate(total=Count('id'))
                final_response = dict()
                # print(queryset)
                # data = {
                #     "users": queryset,
                # }
                final_response['data'] = queryset
                return Response(final_response, status.HTTP_200_OK)


class tranding_order_count_View(GenericAPIView):
    permission_classes = [Is_admin, ]

    def get(self, request, pk=None):
        queryset = Order.objects.filter(order_status=True).values('items__item__name').annotate(count=Count('items__item__name'))
        print(queryset)
        final_response = dict()
        final_response['data'] = []
        for qs in queryset:
            if qs['items__item__name'] is not None:
                data = {
                    "name": qs['items__item__name'],
                    "total": qs['count'],
                }
                final_response['data'].append(data)
        return Response(final_response, status.HTTP_200_OK)


class pending_order_View(GenericAPIView):
    permission_classes = [Is_admin, ]

    def get(self, request, pk=None):
        today = date.today()
        queryset = Order.objects.filter(created_at__gte=today, order_status=True, status="Inprocess").values('items__item__name').annotate(count=Count('items__item__name'))
        print(queryset)
        final_response = dict()
        final_response['data'] = []
        for qs in queryset:
            if qs['items__item__name'] is not None:
                data = {
                    "name": qs['items__item__name'],
                    "total": qs['count'],
                }
                final_response['data'].append(data)
        return Response(final_response, status.HTTP_200_OK)


class today_order_View(GenericAPIView):
    permission_classes = [Is_admin, ]

    def get(self, request, pk=None):
        today = date.today()
        print(today)
        queryset = Order.objects.filter(order_status=True,
                                        created_at__gte=today,
                                        # created_at__date=today,
                                        # created_at__year=today.year,
                                        # created_at__month=today.month,
                                        # created_at__day=today.day,
                                        ).values('items__item__name').annotate(count=Count('items__item__name'))
        print(queryset)
        final_response = dict()
        final_response['data'] = []
        for qs in queryset:
            if qs['items__item__name'] is not None:
                data = {
                    "name": qs['items__item__name'],
                    "total": qs['count'],
                }
                final_response['data'].append(data)
        return Response(final_response, status.HTTP_200_OK)


class month_revenue_View(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = Count_Serializer

    def post(self, request):
        serializer = Count_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            start_date = serializer.data.get('start_date')
            end_data = serializer.data.get('end_data')
            if start_date and end_data is not None:
                date = datetime.strptime(end_data, "%Y-%m-%d").date()
                modified_date = date + timedelta(days=1)
                print(modified_date)
                queryset = Order.objects.filter(created_at__range=[start_date, modified_date],
                                                order_status=True
                                                ).annotate(month=TruncMonth('created_at', DateField())).values('month').annotate(Sum('amount'))
                final_response = dict()
                final_response['data'] = []
                for qs in queryset:
                    total = int(qs['amount__sum'])
                    data = {
                        "month": qs['month'],
                        "total": total,
                        # "all_total": total,
                    }
                    final_response['data'].append(data)
                return Response(final_response, status.HTTP_200_OK)
            else:
                queryset = Order.objects.filter(order_status=True
                                                ).annotate(month=TruncMonth('created_at', DateField())).values('month').annotate(Sum('amount'))
                print(queryset)
                final_response = dict()
                final_response['data'] = []
                for qs in queryset:
                    total = int(qs['amount__sum'])
                    data = {
                        "month": qs['month'],
                        "total": total,
                        # "all_total": total,
                    }
                    final_response['data'].append(data)
                return Response(final_response, status.HTTP_200_OK)


class day_revenue_View(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = Count_Serializer

    def post(self, request):
        serializer = Count_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            start_date = serializer.data.get('start_date')
            end_data = serializer.data.get('end_data')
            if start_date and end_data is not None:
                date = datetime.strptime(end_data, "%Y-%m-%d").date()
                modified_date = date + timedelta(days=1)
                queryset = Order.objects.filter(created_at__range=[start_date, modified_date],
                                                order_status=True
                                                ).annotate(day=TruncDay('created_at', DateField())).values('day').annotate(Sum('amount'))
                final_response = dict()
                final_response['data'] = []
                for qs in queryset:
                    total = int(qs['amount__sum'])
                    data = {
                        "day": qs['day'],
                        "total": total,
                        # "all_total": total,
                    }
                    final_response['data'].append(data)
                return Response(final_response, status.HTTP_200_OK)
            else:
                queryset = Order.objects.filter(order_status=True
                                                ).annotate(day=TruncDay('created_at', DateField())).values('day').annotate(Sum('amount'))
                final_response = dict()
                final_response['data'] = []
                for qs in queryset:
                    total = int(qs['amount__sum'])
                    data = {
                        "day": qs['day'],
                        "total": total,
                        # "all_total": total,
                    }
                    final_response['data'].append(data)
                return Response(final_response, status.HTTP_200_OK)


class store_revenue_month_View(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = Count_Serializer

    def post(self, request, pk=None):
        serializer = Count_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            start_date = serializer.data.get('start_date')
            end_data = serializer.data.get('end_data')
            if start_date and end_data is not None:
                date = datetime.strptime(end_data, "%Y-%m-%d").date()
                modified_date = date + timedelta(days=1)
                store = Store.objects.all()
                id = []
                for qsq in store:
                    a = qsq.store_name
                    id.append(a)
                    print("id", id)

                qss = []
                for y in id:
                    queryset = Order.objects.filter(
                        items__item__store__store_name=y,
                        created_at__range=[start_date, modified_date],
                        order_status=True,
                        ).values('items__item__store__store_name').annotate(month=TruncMonth('created_at', DateField())).values('month').annotate(Sum('amount'))
                    if queryset.exists():
                        for data_queryset in queryset:
                            data = dict(data_queryset)
                            data["store_name"] = y
                            qss.append(data)

                return Response(qss, status.HTTP_200_OK)
            else:
                store = Store.objects.all()
                id = []
                for qsq in store:
                    a = qsq.store_name
                    id.append(a)
                    print("id", id)

                qss = []
                for y in id:
                    queryset = Order.objects.filter(
                        order_status=True,
                        items__item__store__store_name=y,
                    ).annotate(month=TruncMonth('created_at', DateField())).values('month').annotate(Sum('amount'))
                    if queryset.exists():
                        for data_queryset in queryset:
                            data = dict(data_queryset)
                            data["store_name"] = y
                            qss.append(data)

                return Response(qss, status.HTTP_200_OK)


class store_day_revenue_View(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = Count_Serializer

    def post(self, request):
        try:
            serializer = Count_Serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                start_date = serializer.data.get('start_date')
                end_data = serializer.data.get('end_data')
                if start_date and end_data is not None:
                    date = datetime.strptime(end_data, "%Y-%m-%d").date()
                    modified_date = date + timedelta(days=1)
                    store = Store.objects.all()
                    id = []
                    for qsq in store:
                        a = qsq.store_name
                        id.append(a)
                        print("id", id)

                    qss = []
                    for y in id:
                        queryset = Order.objects.filter(
                            items__item__store__store_name=y,
                            created_at__range=[start_date, modified_date],
                            order_status=True,
                            ).annotate(day=TruncDay('created_at', DateField())).values('day').annotate(Sum('amount'))
                        if queryset.exists():
                            data = dict()
                            data["store_name"] = y
                            data["data"] = queryset
                            qss.append(data)

                    return Response(qss, status.HTTP_200_OK)
                else:
                    store = Store.objects.all()
                    id = []
                    for qsq in store:
                        a = qsq.store_name
                        id.append(a)

                    qss = []
                    for y in id:
                        queryset = Order.objects.filter(
                            items__item__store__store_name=y,
                            order_status=True,
                        ).annotate(day=TruncDay('created_at', DateField())).values('day').annotate(Sum('amount'))
                        print(queryset)

                        if queryset.exists():
                            data = dict()
                            data["store_name"] = y
                            data["data"] = queryset
                            qss.append(data)

                    return Response(qss, status.HTTP_200_OK)
        except:
            return Response("somethig went wrong", status.HTTP_400_BAD_REQUEST)


class StoreMonthSaleView(GenericAPIView):
    permission_classes = [Is_admin, ]
    serializer_class = StoreMonthSaleSerializer

    def post(self, request, pk=None):
        serializer = StoreMonthSaleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            store_id = serializer.data.get('store_id')

            if store_id:
                queryset = Order.objects.filter(
                    items__item__store__storeId=store_id,
                    order_status=True,
                    ).values('items__item__store__store_name').annotate(month=TruncMonth('created_at', DateField())).values(
                    'month', 'items__item__store__store_name').annotate(Sum('amount'))
                responce_data = dict()
                responce_data['data'] = []
                for data_queryset in queryset:
                    data = {
                        'store': data_queryset['items__item__store__store_name'],
                        'month': data_queryset['month'],
                        'amount': data_queryset['amount__sum']
                    }
                    responce_data['data'].append(data)

                return Response(responce_data, status.HTTP_200_OK)
            else:
                store = Store.objects.all()
                queryset = Order.objects.filter(
                    items__item__store__in=store,
                    order_status=True,
                ).values('items__item__store__store_name').annotate(month=TruncMonth('created_at', DateField())).values(
                    'month', 'items__item__store__store_name').annotate(Sum('amount'))
                responce_data = dict()
                responce_data['data'] = []
                for data_queryset in queryset:
                    data = {
                        'store': data_queryset['items__item__store__store_name'],
                        'month': data_queryset['month'],
                        'amount': data_queryset['amount__sum']
                    }
                    responce_data['data'].append(data)
                return Response(responce_data, status.HTTP_200_OK)