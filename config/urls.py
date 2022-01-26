from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

from core.users.views import UserCreateView

from django_email_verification import urls as email_urls  # include the urls


urlpatterns = [
    path(
        '',
        include('core.store.urls'),
    ),
    path(
        'articles/',
        include('core.articles.urls'),
    ),
    path(
        '',
        include('core.cart.urls'),
    ),
    path('',include('core.users.urls')),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True)),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('email/', include(email_urls)),  # connect them to an arbitrary path
    path('', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
