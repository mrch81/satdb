#!/usr/bin/env python

"""Unit test for fetcher_service."""
import asyncio
import logging
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from fetch_service.tle_updater import TLEUpdater
from satdb.settings import FETCH_TLE_FREQUENCY, SATELLITE_FEED_URL

logger = logging.getLogger(__name__)


@pytest.fixture
def tle_updater() -> TLEUpdater:
    """Fixture TLEUpdater instance."""
    return TLEUpdater()


@pytest.mark.asyncio
@patch('your_module.aiohttp.ClientSession')
async def test_fetch_tle_data(mock_session: MagicMock,
                              tle_updater: TLEUpdater) -> None:
    """Test for the asynchronous fetch_tle_data method."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = asyncio.Future()
    mock_response.json.return_value.set_result({
        'member': [{'name': 'ISS',
                    'satelliteId': '25544',
                    'date': '2021-01-01',
                    'line1': '1 25544U',
                    'line2': '2 25544'}]
    })
    mock_session.return_value.__aenter__.return_value.get.return_value = mock_response  # noqa: E501

    # Execute
    result: Dict[str, Any] = await tle_updater.fetch_tle_data()

    # Verify
    assert result == {
        'member': [{'name': 'ISS',
                    'satelliteId': '25544',
                    'date': '2021-01-01',
                    'line1': '1 25544U',
                    'line2': '2 25544'}]
    }

    mock_session.return_value.__aenter__.return_value.get.assert_called_once_with(SATELLITE_FEED_URL)  # noqa: E501


# Test for the asynchronous update_satellites method
@pytest.mark.asyncio
@patch('your_module.asyncio.sleep', new_callable=AsyncMock)
@patch('your_module.TLEUpdater.fetch_tle_data')
@patch('your_module.TLEUpdater.update_satellite')
async def test_update_satellites(
    mock_update_satellite: MagicMock,
    mock_fetch_tle_data: MagicMock,
    mock_sleep: AsyncMock,
    tle_updater: TLEUpdater
) -> None:
    """Test for the asynchronous update_satellites method."""
    # Setup mocks
    mock_fetch_tle_data.return_value = asyncio.Future()
    mock_fetch_tle_data.return_value.set_result({
        'member': [{'name': 'ISS', 'satelliteId': '25544'}]
    })
    mock_update_satellite.return_value = asyncio.Future()
    mock_update_satellite.return_value.set_result(None)

    # Stop loop after 1 iteration
    mock_sleep.side_effect = asyncio.CancelledError()

    # Execute
    with pytest.raises(asyncio.CancelledError):
        await tle_updater.update_satellites()

    # Verify
    mock_update_satellite.assert_called_once()
    mock_fetch_tle_data.assert_called_once()
    mock_sleep.assert_called_once_with(FETCH_TLE_FREQUENCY)
