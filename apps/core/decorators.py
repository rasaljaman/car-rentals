from django.http import HttpResponseForbidden

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("is_admin"):
            return HttpResponseForbidden("Admin access only")
        return view_func(request, *args, **kwargs)
    return wrapper