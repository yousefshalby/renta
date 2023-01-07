from modeltranslation.translator import TranslationOptions, register
from . import models

@register(models.Properties)
class PropertiesTranslation(TranslationOptions):
    fields = ['title', "description", 'address']
    
    
@register(models.Area)
class AreaTranslation(TranslationOptions):
    fields = ['name', ]    
    

@register(models.PropertyType)
class PropertyTypeTranslation(TranslationOptions):
    fields = ['name', ]    
    
@register(models.AboutUs)
class AboutUsTranslation(TranslationOptions):
    fields = ['first_paragraph_title', 'first_paragraph_text', 'second_paragraph_title', 'second_paragraph_text', 'third_paragraph_title', 'third_paragraph_text', 'forth_paragraph_title', 'forth_paragraph_text']     