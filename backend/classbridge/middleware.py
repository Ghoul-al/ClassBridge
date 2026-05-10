class SchoolIsolationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'school_id'):
            request.school_id = request.user.school_id
        return self.get_response(request)