from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment
from conans.util import files
import os

class YAMLCppConan(ConanFile):
    name = "yaml-cpp"
    version = "0.6.2"
    YAML_FOLDER_NAME = "yaml-cpp-yaml-cpp-%s" % version
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    description = "A YAML parser and emitter in C++."
    generators = "cmake"
    options = {"shared": [True, False], "fPIC": [True, False]}

    name = "yaml-cpp"
    version = "0.6.2"
    url = "https://github.com/uilianries/conan-yaml-cpp"
    homepage = "https://github.com/jbeder/yaml-cpp"
    author = "Bincrafters <bincrafters@gmail.com>"
    description = "A YAML parser and emitter in C++"
    license = "MIT"
    exports = "LICENSE.md"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    def config_options(self):
        if self.settings.os == 'Windows':
            self.options.remove("fPIC")

    def source(self):
      #y_name = "yamp-cpp-%s.tar.gz" % self.version
      #tools.download("https://github.com/jbeder/yaml-cpp/archive/yaml-cpp-%s.tar.gz" % self.version, y_name)
      #tools.unzip(y_name)
      #os.unlink(y_name)
      #if not tools.os_info.is_windows:
        #self.run("chmod +x ./%s/configure" % self.YAML_FOLDER_NAME)
      
      #os.rename(self.YAML_FOLDER_NAME, 'src')
      self.run("git clone https://github.com/jbeder/yaml-cpp.git")
	  

    def build(self):
      cmake = CMake(self, parallel=True)
      
      cmake.definitions["YAML_CPP_BUILD_CONTRIB"] = True
      cmake.definitions["YAML_CPP_BUILD_TOOLS"] = False
      cmake.definitions["YAML_CPP_BUILD_TESTS"] = False
      
      if self.settings.os == "Windows" and self.options.shared:
        cmake.definitions["BUILD_SHARED_LIBS"] = True
      if self.settings.os == "Windows" and not self.options.shared:
        cmake.definitions["BUILD_SHARED_LIBS"] = False
      
      if self.settings.os == "Windows":
        cmake.definitions["MSVC_SHARED_RT"] = self.settings.compiler.runtime == "MD" or self.settings.compiler.runtime == "MDd"
      
      cmake.configure(source_dir=self.source_folder + '/yaml-cpp')
      cmake.build()

    def package(self):
        #self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        #cmake.install()

        # Headers
        self.copy("*", dst="include", src=self.source_folder + "/yaml-cpp/include", keep_path=True)
        # Libraries
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
