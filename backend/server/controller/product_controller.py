from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from server.models import Product
from server.serializers import ProductSerializer


class initializeController_Product:
    def __str__(self):
        return "Initialize Controller"


# Get all products
@api_view(["GET"])
def get_all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_product_by_category(request, category):
    print(category)
    products = Product.objects.filter(category="DefaultType")
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_product_detailed(request, category, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def get_product_detailed_single_route(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def get_product_filters(request):
    """
    Get unique filter options for the product filters
    Returns all unique brands, connection types, etc. from the products database
    """
    # Get unique brands and count of products for each
    brands = (
        Product.objects.values("brand").annotate(count=Count("brand")).order_by("brand")
    )

    # Get unique connection types and count of products for each
    connections = (
        Product.objects.values("connections")
        .annotate(count=Count("connections"))
        .order_by("connections")
    )

    # Get price ranges (calculated on the fly)
    price_min = (
        Product.objects.order_by("price").first().price
        if Product.objects.exists()
        else 0
    )
    price_max = (
        Product.objects.order_by("-price").first().price
        if Product.objects.exists()
        else 1000
    )

    # Create price ranges based on actual data
    price_ranges = []
    if Product.objects.exists():
        # Define price ranges
        if price_min < 100:
            price_ranges.append(
                {
                    "name": "Under $100",
                    "min": 0,
                    "max": 99.99,
                    "count": Product.objects.filter(price__lt=100).count(),
                }
            )

        if price_min < 300 and price_max > 100:
            price_ranges.append(
                {
                    "name": "$100 - $300",
                    "min": 100,
                    "max": 299.99,
                    "count": Product.objects.filter(
                        price__gte=100, price__lt=300
                    ).count(),
                }
            )

        if price_min < 500 and price_max > 300:
            price_ranges.append(
                {
                    "name": "$300 - $500",
                    "min": 300,
                    "max": 499.99,
                    "count": Product.objects.filter(
                        price__gte=300, price__lt=500
                    ).count(),
                }
            )

        if price_max > 500:
            price_ranges.append(
                {
                    "name": "Over $500",
                    "min": 500,
                    "max": None,
                    "count": Product.objects.filter(price__gte=500).count(),
                }
            )
    else:
        # Default price ranges if no products exist
        price_ranges = [
            {"name": "Under $100", "min": 0, "max": 99.99, "count": 0},
            {"name": "$100 - $300", "min": 100, "max": 299.99, "count": 0},
            {"name": "$300 - $500", "min": 300, "max": 499.99, "count": 0},
            {"name": "Over $500", "min": 500, "max": None, "count": 0},
        ]

    # Product types (you could extend your model to include a 'type' field)
    # For now, let's return some default types based on product descriptions

    return Response(
        {
            "brands": list(brands),
            "connections": list(connections),
            "types": [],
            "price_ranges": price_ranges,
        }
    )
