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
    name='proton_decay_study',
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
    url='https://github.com/HEP-DL/proton_decay_study',
    packages=find_packages(),
    package_dir={'proton_decay_study':
                 'proton_decay_study'},
    entry_points={
        'console_scripts': [
            'proton_decay_study=proton_decay_study.cli:main',
            'vgg_training=proton_decay_study.cli:standard_vgg_training',
            'kjw_train=proton_decay_study.cli:advanced_vgg_training',
            'test_file_input=proton_decay_study.cli:test_file_input',
            'test_threaded_files=proton_decay_study.cli:test_threaded_file_input',
            'plot_model=proton_decay_study.cli:plot_model',
            'train_kevnet=proton_decay_study.cli:train_kevnet',
            'train_nbn=proton_decay_study.cli:train_nbn',
            'train_nb_prl=proton_decay_study.cli:train_nbn_prl',
            'make_kevnet_featuremap=proton_decay_study.cli:make_kevnet_featuremap'
        ]
    },
    include_package_data=True,
    install_requires=reqs,
    license="MIT license",
    zip_safe=False,
    keywords='proton_decay_study',
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
