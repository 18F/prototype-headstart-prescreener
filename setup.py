from setuptools import find_packages, setup

setup(
    name='Prototype Head Start Pre-Screener',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'requests',
        'python-dotenv',
        'Flask-HTTPAuth'
    ],
)
