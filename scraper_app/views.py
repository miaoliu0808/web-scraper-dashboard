from django.shortcuts import render
from django.http import JsonResponse
from .services import run_b2b_scraper

def dashboard_view(request):
    """
    接收用户的网页请求，返回一个 HTML 页面。
    """
    return render(request, 'scraper_app/dashboard.html')

def trigger_scraper(request):
    """
    接收用户的网页请求，调用爬虫服务，并返回 JSON 结果。
    """
    print("[*] 收到抓取请求，正在通知后厨开始工作...")
    
    # 调用我们在 service 层写好的爬虫主函数（为了测试快一点，我们先只抓 2 页）
    filename = run_b2b_scraper(max_pages=2) 
    
    # 根据后厨返回的结果，给前端网页不同的响应
    if filename:
        return JsonResponse({
            "status": "success",
            "message": "数据抓取成功！",
            "file_generated": filename
        })
    else:
        return JsonResponse({
            "status": "error",
            "message": "抓取失败或未能获取到数据。"
        }, status=500)