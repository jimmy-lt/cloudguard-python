# cloudguard/typing.py
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
import typing as ty

import cloudguard.client
import cloudguard.region


#: Type definition for a CloudGuard API client.
APIClient = ty.Union[
    cloudguard.client.APIClient,
    cloudguard.client.AsyncAPIClient,
]

#: Type definition for a user provided
#: :class:`CloudGuard region <cloudguard.region.CloudGuardRegion>`.
CloudGuardRegion = ty.Union[cloudguard.region.CloudGuardRegion, str]
