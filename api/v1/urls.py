from tkinter.font import names

from django.urls import include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from api.v1.viewsets import *

router = routers.DefaultRouter()

router.register(r'user', UserViewset, basename='usuario'),
router.register(r'province', ProvinceViewset, basename='provincia'),
router.register(r'service', ServiceViewset, basename='servicio'),
router.register(r'municipality', MunicipalityViewset, basename='municipio'),
router.register(r'school', SchoolViewset, basename='escuela'),
router.register(r'client', ClientViewset, basename='cliente'),
router.register(r'client-classes', ClientClassesViewset, basename='cliente-classes'),
router.register(r'company', CompanyViewset, basename='empresa'),
router.register(r'dutiesrigths', DutiesrigthsViewset, basename='deberesYderechos'),
router.register(r'classroom', ClassroomViewset, basename='aula'),
router.register(r'course', CourseViewset, basename='curso'),
router.register(r'offer', OfferViewset, basename='oferta'),
router.register(r'multipleBooking', MultipleBookingsViewset, basename='ReservaEmpresa'),
router.register(r'booking', BookingViewset, basename='Reserva'),
router.register(r'payment-code', PaymentCodeViewset, basename='payment-code')


schema_view = get_schema_view(
    openapi.Info(
        title="Tramos",
        default_version='v1',
        description="Sistema de Tramos",
        # terms_of_service="https://apklis.cu/terms/",
        # contact=openapi.Contact(email="apklis@mprc.cu"),
    ),
    public=True,
)

urlpatterns = [
    re_path('', include(router.urls)),
    re_path('roles/', RoleListApiView.as_view(), name='roles-list'),
    re_path('reports/offer/current/', OfferListView.as_view(), name='offer-list'),
    re_path('reports/course-evaluation/', CourseReportView.as_view(), name='course-report'),
    re_path('payment/register/', PaymentAPIView.as_view(), name='payment-register'),
    re_path('payment/notification/', PaymentNotificationAPIView.as_view(), name='payment-notification'),
    re_path('swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path('swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
