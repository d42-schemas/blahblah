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
    'https://github.com/nikitanovosibirsk/district42/tarball/19cda359f4a356c9ead02f9f951e24a233242fef#egg=district42-0.6.1'
  ]
)
