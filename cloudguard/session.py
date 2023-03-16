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
from cloudguard.config import Config


class Session(object):
    """The session consolidates in a single place everything required to
    communicate with the CloudGuard API.

    """

    def __init__(self, *args, **kwargs):
        """Constructor for :class:`cloudguard.session.Session`."""
        self.config = Config.load()


class AsyncSession(Session):
    """The asynchronous session is to be used in a concurrent runtime."""

    pass
