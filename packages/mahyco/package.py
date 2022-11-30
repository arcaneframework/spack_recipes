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


class Mahyco(CMakePackage):
    """MaHyCo: Generic API for Linear Algebra."""

    homepage = "https://github.com/cea-hpc/MaHyCo"
    git = "https://github.com/cea-hpc/MaHyCo.git"

    version("master", branch="master")
    version("develop", branch="Mahyco_gpu2")

    variant("cuda", description="Enable CUDA offloading", default=False)
    variant(
        "arcane_cartesian", description="Use Arcane/cea cartesian mesh", default=False
    )
    variant("cuda_prof", description="Enable GPU profiling", default=False)

    depends_on("arcane@3.7")
    depends_on("arcane +cuda", when="+cuda")

    def cmake_args(self):
        return [
            self.define_from_variant("WANT_CUDA", "cuda"),
            self.define_from_variant("WANT_IMPL_CART_ARCANE", "arcane_cartesian"),
            self.define_from_variant("WANT_PROF_ACC", "cuda_prof"),
        ]
