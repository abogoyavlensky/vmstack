import setuptools

setuptools.setup(
    name = 'vmstack',
    version = '0.1',
    packages = ["vmstack"],
    scripts = [
    ],
    package_data = {'vmstack': [
        'templates/*.html',
    ]},
    install_requires = [
        'tornado',
        'sqlalchemy'
    ],
    entry_points = {
        'console_scripts': [
            'vmstack = vmstack.web_api:main'
            ]
    }
)
