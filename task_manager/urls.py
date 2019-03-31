from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import reverse_lazy

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$',RedirectView.as_view(url=reverse_lazy('tasks:index'),permanent=False)),
    url(r'tasks/',include('tasks.urls')),
]
