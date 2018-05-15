from setuptools import find_packages, setup

setup(
    name='laudos_dashboard',
    description='',
    version='0.0.1',
    url='https://github.com/IvanBrasilico/laudos_dashboard',
    license='GPL',
    author='Ivan Brasilico',
    author_email='brasilico.ivan@gmail.com',
    packages=find_packages(),
    install_requires=[
        'dash==0.21.1',
        'dash-renderer==0.12.1',
        'dash-html-components==0.10.1',
        'dash-core-components==0.22.1',
        'mysqlclient',
        'pandas',
        'plotly==2.2.3'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="tests",
    package_data={
    },
    extras_require={
        'dev': [
            'bandit',
            'coverage',
            'flake8',
            'flake8-quotes',
            'flask-webtest',
            'isort',
            'pylint',
            'pytest',
            'pytest-cov',
            'pytest-mock',
            'sphinx',
            'sphinx_rtd_theme',
            'testfixtures',
            'tox'
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.5',
    ],
)
