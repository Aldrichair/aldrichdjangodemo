from django.urls import path
from .views import ImageCodeView, InfoCodeView

"""
var url ='/sms_codes/' + this.mobile + '/' + '?image_code=' + this.image_code+ '&image_code_id=' + this.image_code_id
"""
urlpatterns = [
    path('image_codes/<uuid>/', ImageCodeView.as_view()),
    path('sms_codes/<mobile>/', InfoCodeView.as_view())
]