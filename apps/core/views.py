from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from decouple import config
from .supabase import supabase

ADMIN_EMAIL = config("ADMIN_EMAIL")

def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email != ADMIN_EMAIL:
            return HttpResponseForbidden("Not allowed")

        try:
            supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
        except Exception:
            return render(request, "admin_login.html", {
                "error": "Invalid credentials"
            })

        request.session["is_admin"] = True
        return redirect("/admin-dashboard/")

    return render(request, "admin_login.html")
    
def admin_dashboard(request):
    if not request.session.get("is_admin"):
        return HttpResponseForbidden("Access denied")

    return render(request, "admin_dashboard.html")