from setuptools import setup, find_packages

setup(
    name='indicator-shoppe',
    version='1.0.0',
    description='Professional Trading Indicators Library',
    author='Softstove',
    author_email='softstove@github.com',
    url='https://github.com/Softstove/Tokenizer',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.20.0',
        'pandas>=1.2.0',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
