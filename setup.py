from setuptools import setup

setup(name='walog',
      version='0.1',
      description='WhatsApp conversation logger',
      url='https://github.com/marcoh00/walog',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Communications :: Chat'
      ],
      author='Marco Huenseler',
      author_email='marcoh.huenseler+git@gmail.com',
      license='MPL-2.0',
      packages=['walog'],
      install_requires=[
          'yowsup2 > 2.5.2'
      ],
      entry_points={
          'console_scripts': ['walog=walog.walog:main']
      },
      include_package_data=True,
      zip_safe=False
)