import setuptools


def read_requirements():
    """parses requirements from requirements.txt"""

    with open('requirements/common.txt') as f:
        req = f.readlines()

    return req


if __name__ == "__main__":
    setuptools.setup(
        name='QCArchive_webapps',
        version="0.1.0",
        description='Website for the QCArchive: the Quantum Chemistry Archive',
        author='Doaa Altarawy',
        author_email='daltarawy@vt.edu',
        url="https://github.com/MolSSI/QCArchive_webapps",
        license='BSD-3C',

        packages=setuptools.find_packages(),

        install_requires=read_requirements(),

        include_package_data=True,

        extras_require={
            'tests': [
            ],
        },

        tests_require=[],

        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
        ],
        zip_safe=True,
    )
