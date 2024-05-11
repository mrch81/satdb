#!/usr/bin/env python

"""Unit test for fetcher_service."""
# import asyncio
import logging

import pytest

from fetch_service.tle_updater import TLEUpdater

# from typing import Any, Dict
# from unittest.mock import AsyncMock, MagicMock, patch


# from satdb.settings import FETCH_TLE_FREQUENCY, SATELLITE_FEED_URL

logger = logging.getLogger(__name__)


@pytest.fixture
def tle_updater() -> TLEUpdater:
    """Fixture TLEUpdater instance."""
    return TLEUpdater()


@pytest.mark.asyncio
async def test_fetch_tle_data(tle_updater: TLEUpdater) -> None:
    """Test for the asynchronous fetch_tle_data method."""
    logger.warning("TODO: Implement this test")
    pass
    # # Setup mock response
    # mock_response = MagicMock()
    # mock_response.json.return_value = asyncio.Future()
    # mock_response.json.return_value.set_result({
    #     'member': [{'name': 'ISS',
    #                 'satelliteId': '25544',
    #                 'date': '2021-01-01',
    #                 'line1': '1 25544U',
    #                 'line2': '2 25544'}]
    # })
    #
    # mock_session = MagicMock()
    # mock_session.return_value.__aenter__.return_value.get.return_value = mock_response  # noqa: E501
    #
    # # Execute
    # result: Dict[str, Any] = await tle_updater.fetch_tle_data()

    # # Verify
    # assert result == {
    #     'member': [{'name': 'ISS',
    #                 'satelliteId': '25544',
    #                 'date': '2021-01-01',
    #                 'line1': '1 25544U',
    #                 'line2': '2 25544'}]
    # }

    # mock_session.return_value.__aenter__.return_value.get.assert_called_once_with(SATELLITE_FEED_URL)  # noqa: E501


# Test for the asynchronous update_satellites method
@pytest.mark.asyncio
async def test_update_satellites(
    tle_updater: TLEUpdater
) -> None:
    """Test for the asynchronous update_satellites method."""
    # Setup mocks
    logger.warning("TODO: Implement this test")
    pass
