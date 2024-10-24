from setuptools import setup, find_packages

# Read the contents of your README file for the long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="quantum_data_analysis",  # Replace with your package name
    version="0.1.0",  # Initial version
    author="KOSASIH",  # Replace with your name
    author_email="kosasihg88@gmail.com",  # Replace with your email
    description="A package for advanced quantum data analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quantum_data_analysis",  # Replace with your GitHub repo URL
    packages=find_packages(),  # Automatically find packages in the project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your license
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
    install_requires=[
        "pandas==1.5.3",
        "numpy==1.23.5",
        "matplotlib==3.6.2",
        "seaborn==0.12.1",
        # Add any other dependencies your project requires
    ],
    entry_points={
        'console_scripts': [
            'quantum-analyze=src.main:main',  # Command to run your main function
        ],
    },
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    zip_safe=False,  # Set to False if your package cannot be reliably used if installed as a .egg file
)
