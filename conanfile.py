# Copyright (c) 2016-2020 Knuth Project developers.
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import os
import glob
import platform
import shutil
from conans import tools, ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
from kthbuild import KnuthConanFile

class FmtConan(KnuthConanFile):
    def recipe_dir(self):
        return os.path.dirname(os.path.abspath(__file__))

    name = "fmt"
    version = "6.2.0"
    homepage = "https://github.com/fmtlib/fmt"
    license = "MIT"
    description = "A safe and fast alternative to printf and IOStreams."
    url = "https://github.com/k-nuth/conan-fmt"
    topics = ("conan", "fmt", "format", "iostream", "printf")
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"

    exports = ["conan_*", "ci_utils/*"]
    exports_sources = ["CMakeLists.txt", "patches/**", "knuthbuildinfo.cmake"]

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _env_build = None
    
    build_policy = "missing"
    
    options = {"shared": [True, False], 
               "header_only": [True, False], 
               "fPIC": [True, False], 
               "with_fmt_alias": [True, False],
               "verbose": [True, False],
               "microarchitecture": "ANY",
               "fix_march": [True, False],
               "march_id": "ANY",
               "cxxflags": "ANY",
               "cflags": "ANY",
               "glibcxx_supports_cxx11_abi": "ANY",
    }

    default_options = {
                "shared": False, 
                "header_only": False, 
                "fPIC": True, 
                "with_fmt_alias": False,
                "verbose": False,
                "microarchitecture": '_DUMMY_',
                "fix_march": False,
                "march_id": '_DUMMY_',
                "cxxflags": '_DUMMY_',
                "cflags": '_DUMMY_',
                "glibcxx_supports_cxx11_abi": '_DUMMY_',
    }

    source_url = "https://github.com/fmtlib/fmt/archive/{0}.tar.gz".format(version)
    source_sha256 = "fe6e4ff397e01c379fc4532519339c93da47404b9f6674184a458a9967a76575"

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def package_id(self):
        KnuthConanFile.package_id(self)

        if self.options.header_only:
            self.info.header_only()
        else:
            del self.info.options.with_fmt_alias

    def config_options(self):
        KnuthConanFile.config_options(self)

        #TODO: chequear si está repetido en la función de arriba
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        KnuthConanFile.configure(self)

        if self.options.header_only:
            self.settings.clear()
            del self.options.fPIC
            del self.options.shared
            del self.options.microarchitecture
            del self.options.fix_march
            del self.options.march_id
            del self.options.glibcxx_supports_cxx11_abi

    def source(self):
        self.output.info("Fetching sources: {0}".format(self.source_url))
        tools.get(self.source_url)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["FMT_DOC"] = False
        self._cmake.definitions["FMT_TEST"] = False
        self._cmake.definitions["FMT_INSTALL"] = True
        self._cmake.definitions["FMT_LIB_DIR"] = "lib"
        self._cmake.configure()
        # self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        # if "patches" in self.conan_data and self.version in self.conan_data["patches"]:
        #     for patch in self.conan_data["patches"][self.version]:
        #         tools.patch(**patch)

        if not self.options.header_only:
            cmake = self._configure_cmake()
            cmake.build()

    def package(self):
        # self.copy("LICENSE.rst", dst="licenses", src=self._source_subfolder)
        if self.options.header_only:
            src_dir = os.path.join(self._source_subfolder, "src")
            header_dir = os.path.join(self._source_subfolder, "include")
            dst_dir = os.path.join("include", "fmt")
            self.copy("*.h", dst="include", src=header_dir)
            self.copy("*.cc", dst=dst_dir, src=src_dir)
        else:
            cmake = self._configure_cmake()
            cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "share"))


    def package_info(self):
        if self.options.with_fmt_alias:
            self.cpp_info.defines.append("FMT_STRING_ALIAS=1")

        if self.options.header_only:
            self.cpp_info.defines.append("FMT_HEADER_ONLY")
        else:
            self.cpp_info.libs = tools.collect_libs(self)
            if self.options.shared:
                self.cpp_info.defines.append("FMT_SHARED")