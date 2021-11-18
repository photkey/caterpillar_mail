#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

VERSION="1.0.5"

setup(
    name="caterpillar_mail",
    version=VERSION,
    description='收发邮件解析邮件的高层封装，极简应用',
    long_description=long_description,
    author='redrose2100',
    author_email='hitredrose@163.com',
    maintainer='redrose2100',
    maintainer_email='hitredrose@163.com',
    license='MulanPSL2',
    packages=[],
    py_modules=["caterpillar_mail"],
    install_requires=[
    ],
    platforms=["all"],
    url='https://gitee.com/redrose2020_admin/caterpillar_mail',
    include_package_data=True,
    entry_points={
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
)