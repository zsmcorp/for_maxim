from django.urls import re_path
from django.conf.urls.static import static
from django.contrib import admin
from mainapp import settings
from django.urls import path, include
import debug_toolbar
from .yasg import urlpatterns as doc_urls

urlpatterns = [
                  re_path(r'user/', include('api.views.user.urls')),
                  re_path(r'support/', include('api.views.support.urls')),
                  re_path(r'category/', include('api.views.category.urls')),
                  re_path(r'account/', include('api.views.account.urls')),
                  re_path(r'purchases/', include('api.views.purchases.urls')),
                  re_path(r'news/', include('api.views.news.urls')),
                  re_path(r'product/', include('api.views.product.urls')),
                  re_path(r'company/', include('api.views.company.urls')),
                  re_path(r'messages/', include('api.views.messages.urls')),
                  re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  path('__debug__/', include(debug_toolbar.urls)),
              ] + \
              static(settings.STATIC_URL,
                     document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
