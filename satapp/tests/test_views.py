#!/usr/bin/env python

"""Test admin module."""

import pytest


@pytest.mark.django_db
def test_admin_view(client):
    """Get admin view."""
    response = client.get('/admin/', follow=True)
    assert response.status_code == 200
