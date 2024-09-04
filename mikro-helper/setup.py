from setuptools import setup, find_packages

setup(
    name='mikro-helper',
    version='1.1.1',
    description='Creating backups of Mikrotik Network devices',
    author='Veronica',
    author_email='veronica@yun.kz',
    url='https://github.com/Yun-Veronica/mikro-helper',
    packages=find_packages(),
    install_requires=[
        'paramiko>=3.4.0',
        'PyYAML>=6.0.1'

    ],
    classifiers=[  # Optional classifiers
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPU 3.0 License ', ],
    python_requires='>=3.10',  # Specify the Python version required
)
