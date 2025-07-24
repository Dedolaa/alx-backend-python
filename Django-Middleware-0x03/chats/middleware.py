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
        now = datetime.now().time()
        start = time(18, 0)  # 6:00 PM
        end = time(21, 0)    # 9:00 PM

        # If current time is outside 6 PM - 9 PM, deny access
        if not (start <= now <= end):
            return HttpResponseForbidden("Access to chat is only allowed between 6 PM and 9 PM.")

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_records = {}

    def __call__(self, request):
        # Only limit POST requests to messaging endpoints
        if request.method == 'POST' and '/messages' in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize if IP not tracked
            if ip not in self.ip_records:
                self.ip_records[ip] = []

            # Remove old timestamps >1 minute ago
            one_min_ago = now - timedelta(minutes=1)
            self.ip_records[ip] = [
                ts for ts in self.ip_records[ip] if ts > one_min_ago
            ]

            # Check if current count exceeds limit
            if len(self.ip_records[ip]) >= 5:
               return HttpResponse(
                  "You have exceeded the 5-message-per-minute limit. Please wait.",
                   status=429
)

            # Record new timestamp
            self.ip_records[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Handle proxies (if any)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

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