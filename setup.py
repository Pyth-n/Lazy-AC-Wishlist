from setuptools import setup, find_packages

from lazy_ac_wishlist.version import __version__

exec(open('lazy_ac_wishlist/version.py').read())
setup(name='lazyacwishlist', version=__version__, packages = find_packages(),
    install_requires=['selenium, black'])