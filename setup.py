from setuptools import setup, find_packages

setup(
    name='your_package_name',
    version='0.1.0',  # Start with version 0.1.0, increment as needed
    packages=find_packages(),  # Automatically find all packages in your directory
    install_requires=[         # Dependencies (if any)
        'some_dependency',      # Add any external libraries your package uses
    ],
    description='A short description of your package',
    long_description=open('README.md').read(),  # Optional, read the content of README
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/your_package',  # URL of the package (if on GitHub)
    classifiers=[             # Optional, metadata for PyPI listing
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
)
