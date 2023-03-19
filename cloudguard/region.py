# cloudguard/region.py
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
import dataclasses as dc

from httpx import URL


@dc.dataclass(frozen=True)
class CloudGuardRegion(object):
    """Specification of CloudGuard resource locations for a given region."""

    #: Friendly name of the CloudGuard region.
    name: str
    #: Code assigned to the CloudGuard region.
    code: str
    #: URL to access the CloudGuard API.
    api: URL


#: CloudGuard region, Australia (``ap2``).
Australia = CloudGuardRegion(
    name="Australia",
    code="ap2",
    api=URL("https://api.ap2.dome9.com/"),
)

#: CloudGuard region, Canada (``cace1``).
Canada = CloudGuardRegion(
    name="Canada",
    code="cace1",
    api=URL("https://api.cace1.dome9.com/"),
)

#: CloudGuard region, India (``ap3``).
India = CloudGuardRegion(
    name="India",
    code="ap3",
    api=URL("https://api.ap3.dome9.com/"),
)

#: CloudGuard region, Ireland (``eu1``).
Ireland = CloudGuardRegion(
    name="Ireland",
    code="eu1",
    api=URL("https://api.eu1.dome9.com/"),
)

#: CloudGuard region, Singapore (``ap1``).
Singapore = CloudGuardRegion(
    name="Singapore",
    code="ap1",
    api=URL("https://api.ap1.dome9.com/"),
)

#: CloudGuard region, United States (``us``).
UnitedStates = CloudGuardRegion(
    name="United States",
    code="us",
    api=URL("https://api.dome9.com/"),
)

#: Alias to the Singapore CloudGuard region.
ap1 = Singapore
#: Alias to the Australia CloudGuard region.
ap2 = Australia
#: Alias to the India CloudGuard region.
ap3 = India
#: Alias to the Canada CloudGuard region.
cace1 = Canada
#: Alias to the Ireland CloudGuard region.
eu1 = Ireland
#: Alias to the United States CloudGuard region.
us = UnitedStates
