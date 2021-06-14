from setuptools import find_packages, setup

setup(
  name='blahblah',
  version='0.6.9',
  description='Fake data generator for district42 schema',
  url='https://github.com/nikitanovosibirsk/blahblah',
  author='Nikita Tsvetkov',
  author_email='nikitanovosibirsk@yandex.com',
  python_requires='>=3.6',
  license='MIT',
  packages=find_packages(),
  install_requires=[
    'district42<1.0',
    'exrex==0.10.5',
  ],
)
