# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink
from spack import *

import platform

_versions = {
    "3.1.414": {
        "Linux-aarch64": (
            "42b526d4ae914a0f1b04cbefe70b2c052eae9791dce54431ee5aff2e1bba5dbd08f49505a835319dab0551e9e9788f239e53ac154760cc8c0a85512cbe568408",
            "https://dotnetcli.azureedge.net/dotnet/Sdk/3.1.414/dotnet-sdk-3.1.414-linux-arm64.tar.gz",
        ),
        "Linux-x86_64": (
            "f0a133a2bfbbdb6e3f35ad543bfd8e48f35e2a0e0bd719f712853d686e5f453b89569504813fde33baf8788dfe509bb3bc7ad69026588761f0a07362eac76104",
            "https://dotnetcli.azureedge.net/dotnet/Sdk/3.1.414/dotnet-sdk-3.1.414-linux-x64.tar.gz",
        ),
    },
    "6.0.102": {
        "Linux-aarch64": (
            "790cbf322ca8fed32eaf574f19d0bdc05656c5a88a65aa4dba8269cfce1443cd7cdeecdd3a40e353c368f055490b70592ca7f15f981a66c5b3a9517d0b09e4cb",
            "https://download.visualstudio.microsoft.com/download/pr/93dd8d1e-f2af-45b1-8e86-9b8c3d58f4d2/b3fc3ef9da1db691043387fcb56f4d6f/dotnet-sdk-6.0.102-linux-arm64.tar.gz",
        ),
        "Linux-x86_64": (
            "edd79ebad3327032ea0aaa8504c14e3270050bb459b098202676776b41a3a1d282aaefd1e5e8aa09ef7f7cf7c4601c4783a57112ff6e3d427507e8eec2bfb748",
            "https://download.visualstudio.microsoft.com/download/pr/e7acb87d-ab08-4620-9050-b3e80f688d36/e93bbadc19b12f81e3a6761719f28b47/dotnet-sdk-6.0.102-linux-x64.tar.gz",
        ),
    },
    "6.0.104": {
        "Linux-aarch64": (
            "91fa1114a656173a988aafd65c657c9498c34ef9145eac60b6feacc8a08f68538defeb38af472e2626ffd0669eb62140fdb1408771db0e2b63501baf2a646f29",
            "https://download.visualstudio.microsoft.com/download/pr/e61cf583-1e44-4ac5-a04f-5b59fda42ea7/df3853bb318af131f7eafa61f2b839b8/dotnet-sdk-6.0.104-linux-arm64.tar.gz",
        ),
        "Linux-x86_64": (
            "126f22f48cdbbf59ff21ac1a6cd354b4dab500cef372c42a7e4a9546c755ab6d1670a096be3c66f5fe80b6e2a5c31b16901a2c3ccbe928b501e25bb86339ec6c",
            "https://download.visualstudio.microsoft.com/download/pr/ecbf40a3-ec68-4d08-9240-17b8530731bf/56aed66e46a72269c29bc3cc0f94ffc8/dotnet-sdk-6.0.104-linux-x64.tar.gz",
        ),
    },
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

    variant(
        "telemetry", default=False, description="allow collection of telemetry data"
    )

    # Packages that use dotnet-core-sdk will use these variables.
    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Warning, these environment variables are not used outside spack!
        if "-telemetry" in self.spec:
            spack_env.set("DOTNET_CLI_TELEMETRY_OPTOUT", 1)
        # Avoid "Couldn't find a valid ICU package installed on the system."
        # else, we have to find a way to add a dependency to icu4c package.
        # It's the case on aarch64 platform or containerize RHEL8.
        spack_env.set("DOTNET_SYSTEM_GLOBALIZATION_INVARIANT", 1)

    def install(self, spec, prefix):
        mkdirp("bin")
        symlink("../dotnet", "bin/dotnet")
        install_tree(".", prefix)
