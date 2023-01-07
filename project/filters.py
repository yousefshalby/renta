import django_filters
from django.db.models import Q

from project.models import Properties


class PropertiesFilter(django_filters.FilterSet):
    price_gte = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_lte = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    area_gte = django_filters.NumberFilter(field_name="area", lookup_expr="gte")
    area_lte = django_filters.NumberFilter(field_name="area", lookup_expr="lte")
 
    class Meta:
        model = Properties
        fields = (
           'Bedrooms','Bathrooms', 'price', 'property_type', 'area'
        )

    
