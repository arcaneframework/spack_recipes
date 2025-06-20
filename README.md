# spack_recipes

Spack recipes for Arcane Framework.

Beginning with version 3.16 of Arcane Framework, the package is named
`arcane-framework`. Before this version, the package is named `arcane`.

This recipe has been tested with Spack version `1.0` but may work with Spacek version `0.23`

Before using spack, you have to add this directory to the spack repo list with the following command:

```{.sh}
spack repo add /path/to/this/repository
```

To compile Arcane in Debug mode:

```{.sh}
spack install arcane-framework +arcane build_type=Debug
```

To compile Arcane in Check mode:

```{.sh}
spack install arcane-framework +arcane build_mode=Check
```

To compile Arcane in Release mode:

```{.sh}
spack install arcane-framework +arcane build_mode=Release
```

To compile Arcane with Alien

```{.sh}
spack install arcane-framework +arcane +alien
```

To compile only Alien

```{.sh}
spack install arcane-framework ~arcane +alien
```

To compile only Arccore

```{.sh}
spack install arcane-framework ~arcane
```

To compile Arcane using GCC with CUDA support using Clang as CUDA compiler

```{.sh}
spack install arcane-framework  build_type=Debug +arcane ~mpi ~hdf5 ~dotnet_wrapper cuda_arch=75 +cuda +cuda_clang %gcc
```
