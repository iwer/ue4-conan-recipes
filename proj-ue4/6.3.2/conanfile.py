from conans import ConanFile, CMake, tools

class ProjUe4Conan(ConanFile):
    name = "proj-ue4"
    version = "6.3.2"
    license = "MIT"
    url = "https://github.com/adamrehn/ue4-conan-recipes/proj-ue4"
    description = "PROJ custom build for Unreal Engine 4"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = (
        "libcxx/ue4@adamrehn/profile",
        "ue4util/ue4@adamrehn/profile"
    )
    
    def requirements(self):
        self.requires("sqlite3-ue4/3.39.2@adamrehn/{}".format(self.channel))
    
    def cmake_flags(self):
    
        from ue4util import Utility
        sqlite = self.deps_cpp_info["sqlite3-ue4"]
        
        return [
            "-DPROJ_LIB_SUBDIR=lib",
            "-DPROJ_INCLUDE_SUBDIR=include",
            "-DPROJ_TESTS=OFF",
            "-DBUILD_CCT=OFF",
            "-DBUILD_GIE=OFF",
            "-DBUILD_PROJ=OFF",
            "-DBUILD_PROJINFO=OFF",
            "-DBUILD_LIBPROJ_SHARED=OFF",
            "-DBUILD_CS2CS=OFF",
            "-DBUILD_GEOD=OFF",
            "-DBUILD_NAD2BIN=OFF",
            "-DSQLITE3_INCLUDE_DIR="+ sqlite.include_paths[0],
            "-DSQLITE3_LIBRARY=" + Utility.resolve_file(sqlite.lib_paths[0], sqlite.libs[0])
        ]
    
    def source(self):
        
        # Clone the source code
        self.run("git clone --progress --depth=1 https://github.com/OSGeo/proj.4.git -b {}".format(self.version))
        
        # We need to patch the PROJ CMakeLists to fix a bug when the PROJ binaries are not being built
#        tools.replace_in_file(
#            "proj.4/CMakeLists.txt",
#            "add_subdirectory(nad)",
#            "#add_subdirectory(nad)"
#        )
#        tools.replace_in_file(
#            "proj.4/src/CMakeLists.txt",
#            "set_target_properties (cs2cs binproj geod nad2bin PROPERTIES",
#            "#set_target_properties (cs2cs binproj geod nad2bin PROPERTIES"
#        )
#        tools.replace_in_file(
#            "proj.4/src/CMakeLists.txt",
#            "DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})",
#            "#DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})"
#        )
    
    def build(self):
        
        # Enable compiler interposition under Linux to enforce the correct flags for libc++
        from libcxx import LibCxx
        LibCxx.set_vars(self)
        
        # Build PROJ
        cmake = CMake(self)
        cmake.configure(source_folder="proj.4", args=self.cmake_flags())
        cmake.build()
        cmake.install()
    
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
