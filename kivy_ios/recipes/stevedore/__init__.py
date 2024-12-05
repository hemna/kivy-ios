# pure-python package, this can be removed when we'll support any python package
from kivy_ios.toolchain import PythonRecipe, shprint
from kivy_ios.context_managers import cd
from os.path import join
import sh


class StevedoreRecipe(PythonRecipe):
    version = "5.4.0"
    url = "https://files.pythonhosted.org/packages/4a/e9/4eedccff8332cc40cc60ddd3b28d4c3e255ee7e9c65679fa4533ab98f598/stevedore-{version}.tar.gz"
    depends = ["python"]

    def install(self):
        plat = list(self.platforms_to_build)[0]
        build_dir = self.get_build_dir(plat)
        hostpython_pip = sh.Command(join(self.ctx.dist_dir, "hostpython3", "bin", "pip3"))
        build_env = plat.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        build_env['PYTHONPATH'] = self.ctx.site_packages_dir
        with cd(build_dir):
            shprint(hostpython_pip, "install", build_dir, "--prefix", dest_dir, _env=build_env)



recipe = StevedoreRecipe()
