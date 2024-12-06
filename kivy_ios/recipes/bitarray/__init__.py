from kivy_ios.toolchain import PythonRecipe


class BitarrayRecipeA(PythonRecipe):
    version = "3.0.0"
    url = "https://github.com/ilanschnell/bitarray/archive/refs/tags/{version}.tar.gz"
    depends = ["hostpython3", "python3"]



class BitarrayRecipeB(PythonRecipe):
    version = "latest"
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

recipe = BitarrayRecipeB()
