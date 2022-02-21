##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os


class Axlstar(CMakePackage):
    """Axl generator: a xml based code generator for Alien and Arcane."""

    homepage = "https://arcaneframework.github.io"
    url = "https://github.com/arcaneframework/framework/releases/download/axlstar-v2.0.0.0/axlstar-2.0.0.0.src.tar.gz"
    git = "https://github.com/arcaneframework/framework.git"

    version("main", branch="main")

    version(
        '2.0.0.0',
        sha256='0f41c6b3af8344ce1fec030069559448f8267f87a4b05f9b8c247a8c27d49e42'
    )  # noqa: E501

    version(
        '2.0.1.0',
        sha256='db50f561f54840faa886e67d2d85dfbfcd3c5a3cddd7f4b5365138e545d73e3d'
    )  # noqa: E501

    depends_on("cmake@3.12:", type=("build", ))
    depends_on("arccon@1.2:", type=("build", ))
    depends_on("arcdependencies", type=("build"))
    depends_on("dotnet-core-sdk@3.1:", type=("build", "link", "run"))
