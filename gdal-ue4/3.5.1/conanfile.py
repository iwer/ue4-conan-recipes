from conans import ConanFile, CMake, tools

class GdalUe4Conan(ConanFile):
    name = "gdal-ue4"
    version = "3.5.1"
    license = "MIT"
    url = "https://github.com/adamrehn/ue4-conan-recipes/gdal-ue4"
    description = "GDAL custom build for Unreal Engine 4"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    short_paths = True
    requires = (
        "libcxx/ue4@adamrehn/profile",
        "ue4util/ue4@adamrehn/profile"
    )
    
    def requirements(self):
        self.requires("geos-ue4/3.6.3@adamrehn/{}".format(self.channel))
        self.requires("proj-ue4/8.2.1@adamrehn/{}".format(self.channel))
        self.requires("libcurl/ue4@adamrehn/{}".format(self.channel))
        self.requires("UElibPNG/ue4@adamrehn/{}".format(self.channel))
        self.requires("zlib/ue4@adamrehn/{}".format(self.channel))
        self.requires("LibTiff/ue4@adamrehn/{}".format(self.channel))
        self.requires("libgeotiff-ue4/1.7.1@adamrehn/{}".format(self.channel))
        self.requires("LibJpegTurbo/ue4@adamrehn/{}".format(self.channel))
        
    def cmake_flags(self):
        from ue4util import Utility
        zlib = self.deps_cpp_info["zlib"]
        geos = self.deps_cpp_info["geos-ue4"]
        proj = self.deps_cpp_info["proj-ue4"]
        tiff = self.deps_cpp_info["LibTiff"]
        png =  self.deps_cpp_info["UElibPNG"]
        jpeg = self.deps_cpp_info["LibJpegTurbo"]
        geotiff = self.deps_cpp_info["libgeotiff-ue4"]
        geosConfig = Utility.resolve_file(geos.bin_paths[0], "geos-config")

    
        return [
            "-DBUILD_APPS=OFF",
            "-DBUILD_CSHARP_BINDINGS=OFF",
            "-DBUILD_DOCS=OFF",
            "-DBUILD_JAVA_BINDINGS=OFF",
            "-DBUILD_PYTHON_BINDINGS=OFF",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DBUILD_TESTING=OFF",
            "-DENABLE_PAM=OFF",
            "-DGDAL_USE_PNG_INTERNAL=OFF",
            "-DGDAL_USE_ZLIB_INTERNAL=OFF",
            "-DGDAL_USE_JPEG_INTERNAL=OFF",
            "-DGDAL_USE_JSONC_INTERNAL=ON",
            "-DGDAL_USE_JPEG12_INTERNAL=OFF",
            "-DGDAL_ENABLE_DRIVER_JPEG=ON",
            "-DGDAL_ENABLE_DRIVER_PCRASTER=OFF",
            "-DGDAL_ENABLE_DRIVER_MRF=OFF",
            "-DGDAL_ENABLE_DRIVER_MSGN=OFF",
            "-DGDAL_ENABLE_DRIVER_BSB=OFF",
            "-DGDAL_ENABLE_DRIVER_GRIB=OFF",
            "-DGDAL_ENABLE_DRIVER_PDF=OFF",
            "-DGDAL_ENABLE_DRIVER_HEIF=OFF",
            "-DGDAL_USE_POSTGRESQL=OFF",
            "-DGDAL_USE_CFITSIO=OFF",
            "-DGDAL_USE_GIFF=OFF",
            "-DGDAL_USE_OGDI=OFF",
            "-DGDAL_USE_HDF4=OFF",
            "-DGDAL_USE_HDF5=OFF",
            "-DGDAL_USE_NETCDF=OFF",
            "-DGDAL_USE_OPENJPEG=OFF",
            "-DGDAL_USE_MYSQL=OFF",
            "-DGDAL_USE_XERCESC=OFF",
            "-DGDAL_USE_EXPAT=OFF",
            "-DGDAL_USE_LIBKML=OFF",
            "-DGDAL_USE_ODBC=OFF",
            "-DGDAL_USE_CURL=OFF",
            "-DGDAL_USE_LIBXML2=OFF",
            "-DGDAL_USE_SPATIALITE=OFF",
            "-DGDAL_USE_SQLITE3=OFF",
            "-DGDAL_USE_PCRE2=OFF",
            "-DGDAL_USE_WEBP=OFF",
            "-DGDAL_USE_QHULL=OFF",
            "-DGDAL_USE_FREEXL=OFF",
            "-DGDAL_USE_POPPLER=OFF",
            "-DGDAL_USE_ARMADILLO=OFF",
            "-DGDAL_USE_CRYPTOPP=OFF",
            "-DGDAL_USE_OPENSSL=OFF",
            "-DGDAL_USE_OPENEXR=OFF",
            "-DGDAL_USE_ZLIB=ON",
            "-DGDAL_USE_TIFF=ON",
            "-DGDAL_USE_GEOTIFF=ON",
            "-DOGR_ENABLE_DRIVER_SOSI=OFF",
            "-DTIFF_INCLUDE_DIR=" + tiff.include_paths[0],
            "-DTIFF_LIBRARY_RELEASE=" + Utility.resolve_file(tiff.lib_paths[0], tiff.libs[0]),
            "-DGEOTIFF_INCLUDE_DIR=" + geotiff.include_paths[0],
            "-DGEOTIFF_LIBRARY_RELEASE=" + Utility.resolve_file(geotiff.lib_paths[0], geotiff.libs[0]),
            "-DPNG_PNG_INCLUDE_DIR=" + png.include_paths[0],
            "-DPNG_LIBRARY_RELEASE=" + Utility.resolve_file(png.lib_paths[0], png.libs[0]),
            "-DJPEG_INCLUDE_DIR=" + jpeg.include_paths[0],
            "-DJPEG_LIBRARY_RELEASE=" + Utility.resolve_file(jpeg.lib_paths[0], jpeg.libs[0]),
            "-DZLIB_INCLUDE_DIR=" + zlib.include_paths[0],
            "-DZLIB_LIBRARY_RELEASE=" + Utility.resolve_file(zlib.lib_paths[0], zlib.libs[0]),
            "-DPROJ_INCLUDE_DIR="+ proj.include_paths[0],
            "-DPROJ_LIBRARY=" + Utility.resolve_file(proj.lib_paths[0], proj.libs[0]),
            "-DGEOS_DIR={}".format(geosConfig),
            "-DGEOS_INCLUDE_DIR=" + geos.include_paths[0],
            "-DGEOS_LIBRARY=" + Utility.resolve_file(geos.lib_paths[0], geos.libs[0])            
        ]
    
    def source(self):
        self.run("git clone --progress --depth=1 https://github.com/OSGeo/gdal.git -b v{}".format(self.version))
        
    def build(self):
        
        # Enable compiler interposition under Linux to enforce the correct flags for libc++
        from libcxx import LibCxx
        LibCxx.set_vars(self)
        
        # Build PROJ
        cmake = CMake(self)
        cmake.configure(source_folder="gdal",args=self.cmake_flags())
        cmake.build()
        cmake.install()
    
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
