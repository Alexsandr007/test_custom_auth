from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.decorators import check_permission

class ProductListView(APIView):
    @check_permission('products', 'read')
    def get(self, request):
        products = [
            {'id': 1, 'name': 'Товар 1', 'price': 100, 'owner_id': 1},
            {'id': 2, 'name': 'Товар 2', 'price': 200, 'owner_id': 2},
            {'id': 3, 'name': 'Товар 3', 'price': 300, 'owner_id': 1},
        ]
        return Response(products)

class OrderListView(APIView):
    @check_permission('orders', 'read')
    def get(self, request):
        orders = [
            {'id': 1, 'product': 'Товар 1', 'status': 'обработан', 'owner_id': 1},
            {'id': 2, 'product': 'Товар 2', 'status': 'в обработке', 'owner_id': 2},
        ]
        return Response(orders)

class StoreListView(APIView):
    @check_permission('stores', 'read')
    def get(self, request):
        stores = [
            {'id': 1, 'name': 'Магазин 1', 'address': 'Адрес 1'},
            {'id': 2, 'name': 'Магазин 2', 'address': 'Адрес 2'},
        ]
        return Response(stores)