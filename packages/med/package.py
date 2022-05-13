# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Med(CMakePackage):
    """The MED file format is a specialization of the HDF5 standard."""

    homepage = "http://docs.salome-platform.org/latest/dev/MEDCoupling/med-file.html"
    url = "http://files.salome-platform.org/Salome/other/med-4.0.0.tar.gz"

    maintainers = ["likask"]

    version(
        "4.0.0",
        sha256="a474e90b5882ce69c5e9f66f6359c53b8b73eb448c5f631fa96e8cd2c14df004",
    )

    # variant('api23', default=True, description='Enable API2.3')

    depends_on("mpi")
    depends_on("hdf5@:1.10+mpi")

    # FIXME This is minimal installation.

    def cmake_args(self):
        spec = self.spec

        options = []

        options.extend(
            [
                "-DMEDFILE_USE_MPI=YES"
                "-DMEDFILE_BUILD_TESTS={0}".format("ON" if self.run_tests else "OFF"),
                "-DMEDFILE_BUILD_PYTHON=OFF",
                "-DMEDFILE_INSTALL_DOC=OFF",
                "-DMEDFILE_BUILD_SHARED_LIBS=ON",
                "-DMEDFILE_BUILD_STATIC_LIBS=OFF",
                "-DCMAKE_Fortran_COMPILER=",
            ]
        )

        options.extend(
            [
                "-DHDF5_ROOT_DIR=%s" % spec["hdf5"].prefix,
                "-DMPI_ROOT_DIR=%s" % spec["mpi"].prefix,
            ]
        )

        return options
