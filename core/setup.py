from setuptools import setup, find_packages

setup(
    name='books-core',
    version='0.0.1',
    description='Bookstore core modules',
    url='http://mybooks.com',
    author='Yogesh',
    author_email='yogesh.hole93@gmail.com',
    license='ABC',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'fastapi',
    ],
    setup_requires=[
        'fastapi',
    ],
    python_requires='>=3.7',
)
