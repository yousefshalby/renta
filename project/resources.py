from import_export import resources
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from . import models


class AreaResource(resources.ModelResource):
    class Meta:
        model = models.Area
        fields = ("id", "name_en", 'name_ar')
        export_order = fields


class PropertyTypeResource(resources.ModelResource):
    class Meta:
        model = models.PropertyType
        fields = ("id", "name_en", 'name_ar')
        export_order = fields


class UserContractResource(resources.ModelResource):
    property_title = Field(
        column_name='property name',
        attribute='property',
        widget=ForeignKeyWidget(models.Properties, 'title'),
    )
    
    class Meta:
        model = models.UserContract
        fields = ('id','renter_name', 'rent_amount_per_month', 'contract_start', 'contract_end', 'contract_photo', 'renter_id_photo', 'property_title')
        export_order = fields


class PropertyResource(resources.ModelResource):
    area_name = Field(
        column_name='area name',
        attribute='area',
        widget=ForeignKeyWidget(models.Area, 'name'),
    )

    property_type_name = Field(
        column_name='property_type name',
        attribute='property_type',
        widget=ForeignKeyWidget(models.PropertyType, 'name'),
    )

    class Meta:
        model = models.Properties
        fields = ('id', 'title', 'address', 'price', 'Bedrooms','Bathrooms', 'listing_date', 'area_name', 'property_type_name', 'latitude', 'longitude')
        export_order = fields
        
