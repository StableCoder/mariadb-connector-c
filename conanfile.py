from conans import ConanFile, CMake, tools
import os


class MariadbConnectorConan(ConanFile):
    name = "mariadb-connector-c"
    version = "3.1.3"
    license = "LGPL 2.1"
    url = "https://git.stabletec.com/conan/mariadb-connector-c"
    description = "MariaDB Connector/C is used to connect applications developed in C/C++ to MariaDB and MySQL databases."
    settings = "os", "compiler", "build_type", "arch"
    options = {"with_curl": [True, False],
               "with_external_zlib": [True, False],
               "with_dyncol": [True, False],
               "with_mysqlcompat": [True, False],
               "with_ssl": [True, False]}
    default_options = "with_curl=False", "with_dyncol=True", "with_external_zlib=False", "with_mysqlcompat=False", "with_ssl=True"
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
        if self.options.with_ssl:
            self.requires("OpenSSL/1.1.1c@conan/stable")
        if self.options.with_external_zlib:
            self.requires("zlib/1.2.11@conan/stable")
        if self.options.with_curl:
            self.requires("libcurl/7.64.1@bincrafters/stable")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["WITH_UNIT_TESTS"] = False
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = True
        if not self.options.with_curl:
            cmake.definitions["WITH_CURL"] = False
        if not self.options.with_dyncol:
            cmake.definitions["WITH_DYNCOL"] = False
        if self.options.with_external_zlib:
            cmake.definitions["WITH_EXTERNAL_ZLIB"] = True
        if self.options.with_mysqlcompat:
            cmake.definitions["WITH_MYSQLCOMPAT"] = True
        if not self.options.with_ssl:
            cmake.definitions["WITH_SSL"] = False
        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()

    def package(self):
        include_folder = "{0}/include".format(self.source_subfolder)
        # Headers
        self.copy("mariadb/*.h", dst="include/mysql", src=include_folder)
        self.copy("mysql*", dst="include/mysql", src=include_folder)
        self.copy("errmsg.h", dst="include/mysql", src=include_folder)
        self.copy("ma_list.h", dst="include/mysql", src=include_folder)
        self.copy("ma_pvio.h", dst="include/mysql", src=include_folder)
        self.copy("ma_tls.h", dst="include/mysql", src=include_folder)
        self.copy("mariadb_com.h", dst="include/mysql", src=include_folder)
        self.copy("mariadb_ctype.h", dst="include/mysql", src=include_folder)
        self.copy("mariadb_dyncol.h",
                  dst="include/mysql", src=include_folder)
        self.copy("mariadb_stmt.h", dst="include/mysql", src=include_folder)
        self.copy("mariadb_version.h",
                  dst="include/mysql", src="include")
        # Libraries
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.pdb", dst="bin", src="bin")
        self.copy("libmariadb.lib", dst="lib", src="lib")
        self.copy("mariadbclient.lib", dst="lib", src="lib")
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("libmariadb.so*", dst="lib", src="lib")
        self.copy("libmariadbclient.a", dst="lib", src="lib")
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["libmariadb", "mariadbclient"]
        else:
            self.cpp_info.libs = ["mariadb", "mariadbclient"]
