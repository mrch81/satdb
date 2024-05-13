#!/usr/bin/env python

"""Disable CSRF for GraphQL. TODO: Find a better way."""

from typing import Callable

from django.http import HttpRequest, HttpResponse


class DisableCSRF:
    """Disable CSRF to allow the front to access data (TODO temporary)."""

    def __init__(self,
                 get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Disable CSRF constructor method.

        Args:
            get_response (Callable): a typical middleware handling callable
            that processes an HttpRequest and returns an HttpResponse object.
        """
        self.get_response: Callable[[HttpRequest], HttpResponse] = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Disable CSRF if the request ends with graphql.

        Args:
            request (HttpRequest): request

        Returns:
            response: HttpResponse
        """
        # Disable CSRF only for the GraphQL endpoint
        if request.path.startswith('/graphql'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        response: HttpResponse = self.get_response(request)
        return response
