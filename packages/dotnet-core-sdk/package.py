# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink
from spack import *

import platform

_versions = {
    '3.1.414': {
        'Linux-aarch64':
        ('42b526d4ae914a0f1b04cbefe70b2c052eae9791dce54431ee5aff2e1bba5dbd08f49505a835319dab0551e9e9788f239e53ac154760cc8c0a85512cbe568408',
         'https://dotnetcli.azureedge.net/dotnet/Sdk/3.1.414/dotnet-sdk-3.1.414-linux-arm64.tar.gz'
         ),
        'Linux-x86_64':
        ('f0a133a2bfbbdb6e3f35ad543bfd8e48f35e2a0e0bd719f712853d686e5f453b89569504813fde33baf8788dfe509bb3bc7ad69026588761f0a07362eac76104',
         'https://dotnetcli.azureedge.net/dotnet/Sdk/3.1.414/dotnet-sdk-3.1.414-linux-x64.tar.gz'
         )
    }
}


class DotnetCoreSdk(Package):
    """The .NET Core SDK is a powerful development environment to write
    applications for all types of infrastructure."""

    homepage = "https://www.microsoft.com/net/"
    git = "https://github.com/dotnet/core.git"
    # From https://github.com/dotnet/dotnet-docker/blob/main/src/sdk/3.1/focal/amd64/Dockerfile
    url = "https://dotnetcli.azureedge.net/dotnet/Sdk/3.1.414/dotnet-sdk-3.1.414-linux-x64.tar.gz"

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha512=pkg[0], url=pkg[1])

    variant('telemetry',
            default=False,
            description='allow collection of telemetry data')

    def setup_environment(self, spack_env, run_env):
        # Warning, these environment variables are not used outside spack!
        if '-telemetry' in self.spec:
            spack_env.set('DOTNET_CLI_TELEMETRY_OPTOUT', 1)
        # Avoid "Couldn't find a valid ICU package installed on the system."
        # else, we have to find a way to add a dependency to icu4c package.
        spack_env.set('DOTNET_SYSTEM_GLOBALIZATION_INVARIANT', 1)

    def install(self, spec, prefix):
        mkdirp('bin')
        symlink('../dotnet', 'bin/dotnet')
        install_tree(".", prefix)
