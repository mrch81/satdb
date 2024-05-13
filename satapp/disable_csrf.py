#!/usr/bin/env python

"""Disable CSRF for GraphQL. TODO: Find a better way"""


class DisableCSRF:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Disable CSRF only for the GraphQL endpoint
        if request.path.startswith('/graphql'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response

