from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('ecommerce/', include('ecommerce.urls')),
                  path('product/', include('product.urls')),
                  path('accounts/', include('user.urls')),
                  path('social-auth/', include('social_django.urls', namespace='social')),
                  path('app/', include('app.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
