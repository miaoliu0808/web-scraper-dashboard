from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    
    # 当用户访问 /api/scrape/ 时，触发 views.py 里的 trigger_scraper 函数
    path('api/scrape/', views.trigger_scraper, name='trigger_scraper'),
]