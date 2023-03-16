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


@dc.dataclass(frozen=True)
class CloudGuardRegion(object):
    """Specification of CloudGuard resource locations for a given region."""

    #: Friendly name of the CloudGuard region.
    name: str
    #: Code assigned to the CloudGuard region.
    code: str
    #: URL to access the CloudGuard API.
    api: str
