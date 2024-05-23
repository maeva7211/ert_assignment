"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst', 'rt') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', 'rt') as history_file:
    history = history_file.read()


setup(
    author="Maeva Pourpoint",
    author_email="pourpointmaeva@gmail.com",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description="Application to monitor data from the NOAA Space Weather Prediction Center (SWPC).",
    entry_points={
        'console_scripts': [
            'swpc_monitoring=swpc_monitoring.swpc_monitoring:main',
        ],
    },
    install_requires=['influxdb-client',
                      'python-dotenv',
                      'requests',
                      'scheduler'],
    setup_requires=[],
    extras_require={
        'dev': [
            'flake8',
            'jupyterlab',
            'mypy',
            'tox',
        ]
    },
    license="",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='swpc_monitoring',
    name='swpc_monitoring',
    packages=find_packages(include=['swpc_monitoring']),
    version='2024.1.0.0',
    zip_safe=False,
)
