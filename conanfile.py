from conans import ConanFile, CMake, tools
import os


class MariadbConnectorConan(ConanFile):
    name = "mariadb-connector"
    version = "3.0.4"
    license = "LGPL 2+"
    url = "https://github.com/StableCoder/conan-mariadb-connector"
    description = "MariaDB Connector/C is used to connect applications developed in C/C++ to MariaDB and MySQL databases."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "no_zlib": [True, False], "no_ssl": [True, False]}
    default_options = "shared=False", "fPIC=True", "no_zlib=False", "no_ssl=False"
    generators = "cmake"
    source_subfolder = "source_subfolder"

    def source(self):
        tools.get(
            "https://downloads.mariadb.org/f/connector-c-{0}/mariadb-connector-c-{0}-src.zip".format(self.version))
        os.rename(
            "mariadb-connector-c-{0}-src".format(self.version), self.source_subfolder)
        tools.replace_in_file("{0}/CMakeLists.txt".format(self.source_subfolder), "PROJECT(mariadb-connector-c C)",
                              '''PROJECT(mariadb-connector-c C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def requirements(self):
        if not self.options.no_ssl:
            self.requires("OpenSSL/1.0.2o@conan/stable")
        if not self.options.no_zlib:
            self.requires("zlib/1.2.11@conan/stable")

    def build(self):
        cmake = CMake(self)
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        if not self.options.no_zlib:
            cmake.definitions["WITH_EXTERNAL_ZLIB"] = True
        if self.options.no_ssl:
            cmake.definitions["WITH_SSL"] = False
        cmake.definitions["WITH_UNIT_TESTS"] = False
        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()

    def package(self):
        include_folder = "{0}/include".format(self.source_subfolder)
        self.copy("*.h", dst="include/mysql", src=include_folder)
        self.copy("*.h", dst="include/mysql", src="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = tools.collect_libs(self)
        else:
            self.cpp_info.libs = ["mariadb", "mariadbclient"]
