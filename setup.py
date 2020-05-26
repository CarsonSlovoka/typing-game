import setuptools
from setuptools import setup, find_packages
from setuptools.command.test import test as test_class

if 'env path':
    import typing_drop_down
    from typing_drop_down import __version__

VERSION_NUMBER = __version__
DOWNLOAD_VERSION = __version__
PACKAGES_DIR = typing_drop_down.__name__
SETUP_NAME = PACKAGES_DIR.replace('_', '-')

GITHUB_URL = f'https://github.com/CarsonSlovoka/{SETUP_NAME}/tree/master'

# Store original `find_package_modules` function
find_package_modules = setuptools.command.build_py.build_py.find_package_modules


def custom_find_package_modules(self, package, package_dir):
    all_info_list = find_package_modules(self, package, package_dir)

    accepted_info_list = []

    for pkg_full_name, module_bare_name, module_path in all_info_list:
        next_flag = False
        for exclude_file in ('test_entry.py', 'test.old.py', 'test.py'):
            if exclude_file in module_path:
                next_flag = True
                break
        if next_flag:
            continue
        accepted_info_list.append((pkg_full_name, module_bare_name, module_path))
    return accepted_info_list


# Replace original `find_package_modules` function with the custom one.
setuptools.command.build_py.build_py.find_package_modules = custom_find_package_modules


with open('README.rst', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

with open('requirements.txt') as req_txt:
    LIST_REQUIRES = [line.strip() for line in req_txt if not line.startswith('#') and line.strip() != '']

setup(
    name=SETUP_NAME,
    version=VERSION_NUMBER,  # x.x.x.{dev, a, b, rc}

    packages=find_packages(exclude=['*.test_cases']),

    include_package_data=True,  # include any data files it finds inside your package directories that are specified by your MANIFEST.in
    package_data={f'{PACKAGES_DIR}': ['_static/home.jpg', ],
                  },
    license="MIT",
    author='Carson',
    author_email='jackparadise520a@gmail.com',
    install_requires=LIST_REQUIRES,
    url=GITHUB_URL,
    description='Tilt corrector for the text image',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    keywords=['typing', 'game', 'pygame', 'pygame-menu', ],

    download_url=f'{GITHUB_URL}/tarball/v{DOWNLOAD_VERSION}',
    python_requires='>=3.6.2,',

    zip_safe=False,
    classifiers=[  # https://pypi.org/classifiers/
        'Topic :: Education',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development',
        'Typing :: Typed',
        'Topic :: Utilities',
        'Natural Language :: Chinese (Traditional)',
        'Natural Language :: English',
        'Operating System :: Microsoft',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],

    entry_points={
        'console_scripts': [
            f'typing_game={PACKAGES_DIR}.cli:main',
        ],
    },
)
