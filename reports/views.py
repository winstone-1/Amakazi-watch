from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "name": "AmakaziWatch API",
        "description": "GBV Awareness, Reporting and Prevention Platform for Kenya",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs/",
        "redoc": "/redoc/",
        "schema": "/api/schema/",
        "endpoints": {
            "auth": {
                "register": "/api/auth/register/",
                "login": "/api/auth/token/",
                "refresh": "/api/auth/token/refresh/"
            },
            "reports": {
                "submit": "/api/reports/",
                "heatmap": "/api/reports/heatmap/"
            },
            "organisations": {
                "list": "/api/organisations/",
                "register": "/api/organisations/register/",
                "map": "/api/organisations/map/",
                "heatmap": "/api/organisations/heatmap/"
            },
            "content": {
                "list": "/api/content/",
                "create": "/api/content/create/",
                "videos": "/api/content/videos/"
            },
            "quizzes": {
                "list": "/api/quizzes/",
                "complete": "/api/quizzes/<id>/complete/"
            },
            "donations": {
                "initiate": "/api/donations/initiate/",
                "verify": "/api/donations/verify/"
            },
            "chat": "/api/chat/"
        }
    })
