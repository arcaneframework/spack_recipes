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


class Alien(CMakePackage):
    """Alien: Generic API for Linear Algebra."""

    homepage = "https://arcaneframework.github.io/alien"
    url = "https://github.com/arcaneframework/alien/archive/refs/tags/v1.0.3.tar.gz"
    git = "https://github.com/arcaneframework/alien.git"

    version(
        "1.0.1",
        sha256="ac8360f0fe80937397e9aaa5980236ea5338ae7b5b2ad5278cf463a35e41277c",
        url="https://gitlab.com/cea-ifpen/alien/-/archive/v1.0.1/alien-v1.0.1.tar.gz",
    )
    version(
        "1.0.2",
        sha256="4191972e89bf61d7130278c2c892f638aeab27f96b920c1fb122f86251fbbfa5",
        url="https://gitlab.com/cea-ifpen/alien/-/archive/v1.0.2/alien-v1.0.2.tar.gz",
    )

    version(
        "1.1.0",
        sha256="e0250eb5983dd4703a9d498951bdbc7da52c0271ac7f1e0149ceeabb21da06e0",
    )
    version(
        "1.1.1",
        sha256="8be37135b26521e30bd3a4db4f4182b230d1292759420484d7ce194fbe40e8dc",
    )
    version(
        "1.1.2",
        sha256="3246becbc665106f0efdabd0ed836421d04133a703affda64c64ad94f36eea57",
    )
    version(
        "1.1.3",
        sha256="36b5aeabc5c1f2a80d7f4943796c179b88b54164e3eada6113027fbf35936f37",
    )

    variant("hdf5", description="hdf5 export for Alien", default=False)
    variant("xml", description="xml export for Alien", default=True)
    variant("move", description="Move Semantic api for Alien", default=True)
    variant("ref", description="Ref Semantic api for Alien", default=True)

    variant("hypre", description="Enable hypre backend", default=False)
    variant("petsc", description="Enable PETSc backend", default=False)

    ginkgo_backends = ("omp", "ref", "cuda", "hip", "dpcpp")
    variant(
        "ginkgo",
        description="Enable Ginkgo specific backend",
        default="none",
        values=ginkgo_backends + ("none",),
        multi=False,
        when="@1.1.3:",
    )

    trilinos_backends = ("omp", "ref", "cuda", "hip")
    variant(
        "trilinos",
        description="Enable Trilinos specific backend",
        default="none",
        values=trilinos_backends + ("none",),
        multi=False,
        when="@1.1.4:",
    )

    depends_on("hypre +mpi", when="+hypre")
    depends_on("petsc +mpi", when="+petsc")

    depends_on("ginkgo +cuda", when="ginkgo=cuda")
    depends_on("ginkgo +openmp", when="ginkgo=omp")
    depends_on("ginkgo +rocm", when="ginkgo=hip")
    depends_on("ginkgo", when="ginkgo=ref")

    trilinos_variants = "+tpetra +kokkos +belos +ifpack2"
    depends_on("trilinos {}".format(trilinos_variants), when="trilinos=ref")
    depends_on("trilinos {} +cuda".format(trilinos_variants), when="trilinos=cuda")
    depends_on("trilinos {} +rocm".format(trilinos_variants), when="trilinos=hip")
    depends_on("trilinos {} +openmp".format(trilinos_variants), when="trilinos=omp")

    depends_on("cmake", type="build")

    # Exported build system depends on arccon, we must export it to the client
    depends_on("arccon", type=("build", "link"))

    depends_on("arccore", type=("build", "link"))
    depends_on("googletest", type=("build"))
    depends_on("boost +program_options")
    # depends_on("boost +context", when="+sycl")
    depends_on("blas")
    depends_on("mpi")
    depends_on("libxml2", when="+xml")
    depends_on("hdf5", when="+hdf5")

    def cmake_args(self):
        options = [
            # Do not use any default options for Alien
            self.define("ALIEN_DEFAULT_OPTIONS", False),
            self.define_from_variant("ALIEN_USE_HDF5", "hdf5"),
            self.define_from_variant("ALIEN_USE_XML", "xml"),
            self.define_from_variant("ALIEN_COMPONENT_MoveSemantic", "move"),
            self.define_from_variant("ALIEN_COMPONENT_RefSemantic", "ref"),
            self.define_from_variant("ALIEN_PLUGIN_HYPRE", "hypre"),
            self.define_from_variant("ALIEN_PLUGIN_PETSC", "petsc"),
            self.define("BUILD_SHARED_LIBS", True),
        ]

        def multivariant(plugin_name, active_options):
            alien_plugin_prefix = "ALIEN_PLUGIN_{}".format(plugin_name.upper())
            if "{}=none".format(plugin_name) in self.spec:
                options.append(self.define(alien_plugin_prefix, False))
            else:
                options.append(self.define(alien_plugin_prefix, True))
                for b in active_options:
                    if "{}={}".format(plugin_name, b) in self.spec:
                        options.append(
                            self.define(
                                "{}_{}".format(alien_plugin_prefix, b.upper()), True
                            )
                        )

        multivariant("ginkgo", self.ginkgo_backends)
        multivariant("trilinos", self.trilinos_backends)

        return options
