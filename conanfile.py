from conans import ConanFile, CMake, tools


class MariadbConnectorConan(ConanFile):
    name = "mariadb-connector"
    version = "3.0.3"
    license = "LGPL 2+"
    url = "https://github.com/StableCoder/conan-mariadb-connector"
    description = "MariaDB Connector/C is used to connect applications developed in C/C++ to MariaDB and MySQL databases."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    requires = "zlib/1.2.11@conan/stable", "libiconv/1.15@bincrafters/stable"
    generators = "cmake"
    source_subfolder = "mariadb-connector-c-{0}-src".format(version)

    def source(self):
        tools.get(
            "https://downloads.mariadb.org/f/connector-c-{0}/mariadb-connector-c-{0}-src.zip?serve".format(self.version))
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("{0}/CMakeLists.txt".format(self.source_subfolder), "PROJECT(mariadb-connector-c C)",
                              '''PROJECT(mariadb-connector-c C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["WITH_EXTERNAL_ZLIB"] = True
        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s' % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include",
                  src="{0}/include".format(self.source_subfolder))
        self.copy("*.h", dst="include", src="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["mariadb"]
