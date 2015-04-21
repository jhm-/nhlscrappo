from nhlscrappo import __version__
from distutils.core import setup
from setuptools import find_packages

def _read(file):
    return open(file, 'rb').read()

setup(name="nhlscrappo",
      version=__version__,
      description="Web scraping API for NHL.com Real Time Shot System (RTSS) reports",
      long_description=_read('README.md').decode('utf-8'),
      author="Jack Morton",
      author_email="jhm@jemscout.com",
      license="MIT",
      url="https://github.com/jhm-/nhlscrappo",
      zip_safe=False,
      include_package_data=True,
      packages=find_packages(),
      install_requires=['lxml', 'beautifulsoup4']
)
