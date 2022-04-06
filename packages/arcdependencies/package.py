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


class Arcdependencies(CMakePackage):
    """Dependencies for Arccon/Arccore/Axlstar."""

    homepage = "https://arcaneframework.github.io"
    git = "https://github.com/arcaneframework/dependencies.git"
    url = "https://github.com/arcaneframework/dependencies/archive/refs/tags/v1.2.0.tar.gz"

    version(
        '1.2.0',
        sha256='86a95610d38e440ecffc18de4c7e38073b517446286acc0ecc62639898c23a1d'
    )  # noqa: E501

    version("main", branch="main")

    depends_on("cmake@3.12:", type=("build", "link"))
    depends_on("arccon", type=("build"))
