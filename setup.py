from setuptools import setup, find_packages

setup(
    name='typext',
    version='0.1.3',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    url='https://github.com/havocesp/typext',
    license='Apache 2.0',
    author='Daniel J. Umpierrez',
    author_email='',
    description='Enhanced Python builtin types.',
    classifiers=[
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Open source library with some useful routines.',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.4'
    ], install_requires=['decorator', 'requests', 'py-term', 'forbiddenfruit']
)

# Specify the Python versions you support here. In particular, ensure
# that you indicate whether you support Python 2, Python 3 or both.
# 'Programming Language :: Python :: 2',
# 'Programming Language :: Python :: 2.6',
# 'Programming Language :: Python :: 2.7',

# How mature is this project? Common values are
#   3 - Alpha
#   4 - Beta
#   5 - Production/Stable
