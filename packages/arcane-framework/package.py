from spack.package import *

class ArcaneFramework(CMakePackage, CudaPackage, ROCmPackage):
    """Arcane Framework"""

    homepage = "https://arcaneframework.github.io"

    url = "https://github.com/arcaneframework/framework/releases/download/arcane-v3.11.15.0/framework-3.11.15.0.src.tar.gz"
    git = "https://github.com/arcaneframework/framework.git"

    version("3.16.6.0", commit="637f8cae62c307a7d47c6b67635746957679c62d", submodules = True)

    generator("ninja")

    variant(
        "build_mode",
        default="Release",
        description="Arccore build type",
        values=("Debug", "Check", "Release"),
    )

    variant("arcane", default=True, description="Compile the component 'Arcane'")
    variant("alien", default=False, description="Compile the component 'Alien'")
    variant("mpi", default=True, description="Use MPI")

    variant("hdf5", default=True, description="HDF5 IO")
    variant("tbb", default=True, description="Use Intel TBB")
    variant("dotnet_wrapper", default=True, when="+arcane", description=".Net wrappers")
    variant("lz4", default=True, when="+arcane", description="Use lz4 compression")

    variant("valgrind", default=False, description="Add support for running tests with valgrind")
    variant("med", default=False, when="+arcane", description="Salome MED support")
    variant("otf2", default=False, when="+arcane", description="OTF2 library support")
    variant("mkl", default=False, description="Use Intel MKL")
    variant("bzip2", default=False, when="+arcane", description="Use bzip2 compression")

    variant("parmetis", default=True, when="+arcane", description="Use ParMetis partitioner")
    variant("scotch", default=False, when="+arcane", description="Use (PT-)Scotch partitioner")
    variant("zoltan", default=False, when="+arcane", description="Use Zoltan partitioner")

    variant("libunwind", default=True, when="+arcane", description="Back trace with libUnwind")
    variant("hwloc", default=True, when="+arcane", description="hwloc support")

    variant("udunits", default=False, when="+arcane", description="Udunits")
    variant("papi", default=False, when="+arcane", description="PAPI counters")

    variant("build_tests", default=True, description="Compile tests")

    variant("cuda_clang", default=False, description="Use clang (instead of nvcc) to compile CUDA code")

    depends_on("c", type="build", when="+arcane")
    # TOOD: check if alien needs 'C' language
    depends_on("c", type="build", when="+alien")
    depends_on("cxx", type="build")

    # TODO: handle the dependencies of this variant
    depends_on("blas", when="+alien")
    depends_on("boost +program_options", when="+alien")
    depends_on("fortran", type="build", when="+alien")

    depends_on("cmake@3.26:", type="build")

    # TODO: Handle variants for alien standalone and alien with arcane
    # For example, alien standalone does not depend on 'libxml2'
    depends_on("dotnet-core-sdk@8:", type=("build", "link", "run"), when="+arcane")
    depends_on("libxml2", when="+arcane")
    depends_on("dotnet-core-sdk@8:", type=("build", "link", "run"), when="+alien")
    depends_on("libxml2", when="+alien")

    depends_on("glib")
    depends_on("valgrind", when="+valgrind")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5@1.10:", when="+hdf5")
    depends_on("intel-tbb@2021:", when="+tbb")
    depends_on("mkl", when="+mkl")
    depends_on("bzip2", when="+bzip2")
    depends_on("lz4", when="+lz4")
    depends_on("med", when="+med")
    depends_on("otf2", when="+otf2")
    depends_on("swig@4:", type=("build"), when="+dotnet_wrapper")

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
    variant("hypre", default=False, description="hypre linear solver (for Aleph)")
    depends_on("hypre", when="+hypre")
    variant("trilinos", default=False, description="Trilinos linear solver (for Aleph)")
    depends_on("trilinos +aztec+ml+ifpack", when="+trilinos")
    depends_on("trilinos +zoltan", when="+zoltan+trilinos")
    variant("petsc", default=False, description="PETSc linear solver (for Aleph)")
    depends_on("petsc +mpi", when="+petsc")

    depends_on("cuda", when="+cuda")
    depends_on("hip", when="+rocm")
    conflicts("+cuda", when="+rocm")

    depends_on("llvm+clang+cuda", when="+cuda +cuda_clang")

    def build_required(self):
        to_cmake = {
            "mpi": "MPI",
            "hdf5": "HDF5",
            "bzip2": "BZip2",
            "lz4": "LZ4",
            "med": "MEDFile",
            "tbb": "TBB",
            "mkl": "MKL",
            "otf2": "Otf2",
            "cuda": "CUDAToolkit",
            "rocm": "Hip",
            "parmetis": "Parmetis",
            "scotch": "PTScotch",
            "zoltan": "Zoltan",
            "libunwind": "LibUnwind",
            "udunits": "Udunits",
            "valgrind": "Valgrind",
            "hwloc": "HWLoc",
            "papi": "Papi",
            "hypre": "Hypre",
            "trilinos": "Trilinos",
            "lima": "Lima",
            "dotnet_wrapper": ["SWIG", "CoreClrEmbed"]
        }
        return ";".join(
            map(
                lambda v: v[1] if not isinstance(v[1], list) else ";".join(v[1]),
                filter(lambda v: "+{}".format(v[0]) in self.spec, to_cmake.items()),
            )
        )

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("ARCCORE_CXX_STANDARD", "20"),
            self.define("ARCANE_BUILD_WITH_SPACK", True),
            self.define("ARCANE_NO_DEFAULT_PACKAGE", True),
            self.define("ARCANE_NO_DEFAULT_PACKAGE", True),
            self.define("ARCANEFRAMEWORK_BUILD_COMPONENTS", "Arcane"),
            self.define("ARCANE_DISABLE_DEPRECATED_WARNINGS", "TRUE"),
            self.define_from_variant("ARCCORE_USE_MPI", "mpi"),
            self.define_from_variant("ARCCORE_BUILD_MODE", "build_mode"),
            self.define_from_variant("ARCANE_ENABLE_TESTS", "build_tests"),
            self.define_from_variant("ARCANE_ENABLE_DOTNET_WRAPPER", "dotnet_wrapper"),
        ]

        # List of components to build
        components_to_build = "Arccore"
        if "+arcane" in self.spec:
            components_to_build = components_to_build + ";" + "Arcane"
        if "+alien" in self.spec:
            components_to_build = components_to_build + ";" + "Alien"
        args.append(self.define("ARCANEFRAMEWORK_BUILD_COMPONENTS", components_to_build))

        default_partitionner = "Auto"
        args.append(self.define("ARCANE_DEFAULT_PARTITIONER", default_partitionner))
        args.append(self.define("ARCANE_REQUIRED_PACKAGE_LIST", self.build_required()))

        if "+alien" in self.spec:
            self.define("ALIEN_DEFAULT_OPTIONS", False),
            self.define_from_variant("ALIEN_PLUGIN_HYPRE", "hypre"),

        if "+rocm" in self.spec:
            args.append(self.define("ARCANE_ACCELERATOR_MODE", "ROCM"))
            amd_arch = self.spec.variants["amdgpu_target"].value
            if amd_arch:
                args.append(self.define("CMAKE_HIP_ARCHITECTURES", ";".join(amd_arch)))
        elif "+cuda" in self.spec:
            args.append(self.define("ARCANE_ACCELERATOR_MODE", "CUDA"))
            # Experimental: use clang to compile CUDA code
            if "+cuda_clang" in self.spec:
                args.append(self.define("CMAKE_CUDA_COMPILER", join_path(self.spec["llvm"].prefix.bin, "clang++")))

            cuda_arch = self.spec.variants["cuda_arch"].value
            if cuda_arch:
                args.append(
                    self.define("CMAKE_CUDA_ARCHITECTURES", ";".join(cuda_arch))
                )

        return args
