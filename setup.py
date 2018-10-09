from setuptools import find_packages, setup

setup(
  name='blahblah',
  version='0.6.3',
  description='Fake data generator for district42 schema',
  url='https://github.com/nikitanovosibirsk/blahblah',
  author='Nikita Tsvetkov',
  author_email='nikitanovosibirsk@yandex.com',
  license='MIT',
  packages=find_packages(),
  install_requires=[
    'district42==0.6.3',
    'exrex==0.10.5'
  ],
  dependency_links=[
    'https://github.com/nikitanovosibirsk/district42/tarball/e81ef1fc033e47a94b9101b05981b73a722aa1ed#egg=district42-0.6.3'
  ]
)
