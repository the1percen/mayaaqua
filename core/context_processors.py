from .models import CompanySetting

def company_settings(request):
    try:
        settings = CompanySetting.objects.first()
    except Exception:
        settings = None
    return {'company': settings}
