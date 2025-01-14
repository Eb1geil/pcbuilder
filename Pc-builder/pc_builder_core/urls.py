from django.urls import path
from .views import motherboard_detail_view, filter_components_by_motherboard, select_motherboard, get_preset

urlpatterns = [
    path('', select_motherboard, name='select_motherboard'),
    path('motherboards/<int:motherboard_id>/', motherboard_detail_view, name='motherboard_view'),  # исправлено здесь
    path('filter/<int:motherboard_id>/<str:component_type>/', filter_components_by_motherboard, name='filter_components_by_motherboard'),
    path('preset/<int:motherboard_id>/<str:preset_type>/', get_preset, name='get_preset'),
]
