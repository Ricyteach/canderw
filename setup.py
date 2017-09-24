from setuptools import find_packages, setup
import pathlib


def _read(path):
    with open(path) as f:
        return f.read()


name = 'canderw'
project_info = {}
exec(_read(pathlib.Path() / 'src' / name / '__version__.py'), project_info)

setup(
    name=project_info['__title__'],
    version=project_info['__version__'],
    description=project_info['__description__'],
    author=project_info['__author__'],
    author_email=project_info['__author_email__'],
    url=project_info['__url__'],
    license=project_info['__license__'],
    keywords=project_info['__keywords__'],
    python_requires='>=3.6',
    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    install_requires=[],
    include_package_data=True,
    long_description='{:s}\n\n{:s}'.format(_read('README.rst'), _read('CHANGELOG.rst')),
    classifiers=(
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: PyPy',
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
    ),
)
