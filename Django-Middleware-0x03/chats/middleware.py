# chats/middleware.py

from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden, HttpResponse



class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with open("requests.log", "a") as log_file:
            log_file.write(log_message)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Only allow access between 6 PM and 9 PM
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to chats is restricted during this time.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}

    def __call__(self, request):
        # Only monitor POST requests (i.e., message sending)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize if IP not already tracked
            if ip not in self.message_log:
                self.message_log[ip] = []

            # Filter messages in the last 60 seconds
            recent_msgs = [
                timestamp for timestamp in self.message_log[ip]
                if now - timestamp < timedelta(minutes=1)
            ]

            # Update log
            recent_msgs.append(now)
            self.message_log[ip] = recent_msgs

            if len(recent_msgs) > 5:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute.")

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is authenticated
        user = request.user

        # Only block if user is authenticated and not an admin or moderator
        if user.is_authenticated:
            # Check if user has role attribute (assumes custom User model or profile)
            role = getattr(user, 'role', None)

            if role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You are not allowed to perform this action.")

        return self.get_response(request)
