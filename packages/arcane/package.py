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


class Arcane(CMakePackage, CudaPackage, ROCmPackage):
    """Arcane Framework"""

    homepage = "https://arcaneframework.github.io"
    url = "https://github.com/arcaneframework/framework/releases/download/arcane-v3.0.5.0/arcane-3.0.5.0.src.tar.gz"
    git = "https://github.com/arcaneframework/framework.git"

    version(
        "3.0.1",
        sha256=
        "45afb7fadc9ae5ca430c72c9c73ca6ba46816092aca502d0266d9140fb47ef35",
        url=
        "https://gitlab.com/cea-ifpen/arcane/-/archive/v3.0.1/arcane-v3.0.1.tar.gz",
    )  # noqa: E501

    version(
        '3.0.5.0',
        sha256='24e0d1f2193aab2398a842d2e0cf9162c52d1d853e57feb60806085655a440d7'
    )  # noqa: E501

    version(
        '3.2.0.1',
        sha256='1b2d9bbea2bbae1a9cbafd5c127f3865871393dbac6a3f6e22b1b8764e435649'
    )  #noqa: E501

    version(
        '3.4.5.0',
        sha256='d2e2834a11a915a4c8a0a8993bd368ecefb4033f740168e7b7449dc17bca0860'
    )  # noqa: E501

    version(
        '3.5.7.0',
        sha256='bfd1cf924e83265981aafd40e31a27753ce5269bccf392289d046c5282247d29'
    )  # noqa: E501

    variant("valgrind", default=False, description="run tests with valgrind")
    variant("mpi", default=True, description="Use MPI")
    variant("hdf5", default=False, description="HDF5 IO")
    variant("med", default=False, description="Salome MED support")
    variant("otf2", default=False, description="OTF2 library support")
    variant("tbb", default=True, description="Use Intel TBB")
    variant("wrapper", default=True, description=".Net wrappers")

    variant("mkl", default=False, description="Use Intel MKL")
    variant("bzip2", default=False, description="Use bzip2 compression")
    variant("lz4", default=False, description="Use lz4 compression")
    variant("vtk", default=False, description="Use VTK XDMF")
    variant("osmesa", default=False, description="Use Mesa rendering")
    variant("iceT", default=False, description="Use IceT")

    variant("parmetis", default=False, description="Use ParMetis partitioner")
    variant("scotch", default=False, description="Use (PT-)Scotch partitioner")
    variant("zoltan", default=False, description="Use Zoltan partitioner")

    variant("libunwind",
            default=False,
            description="Back trace with libUnwind")
    variant("udunits", default=False, description="Udunits")
    variant("hwloc", default=True, description="hwloc support")
    variant("papi", default=False, description="PAPI counters")

    variant("coreclrembed",
            default=True,
            description="Use embedding with coreclr")
    variant("monoembed", default=True, description="Use embedding with mono")

    depends_on("cmake@3.18:", type="build")

    depends_on("arccon@1.1:", type=("build"), when="@:3.0.4")
    depends_on("arccon@1.2:", type=("build"), when="@3.0.5.0")
    depends_on("axlstar@2.0:", type=("build"))
    depends_on("arccore@2.0:", type=("build", "link", "run"), when="@:3.0.4")
    depends_on("arccore@2.0.3",
               type=("build", "link", "run"),
               when="@3.0.5:3.1")
    depends_on("arccore@2.0.6:", type=("build", "link", "run"), when="@3.2:")
    depends_on("arccore build_mode=Debug",
               type=("build", "link", "run"),
               when="build_type='Debug'")
    depends_on("arcdependencies", type=("build"))
    depends_on("mono@5.16:", type=("build", "link", "run"), when="+monoembed")
    depends_on("swig@4:", type=("build"), when="+wrapper")
    depends_on(
        "dotnet-core-sdk@3.1:",
        type=("build", "link", "run"),
    )
    depends_on("glib")
    depends_on("libxml2")
    depends_on("valgrind", when="+valgrind")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5", when="+hdf5")
    depends_on("intel-tbb", when="+tbb")
    depends_on("mkl", when="+mkl")
    depends_on("bzip2", when="+bzip2")
    depends_on("lz4", when="+lz4")
    depends_on("vtk", when="+vtk")
    depends_on("mesa", when="+osmesa")
    depends_on("icet", when="+iceT")
    depends_on("med", when="+med")
    depends_on("otf2", when="+otf2")

    depends_on("parmetis@4:", when="+parmetis")
    depends_on("scotch +mpi -metis +int64", when="+scotch")
    depends_on("zoltan +mpi -parmetis -fortran", when="+zoltan~trilinos")

    depends_on("libunwind", when="+libunwind")
    depends_on("udunits", when="+udunits")
    depends_on("hwloc", when="+hwloc")
    depends_on("papi", when="+papi")

    conflicts("+parmetis", when="~mpi")
    conflicts("+zoltan", when="~mpi")
    conflicts("+scotch", when="~mpi")
    conflicts("+med", when="~mpi")

    # To be moved
    # For Aleph
    variant("hypre",
            default=False,
            description="hypre linear solver (for Aleph)")
    depends_on("hypre", when="+hypre")
    variant("trilinos",
            default=False,
            description="Trilinos linear solver (for Aleph)")
    depends_on("trilinos +aztec+ml+ifpack", when="+trilinos")
    depends_on("trilinos +zoltan", when="+zoltan+trilinos")
    variant("petsc",
            default=False,
            description="PETSc linear solver (for Aleph)")
    depends_on("petsc +mpi", when="+petsc")

    depends_on('cuda', when='+cuda')
    depends_on('hip', when='+rocm')
    depends_on('cmake@3.21:', when='+rocm')
    conflicts('+cuda', when='+rocm')

    def build_required(self):
        to_cmake = {
            'mpi': 'MPI',
            'hdf5': 'HDF5',
            'bzip2': 'BZip2',
            'lz4': 'LZ4',
            'med': 'MEDFile',
            'tbb': 'TBB',
            'vtk': ['vtkIOXML', 'vtkIOXdmf2'],
            'mkl': 'MKL',
            'otf2': 'Otf2',
            'osmesa': 'OSMesa',
            'iceT': 'IceT',
            'cuda': 'CUDAToolkit',
            'rocm': 'Hip',
            'parmetis': 'Parmetis',
            'scotch': 'PTScotch',
            'zoltan': 'Zoltan',
            'libunwind': 'LibUnwind',
            'udunits': 'Udunits',
            'valgrind': 'Valgrind',
            'hwloc': 'HWLoc',
            'papi': 'Papi',
            'sloop': 'Sloop',
            'hypre': 'Hypre',
            'trilinos': 'Trilinos',
            'lima': 'Lima',
            'wrapper': 'SWIG',
            'monoembed': 'MonoEmbed',
            'coreclrembed': 'CoreClrEmbed',
        }
        return ';'.join(
            map(
                lambda v: v[1]
                if not isinstance(v[1], list) else ";".join(v[1]),
                filter(lambda v: '+{}'.format(v[0]) in self.spec,
                       to_cmake.items())))

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("ARCANE_BUILD_WITH_SPACK", True),
            self.define("ARCANE_NO_DEFAULT_PACKAGE", True),
            self.define_from_variant("ARCANE_BUILD_MODE", "build_type"),
        ]
        if "mpi" in self.spec:
            args.append("-DARCANE_WANT_NOMPI=NO")
        else:
            args.append("-DARCANE_WANT_NOMPI=YES")

        default_partitionner = "Metis"
        if "metis" in self.spec:
            default_partitionner = "Metis"
        elif "scotch" in self.spec:
            default_partitionner = "PTScotch"
        elif "zoltan" in self.spec:
            default_partitionner = "Zoltan"

        args.append(
            self.define("ARCANE_DEFAULT_PARTITIONER", default_partitionner))

        args.append(
            self.define('ARCANE_REQUIRED_PACKAGE_LIST', self.build_required()))

        if '+rocm' in self.spec:
            args.append(self.define('ARCANE_ACCELERATOR_MODE', 'ROCMHIP'))
            amd_arch = self.spec.variants['amdgpu_target'].value
            if amd_arch:
                args.append(
                    self.define('CMAKE_HIP_ARCHITECTURES', ";".join(amd_arch)))
        elif '+cuda' in self.spec:
            args.append(self.define('ARCANE_ACCELERATOR_MODE', 'CUDANVCC'))
            cuda_arch = self.spec.variants['cuda_arch'].value
            if cuda_arch:
                args.append(
                    self.define('CMAKE_CUDA_ARCHITECTURES',
                                ";".join(cuda_arch)))

        return args
