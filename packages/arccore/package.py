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
#############################################################################
from spack import *


class Arccore(CMakePackage):
    """Base functionalities for simulation codes."""

    homepage = "https://arcaneframework.github.io"
    url = "https://github.com/arcaneframework/framework/releases/download/arccore-v2.0.3.0/arccore-2.0.3.0.src.tar.gz"
    git = "https://github.com/arcaneframework/framework.git"

    variant(
        "build_mode",
        default="Release",
        description="Arccore build type",
        values=("Debug", "Check", "Release"),
    )

    version(
        "2.0.0",
        sha256="fd385c961ca333757575a93bf1dbfe9417b8c3ff83d2d1956b5d4ed432c9bedc",
        url="https://gitlab.com/cea-ifpen/arccore/-/archive/v2.0.0/arccore-v2.0.0.tar.gz",
    )
    version(
        "2.0.1",
        sha256="d06508ff14d7f2b5e277fa5fc788eb7fd891886d7ffd65bee41c6a12d2ec58ae",
        url="https://gitlab.com/cea-ifpen/arccore/-/archive/v2.0.1/arccore-v2.0.1.tar.gz",
    )
    version(
        "2.0.3.0",
        sha256="fb7678038234fe4dcbde364459a4fc91b737c7ffb6151ad634def9edf2e18705",
    )
    version(
        "2.0.4.0",
        sha256="d0af126861343305011f643f1fcf6311ba1f822ff4d5edb8956b55cb004341a2",
    )
    version(
        "2.0.6.0",
        sha256="9780d48833b0fb8af9744903192ecd828eb94ea03171c484318d35a32055720e",
    )
    version(
        "2.0.8.1",
        sha256="5ed26a0d129234ba26140b025e2c63683d6c310f13fd400b046ab3d2318b4f72",
    )
    version(
        "2.0.9.0",
        sha256="9a0918c9c4c448f56498b45d7369499baa9073dec32f472d9c744626fb847afb",
    )
    version(
        "2.0.11.0",
        sha256="bd8514dc9490b91fe8b1662edefb6ad847a01e096c5c6a03e02e45b9a1194e99",
    )

    variant("mpi", default=True, description="Use MPI")

    # Arccon must be exported to client
    depends_on("arccon", type=("build", "link"))
    depends_on("cmake@3.18:", type="build")
    depends_on("glib")
    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define_from_variant("ARCCORE_USE_MPI", "mpi"),
        ]

        args.append(self.define_from_variant("ARCCORE_BUILD_MODE", "build_mode"))

        if "build_mode=Debug" in self.spec or "build_mode=Check" in self.spec:
            args.append(self.define("ARCCORE_CHECK", True))
        if "build_mode=Debug" in self.spec:
            args.append(self.define("ARCCORE_DEBUG", True))

        return args
