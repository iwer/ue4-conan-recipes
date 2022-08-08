from conans import AutoToolsBuildEnvironment, ConanFile, CMake, tools
from conans.tools import download, untargz, check_sha256
from conans.errors import ConanInvalidConfiguration
import os
import shutil

required_conan_version = ">=1.43.0"


class Sqlite3Conan(ConanFile):
    name = "sqlite3-ue4"
    version = "3.39.2"
    description = "Self-contained, serverless, in-process SQL database engine."
    license = "Public Domain"
    homepage = "https://www.sqlite.org"
    url = "https://github.com/adamrehn/ue4-conan-recipes/libgeotiff-ue4"
    topics = ("sqlite", "database", "sql", "serverless")
    generators: "cmake"
    requires = (
        "libcxx/ue4@adamrehn/profile",
        "ue4util/ue4@adamrehn/profile"
    )
    
    def configure_flags(self):
    
        return []
    
    def source(self):
    
        zip_name = "sqlite3-{}.zip".format(self.version);
        download("https://sqlite.org/2022/sqlite-autoconf-3390200.tar.gz", zip_name);
        untargz(zip_name)
        shutil.move("sqlite-autoconf-3390200", "sqlite")
        os.unlink(zip_name)
    
    def build(self):
        
        # Enable compiler interposition under Linux to enforce the correct flags for libc++
        from libcxx import LibCxx
        LibCxx.set_vars(self)
        
        # Prepare the autotools build environment
        autotools = AutoToolsBuildEnvironment(self)
        LibCxx.fix_autotools(autotools)
        
        # Build using autotools
        with tools.chdir("./sqlite"):
            autotools.configure(args=self.configure_flags())
            autotools.make(args=["-j{}".format(tools.cpu_count())])
            autotools.make(target="install")
    
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
