from pythonforandroid.recipe import PythonRecipe
import shutil


class kivyMDRecipe(PythonRecipe):
    version = 'master'
    url = 'https://github.com/kivymd/KivyMD/archive/{version}.zip'

    depends = ['kivy','materialyoucolor','exceptiongroup','asyncgui','asynckivy']
    site_packages_name = 'kivyMD'
    patches = ['kv.patch']
    call_hostpython_via_targetpython = False
    install_in_hostpython = True



recipe = kivyMDRecipe()
