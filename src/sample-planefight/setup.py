from distutils.core import setup
import py2exe
import glob

INCLUDES = []

options = {
    "py2exe" :
        {
            "compressed" : 1, # 压缩
            "optimize" : 2,
            "bundle_files" : 1, # 所有文件打包成一个 exe 文件
            "dll_excludes" : ["MSVCR100.dll"]
        }
}


setup(
    options=options,
    description = "飞机大战",
    zipfile=None,
    data_files=[("images",
                 glob.glob("images\\*", recursive=True)),
                ("font",
                 glob.glob("font\\*.*")),
                ("music",
                 glob.glob("music\\*.*"))],
    console = [{"script":'main.py'}])
