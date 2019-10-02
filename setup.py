import setuptools

try: # for pip >= 10
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
    from pip.download import PipSession


def read_requirements():
    """parses requirements from requirements.txt"""

    install_reqs = parse_requirements('requirements.txt', session=PipSession())
    return [ir.name for ir in install_reqs]


if __name__ == "__main__":
    setuptools.setup(
        name='QCArchive_website',
        version="0.1.0",
        description='Website for the QCArchive: the Quantum Chemistry Archive',
        author='Doaa Altarawy',
        author_email='daltarawy@vt.edu',
        url="https://github.com/MolSSI/QCArchive_website",
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
