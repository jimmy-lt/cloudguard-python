# cloudguard/session.py
# =====================
#
# Copying
# -------
#
# Copyright (c) 2023 cloudguard authors and contributors.
#
# This file is part of the *cloudguard* project.
#
# *cloudguard* is a free software project. You can redistribute it and/or
# modify it following the terms of the MIT License.
#
# This software project is distributed *as is*, WITHOUT WARRANTY OF ANY KIND;
# including but not limited to the WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE and NONINFRINGEMENT.
#
# You should have received a copy of the MIT License along with *cloudguard*.
# If not, see <http://opensource.org/licenses/MIT>.
#
import typing as ty

import cloudguard.client
import cloudguard.typing as cgty

from cloudguard.config import Config
from cloudguard.region import CloudGuardRegion


class Session(object):
    """The session consolidates in a single place everything required to
    communicate with the CloudGuard API.

    """

    def __init__(self, *args, **kwargs):
        """Constructor for :class:`cloudguard.session.Session`."""
        self.client: ty.Optional[cgty.APIClient] = None
        self.config = Config.load()

    def __enter__(self) -> cloudguard.client.APIClient:
        """Initiate the client's context."""
        self.client = cloudguard.client.APIClient(self.config).__enter__()
        return self.client

    @property
    def region(self) -> ty.Optional[CloudGuardRegion]:
        """Get the CloudGuard region.


        :return: The CloudGuard region.
        :rtype: ~cloudguard.region.CloudGuardRegion

        """
        return self.config.region

    @region.setter
    def region(self, value: cgty.CloudGuardRegion) -> None:
        """Set the region to use when instantiating the client.


        :param value: The CloudGuard region.
        :type value: ~typing.Union[str, ~cloudguard.region.CloudGuardRegion]


        :raise TypeError: When the provided region is none of the accepted
                          types.

        :raise ValueError: When the provided region is not one of the known
                           regions.

        """
        self.config.region = value


class AsyncSession(Session):
    """The asynchronous session is to be used in a concurrent runtime."""

    __enter__ = None

    async def __aenter__(self) -> cloudguard.client.AsyncAPIClient:
        """Initiate the asynchronous client's context."""
        self.client = await cloudguard.client.AsyncAPIClient(self.config).__aenter__()
        return self.client
