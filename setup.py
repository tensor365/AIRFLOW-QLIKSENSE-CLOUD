"""Setup.py for the Qlik Sense Cloud Airflow provider package."""

from setuptools import  setup

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

"""Perform the package airflow-provider-qlik-sense-cloud setup."""
setup(
    name='airflow-provider-qlik-sense-cloud',
    version="0.0.5",
    description='Airflow package provider to reload apps/task/automation from Qlik Sense Cloud.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        "apache_airflow_provider": [
            "provider_info=airflow.providers.qlik_sense_cloud.__init__:get_provider_info"
        ]
    },
    license='Apache License 2.0',
    packages=['airflow.providers.qlik_sense_cloud', 'airflow.providers.qlik_sense_cloud.hooks', 'airflow.providers.qlik_sense_cloud.operators'],
    install_requires=['apache-airflow>=2.0', 'qlik-sdk'],
    setup_requires=['setuptools', 'wheel'],
    author='Clement Parsy',
    author_email='cparsy@decideom.fr',
    url='',
    classifiers=[
        "Framework :: Apache Airflow",
        "Framework :: Apache Airflow :: Provider",
    ],
    python_requires='~=3.7',
)
