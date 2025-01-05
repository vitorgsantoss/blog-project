from .models import SiteSetup

def site_setup(request):
    setup = SiteSetup.objects.order_by('-id').first()
    print(setup)
    return {
        'setup': setup,
    }