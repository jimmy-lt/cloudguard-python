# cloudguard/client.py
# ====================
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
import httpx

from cloudguard.config import Config


class APIClient(httpx.Client):
    """HTTP client to communicate with the CloudGuard API.


    :param config: CloudGuard configuration.
    :type config: ~cloudguard.config.Config

    """

    def __init__(self, config: Config):
        """Constructor for :class:`cloudguard.client.Client`."""
        super().__init__(
            auth=httpx.BasicAuth(
                config.credentials.api.key, config.credentials.api.secret
            ),
            base_url=config.region.api,
        )

        self.config = config


class AsyncAPIClient(APIClient, httpx.AsyncClient):
    """Asynchronous HTTP client to communicate with the CloudGuard API.


    :param config: CloudGuard configuration.
    :type config: ~cloudguard.config.Config

    """

    pass
