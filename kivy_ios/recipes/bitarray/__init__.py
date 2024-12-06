from kivy_ios.toolchain import PythonRecipe, Recipe, shprint
import pathlib
import shutil
import os
from os.path import join
import sh
import fnmatch


class BitarrayRecipeA(PythonRecipe):
    version = "3.0.0"
    url = "https://github.com/ilanschnell/bitarray/archive/refs/tags/{version}.tar.gz"
    depends = ["hostpython3", "python3"]



class BitarrayRecipeB(PythonRecipe):
    version = "3.0.0"
    url = "https://pypi.python.org/packages/source/b/bitarray/bitarray-{version}.tar.gz"
    depends = ["hostpython3", "python3"]
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, plat=None):
        env = super(BitarrayRecipeB, self).get_recipe_env(plat)
        env["PYTHONPATH"] = ":".join(
            [
                self.ctx.get_python_install_dir(plat),
                self.ctx.get_site_packages_dir(plat),
                env["PYTHONPATH"],
            ]
        )
        return env


class BitarrayRecipeC(Recipe):
    version = "3.0.0"
    url = "https://pypi.python.org/packages/source/b/bitarray/bitarray-{version}.tar.gz"
    depends = ["hostpython3", "python3"]
    library = "bitarray.a"
    include_per_platform = True

    def get_bitarray_env(self, plat):
        build_env = plat.get_env()
        build_env["ARCH"] = plat.arch
        build_env["ARM_LD"] = build_env["LD"]
        build_env["LDSHARED"] = join(self.ctx.root_dir, "tools", "liblink")
        build_env["PLATFORM_SDK"] = plat.sdk
        return build_env

    def build_platform(self, plat):
        build_env = self.get_bitarray_env(plat)
        hostpython = sh.Command(self.ctx.hostpython)
        #self.apply_patch("zbarlight_hardcode_version.patch")
        shprint(hostpython, "setup.py", "build", _env=build_env)
        self.biglink()

    def install(self):
        source = next(pathlib.Path(
            self.get_build_dir(list(self.platforms_to_build)[0]),
            "build"
        ).glob("lib.*")) / "bitarray"
        destination = next(pathlib.Path(
            self.ctx.dist_dir,
            "root",
            "python3",
            "lib"
        ).glob("python3.*")) / "site-packages" / "bitarray"

        shutil.rmtree(destination, ignore_errors=True)
        shutil.copytree(source, destination)
        # (destination / "_bitarray.c").unlink()

    def biglink(self):
        dirs = []
        for root, dirnames, filenames in os.walk(self.build_dir):
            if fnmatch.filter(filenames, "*.so.libs"):
                dirs.append(root)

        cmd = sh.Command(join(self.ctx.root_dir, "tools", "biglink"))
        shprint(cmd, join(self.build_dir, self.library), *dirs)


recipe = BitarrayRecipeC()
