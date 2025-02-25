from .models import SiteSettings

def site_settings(request):
    """Context processor to add site settings to all templates"""
    try:
        settings = SiteSettings.objects.first()
        return {
            'site_logo': settings.logo if settings else None
        }
    except Exception as e:
        print(f"Error loading site settings: {e}")
        return {'site_logo': None}