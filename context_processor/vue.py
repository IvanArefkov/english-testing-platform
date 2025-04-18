from django.conf import settings

def vue_script_src(request):
    return {
        'vue_script_src': settings.VUE_SCRIPT_SRC,
    }