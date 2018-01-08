#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import setup, find_packages
from pip.req import parse_requirements
import pip


install_reqs = reqs = [str(ir.req) for ir in parse_requirements('requirements.txt',
    session=pip.download.PipSession())]
dev_reqs = [str(ir.req) for ir in parse_requirements('requirements_dev.txt',
    session=pip.download.PipSession())]

setup(
    name='dlpix_wire',
    version='0.1.0',
    description="Looks for proton decay. USING NEURAL NETWORKS",
    long_description="""
        Top-level code base for CNN study of LArTPC data for proton decay.

        This relies primarily on Kevlar and Keras with the Tensorflow backend.

        Kevlar provides the data interface consumned by the generators. Keras and
        tensorflow provide the framework used to train and utilize the networks.

    """,
    author="Kevin Wierman",
    author_email='kevin.wierman@pnnl.gov',
    url='https://github.com/HEP-DL/dlpix_wire',
    packages=find_packages(),
    package_dir={'dlpix_wire':
                 'dlpix_wire'},
    entry_points={
        'console_scripts': [
            'dlpix_wire=dlpix_wire.cli:main',
            'vgg_training=dlpix_wire.cli:standard_vgg_training',
            'kjw_train=dlpix_wire.cli:advanced_vgg_training',
            'test_file_input=dlpix_wire.cli:test_file_input',
            'test_threaded_files=dlpix_wire.cli:test_threaded_file_input',
            'plot_model=dlpix_wire.cli:plot_model',
            'train_kevnet=dlpix_wire.cli:train_kevnet',
            'train_nbn=dlpix_wire.cli:train_nbn',
            'make_kevnet_featuremap=dlpix_wire.cli:make_kevnet_featuremap'
        ]
    },
    include_package_data=True,
    install_requires=reqs,
    license="MIT license",
    zip_safe=False,
    keywords='dlpix_wire',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=dev_reqs
)
