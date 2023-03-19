# cloudguard/config.py
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
import os
import typing as ty
import logging
import dataclasses as dc
import configparser

from pathlib import Path

import xdg

import cloudguard.region
import cloudguard.typing as cgty
import cloudguard.credentials

from cloudguard.utils import Namespace
from cloudguard.errors import ConfigParseError


log = logging.getLogger(__name__)


#: Name of the environment variable providing the CloudGuard API key.
ENV_CLOUDGUARD_API_KEY: str = "CLOUDGUARD_API_KEY"
#: Name of the environment variable providing the CloudGuard API secret.
ENV_CLOUDGUARD_API_SECRET: str = "CLOUDGUARD_API_SECRET"
#: Name of the environment variable providing the path to CloudGuard's
#: configuration.
ENV_CLOUDGUARD_CONFIG: str = "CLOUDGUARD_CONFIG"
#: Name of the environment variable providing the path to CloudGuard's
#: credentials file.
ENV_CLOUDGUARD_CREDENTIALS: str = "CLOUDGUARD_CREDENTIALS"
#: Name of the environment variable providing the CloudGuard region.
ENV_CLOUDGUARD_REGION: str = "CLOUDGUARD_REGION"

#: Name of the directory holding CloudGuard's configuration.
CLOUDGUARD_CONFIG_DIR_NAME: str = "cloudguard"
#: Path to the configuration file.
CLOUDGUARD_CONFIG_PATH: Path = (
    xdg.xdg_config_home() / CLOUDGUARD_CONFIG_DIR_NAME / "config"
)
#: Path to the credentials file.
CLOUDGUARD_CREDENTIALS_PATH: Path = CLOUDGUARD_CONFIG_PATH.with_name("credentials")


class Credentials(Namespace):
    """Namespace holding CloudGuard credentials."""

    @classmethod
    def load(cls) -> ty.Self:
        """Load credentials from the default file locations or the environment
        variables.


        :return: A new :class:`~cloudguard.config.Credentials` class based on
                 the existing environment.
        :rtype: ~cloudguard.config.Credentials


        :raise ~cloudguard.config.ConfigParseError:
            When the configuration file could not be read as a valid
            configuration.

        """
        self = cls.load_from_file()
        self.update(cls.load_from_env())

        return self

    @classmethod
    def load_from_env(cls) -> ty.Self:
        """Load credentials from the environment variables.


        :return: A new :class:`~cloudguard.config.Credentials` class based on
                 the defined environment.
        :rtype: ~cloudguard.config.Credentials

        """
        self = cls()
        if (api_key := os.environ.get(ENV_CLOUDGUARD_API_KEY)) is not None:
            self.api = cloudguard.credentials.APICredentials(
                key=api_key,
                secret=os.environ.get(ENV_CLOUDGUARD_API_SECRET),
            )

        return self

    @classmethod
    def load_from_file(cls, credentials: ty.Optional[os.PathLike] = None) -> ty.Self:
        """Load credentials from a file.


        :param credentials: Path to the file from which to load the credentials.
        :type credentials: ~os.PathLike


        :return: A new :class:`~cloudguard.config.Credentials` class based on
                 the file content.
        :rtype: ~cloudguard.config.Credentials


        :raise ~cloudguard.config.ConfigParseError:
            When the credentials file could not be read as a valid
            configuration.

        """
        if credentials is None:
            credentials = (
                os.environ.get(ENV_CLOUDGUARD_CREDENTIALS)
                or CLOUDGUARD_CREDENTIALS_PATH
            )

        raw = {}
        try:
            raw = parse_raw_config(credentials)
        except OSError:
            log.warning(f"Could not read credentials at: {credentials or ''}")
        except TypeError:
            pass

        self = cls()
        if (api_key := (raw.get("default") or {}).get("api_key")) is not None:
            self.api = cloudguard.credentials.APICredentials(
                key=api_key,
                secret=(raw.get("default") or {}).get("api_secret"),
            )

        return self


@dc.dataclass(init=False, repr=False)
class Config(object):
    """Configuration of the CloudGuard client.


    :param credentials: A :class:`~cloudguard.config.Credentials` object listing
                        all the CloudGuard credentials.
    :type credentials: ~cloudguard.config.Credentials

    :param region: The region to use when instantiating the client.
    :type region: ~typing.Union[str, ~cloudguard.region.CloudGuardRegion]

    """

    __region: ty.Optional[cloudguard.region.CloudGuardRegion] = dc.field(
        default=None, init=False, metadata={"name": "region"}
    )
    #: Store holding the different authentication credentials required to
    #: interact with CloudGuard.
    credentials: Credentials = dc.field(default_factory=Credentials)

    def __init__(self, **kwargs):
        """Constructor for :class:`cloudguard.config.Config`."""
        allowed = {x.metadata.get("name") or x.name for x in dc.fields(self)}
        for k, v in kwargs.items():
            if k not in allowed:
                raise TypeError(
                    f"{self.__class__.__name__}() got an unexpected keyword argument '{k}'"
                )
            setattr(self, k, v)

    def __repr__(self) -> str:
        """Formal representation of the :class:`cloudguard.config.Config`
        class.

        """
        return "".join(
            (
                self.__class__.__name__,
                "(",
                ", ".join(
                    f"{f}={getattr(self, f)}"
                    for f in {x.metadata.get("name") or x.name for x in dc.fields(self)}
                ),
                ")",
            )
        )

    @classmethod
    def load(cls) -> ty.Self:
        """Load a configuration from the default file locations or the
        environment variables.


        :return: A new :class:`~cloudguard.config.Config` class based on the
                 existing environment.
        :rtype: ~cloudguard.config.Config


        :raise ~cloudguard.config.ConfigParseError:
            When the configuration file could not be read as a valid
            configuration.

        """
        self = cls.load_from_file()
        self.update(cls.load_from_env())
        self.credentials.update(Credentials.load())

        return self

    @classmethod
    def load_from_env(cls) -> ty.Self:
        """Load a configuration from the environment variables.


        :return: A new :class:`~cloudguard.config.Config` class based on the
                 defined environment.
        :rtype: ~cloudguard.config.Config

        """
        self = cls()
        if (region := os.environ.get(ENV_CLOUDGUARD_REGION)) is not None:
            self.region = region

        return self

    @classmethod
    def load_from_file(cls, config: ty.Optional[os.PathLike] = None) -> ty.Self:
        """Load a configuration from a file.


        :param config: Path to the file from which to load the configuration.
        :type config: ~os.PathLike


        :return: A new :class:`~cloudguard.config.Config` class based on the
                 file content.
        :rtype: ~cloudguard.config.Config


        :raise ~cloudguard.config.ConfigParseError:
            When the configuration file could not be read as a valid
            configuration.

        """
        if config is None:
            config = os.environ.get(ENV_CLOUDGUARD_CONFIG) or CLOUDGUARD_CONFIG_PATH

        raw = {}
        try:
            raw = parse_raw_config(config)
        except OSError:
            log.warning(f"Could not read configuration at: {config or ''}")
        except TypeError:
            pass

        self = cls()
        self.update(raw.get("default") or {})

        return self

    @property
    def region(self) -> ty.Optional[cloudguard.region.CloudGuardRegion]:
        """Get the CloudGuard region.


        :return: The CloudGuard region.
        :rtype: ~cloudguard.region.CloudGuardRegion

        """
        return self.__region

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
        if value is None or isinstance(value, cloudguard.region.CloudGuardRegion):
            self.__region = value
        elif isinstance(value, str):
            try:
                self.__region = getattr(cloudguard.region, value)
            except AttributeError:
                raise ValueError(f"unknown region: {value}") from None
        else:
            raise TypeError(
                f"expected `{str!r}` or `{cloudguard.region.CloudGuardRegion!r}`"
                f" got: {type(value)}"
            )

    def update(self, other: ty.Union["Config", ty.Mapping[str, ty.Any]]) -> None:
        """Update the configuration from another configuration object or any
        config-like object. ``None`` values are ignored.


        :param other: The object from which to update the current configuration.
        :type other: ~typing.Union[~cloudguard.region.CloudGuardRegion, ~typing.Mapping[str, ty.Any]]


        :return: ``None``

        """
        for field in dc.fields(self):
            name = field.metadata.get("name") or field.name
            try:
                value = other[name]
            except (KeyError, TypeError):
                try:
                    value = getattr(other, name)
                except AttributeError:
                    continue
            if value is not None:
                setattr(self, name, value)


def parse_raw_config(name: os.PathLike) -> ty.Dict[str, ty.Dict[str, str]]:
    """Read a configuration file using :class:`~configparser.ConfigParser`. And
    return a dictionary from the parsed configuration.

    Each section is a top level key and each section item is an element in the
    section's dictionary.


    :param name: Path to the configuration file to parse.
    :type name: ~os.PathLike


    :return: A dictionary from the loaded configuration file.
    :rtype: ~typing.Dict[str, ~typing.Dict[str, str]]


    :raise ~cloudguard.config.ConfigParseError:
        When the configuration file could not be read as a valid configuration.

    """
    path = os.fspath(Path(name).expanduser())
    cp = configparser.RawConfigParser()
    try:
        cp.read(path)
    except (configparser.Error, UnicodeDecodeError):
        raise ConfigParseError(path=name) from None
    else:
        config = {}
        for section in cp.sections():
            config[section] = {}
            for option in cp.options(section):
                config[section][option] = cp.get(section, option)

        return config


#: Alias for :meth:`cloudguard.config.Config.load`.
load = Config.load
#: Alias for :meth:`cloudguard.config.Config.load_from_env`.
load_from_env = Config.load_from_env
#: Alias for :meth:`cloudguard.config.Config.load_from_file`.
load_from_file = Config.load_from_file
