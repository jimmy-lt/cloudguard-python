# cloudguard/__init__.py
# ======================
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
import asyncio
import logging

from cloudguard.session import Session, AsyncSession


#: The default CloudGuard session.
_DEFAULT_SESSION: ty.Optional[ty.Union[AsyncSession, Session]] = None


def default_session() -> ty.Union[AsyncSession, Session]:
    """Get the SDK's default session.


    :returns: The session used by the SDK by default.
    :rtype: ~typing.Union[~cloudguard.session.Session, ~cloudguard.session.AsyncSession]

    """
    if _DEFAULT_SESSION is None:
        setup_default_session()
    return _DEFAULT_SESSION


def session(
    force_async: bool = False, force_sync: bool = False, *args, **kwargs
) -> ty.Union[AsyncSession, Session]:
    """Create a new CloudGuard session. By default, when an asynchronous runtime
    is detected, an asynchronous session is returned. This can be changed by the
     ``force_async`` or ``force_sync`` parameters.

     Any other parameters are provided to the session's constructor.


    :param force_async: Force the returned session to be asynchronous.
    :type force_async: bool

    :param force_sync: Force the returned session to be synchronous.
    :type force_sync: bool


    :returns: A CloudGuard session.
    :rtype: ~typing.Union[~cloudguard.session.Session, ~cloudguard.session.AsyncSession]

    """
    if force_async and force_sync:
        raise ValueError("`force_async` and `force_sync` cannot be set both.")
    if force_async:
        return AsyncSession(*args, **kwargs)
    if force_sync:
        return Session(*args, **kwargs)

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return Session(*args, **kwargs)
    else:
        return AsyncSession(*args, **kwargs)


def setup_default_session(*args, **kwargs) -> None:
    """Set up the SDK's default session. All parameters are provided to the
    session maker.

    """
    global _DEFAULT_SESSION
    _DEFAULT_SESSION = session(*args, **kwargs)


# Ensure that the library does not emit log messages.
# See: https://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger("cloudguard").addHandler(logging.NullHandler())
