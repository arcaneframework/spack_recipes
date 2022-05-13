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


class Arccon(CMakePackage):
    """A CMake build system for HPC simulation codes."""

    homepage = "https://arcaneframework.github.io"
    url = "https://github.com/arcaneframework/framework/releases/download/arccon-v1.2.0/arccon-1.2.0.src.tar.gz"
    git = "https://github.com/arcaneframework/framework.git"

    version(
        "1.0.0",
        sha256="1f276325251c407c141cb6b5e223f06ac7ef41f128714d5d98d27b5d41b0dbcc",
        url="https://gitlab.com/cea-ifpen/arccon/-/archive/v1.0.0/arccon-v1.0.0.tar.bz2",
    )
    version(
        "1.1.0",
        sha256="34434f8fdd21dc72668bdb02c77a917357d467c0646b9338199492d02c3681f5",
        url="https://gitlab.com/cea-ifpen/arccon/-/archive/v1.1.0/arccon-v1.1.0.tar.bz2",
    )
    version(
        "1.2.0",
        sha256="bdea35e4c559c85cca7bd82d1a9d8859c465832c645baa127595952131933002",
    )

    version("main", branch="main")

    # FIXME: Add dependencies if required.
    depends_on("cmake@3.11:", type=("build", "link"))
