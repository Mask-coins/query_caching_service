from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="query_caching_service",
    version="0.2.1",
    description="一度アクセスした資源に何度もアクセスしないためのツールです．",
    author="Mask_coins",
    url="https://github.com/Mask-coins/query_caching_service",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
    #setup_requires=["pytest-runner"],
    #tests_require=["pytest", "pytest-cov"]
)