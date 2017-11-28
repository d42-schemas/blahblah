from setuptools import find_packages, setup

setup(
  name='blahblah',
  version='0.6.1',
  description='Fake data generator for district42 schema',
  url='https://github.com/nikitanovosibirsk/blahblah',
  author='Nikita Tsvetkov',
  author_email='nikitanovosibirsk@yandex.com',
  license='MIT',
  packages=find_packages(),
  install_requires=[
    'district42==0.6.1',
    'exrex==0.9.4'
  ],
  dependency_links=[
    'https://github.com/nikitanovosibirsk/district42/tarball/41efc1348be6720b844ccf250f5f08f215aa4869#egg=district42-0.6.1'
  ]
)
