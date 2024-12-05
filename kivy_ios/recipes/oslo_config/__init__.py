# pure-python package, this can be removed when we'll support any python package
from kivy_ios.toolchain import PythonRecipe, shprint
from os.path import join
import sh
import os


class OsloConfigRecipe(PythonRecipe):
    version = "9.7.0"
    #url = "https://github.com/mitsuhiko/click/archive/{version}.zip"
    url = "https://files.pythonhosted.org/packages/2e/e9/2cac91d42e8fb86b17ef8f350b523f70282fbc9f3a0785884e455b132e50/oslo.config-{version}.tar.gz"
    depends = ["python"]

    def install(self):
        plat = list(self.platforms_to_build)[0]
        build_dir = self.get_build_dir(plat)
        os.chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = plat.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        build_env['PYTHONPATH'] = self.ctx.site_packages_dir
        shprint(hostpython, "setup.py", "install", "--prefix", dest_dir, _env=build_env)


recipe = OsloConfigRecipe()
