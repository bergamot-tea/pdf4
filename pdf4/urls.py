"""pdf4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . views import home_view, merge_view, insert_view, split_1_view, in_images_view, out_images_view, compress_view, rotate_view, in_pdf_view, in_text_view, faq_view, about_view, rules_view, policy_view
from django.views.generic.base import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home_page'),
    path('faq/', faq_view, name='faq_page'),
    path('about/', about_view, name='about_page'),
    path('rules/', rules_view, name='rules_page'),
    path('policy/', policy_view, name='policy_page'),
    path('merge/', merge_view, name='merge_page'),
    path('insert/', insert_view, name='insert_page'),
    path('split-1/', split_1_view, name='split_1_page'),
    path('in-images/', in_images_view, name='in_images_page'),
    path('out-images/', out_images_view, name='out_images_page'),
    path('compress/', compress_view, name='compress_page'),
    path('rotate/', rotate_view, name='rotate_page'),
    path('in-pdf/', in_pdf_view, name='in_pdf_page'),
    path('in-text/', in_text_view, name='in_text_page'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml"),),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)