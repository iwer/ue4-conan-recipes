from conans import AutoToolsBuildEnvironment, ConanFile, CMake, tools
import os
import shutil

class LibgeotiffUe4Conan(ConanFile):
    name = "libgeotiff-ue4"
    version = "1.7.1"
    description = "Libgeotiff is an open source library normally hosted on top " \
                  "of libtiff for reading, and writing GeoTIFF information tags."
    license = ["MIT", "BSD-3-Clause"]
    topics = ("libgeotiff", "geotiff", "tiff")
    homepage = "https://github.com/OSGeo/libgeotiff"
    url = "https://github.com/adamrehn/ue4-conan-recipes/libgeotiff-ue4"
    generators: "cmake"
    requires = (
        "libcxx/ue4@adamrehn/profile",
        "ue4util/ue4@adamrehn/profile"
    )
    
    def requirements(self):
        self.requires("proj-ue4/6.3.2@adamrehn/{}".format(self.channel))
        self.requires("LibTiff/ue4@adamrehn/{}".format(self.channel))
        self.requires("sqlite3-ue4/3.39.2@adamrehn/{}".format(self.channel))
        
    def build_requirements(self):
        self.build_requires("LibJpegTurbo/ue4@adamrehn/{}".format(self.channel))
    
    def cmake_flags(self):
        from ue4util import Utility
        proj = self.deps_cpp_info["proj-ue4"]
        tiff = self.deps_cpp_info["LibTiff"]

        return [
            "-DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY",
            "-DWITH_JPEG=OFF",
            "-DWITH_UTILITIES=OFF",
            "-DPROJ_INCLUDE_DIR="+ proj.include_paths[0],
            "-DPROJ_LIBRARY=" + Utility.resolve_file(proj.lib_paths[0], proj.libs[0]),
            "-DTIFF_INCLUDE_DIR=" + tiff.include_paths[0],
            "-DTIFF_LIBRARY=" + Utility.resolve_file(tiff.lib_paths[0], tiff.libs[0])
        ]
        
    def source(self):
    
        self.run("git clone --progress --depth=1 https://github.com/OSGeo/libgeotiff.git -b {}".format(self.version))
    
    
    def build(self):
    
        # Enable compiler interposition under Linux to enforce the correct flags for libc++
        from libcxx import LibCxx
        LibCxx.set_vars(self)
        
        # Build PROJ
        cmake = CMake(self)
        cmake.configure(source_folder="libgeotiff/libgeotiff", args=self.cmake_flags())
        cmake.build()
        cmake.install()
    
    def package_info(self):
    
        self.cpp_info.libs = tools.collect_libs(self)
        
