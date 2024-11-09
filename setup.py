from setuptools import setup, find_packages

setup(
    name='quantdb',  # Your package name
    version='0.1.0',  # Initial version
    packages=find_packages(),  # Automatically includes your package
    install_requires=[],  # List of dependencies (from requirements.txt)
    author='Your Name',
    author_email='your.email@example.com',
    description='A description of your package',
    url='https://github.com/yourusername/my-package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
