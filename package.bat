# 安装到本地
pip install . --user

py -m build
py -m twine upload --repository testpypi dist/*
--py -m twine upload dist/*
