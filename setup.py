from setuptools import setup, find_packages

setup(name="aclhound",
      version='0.1',
      description='ACL compiler',
      url='https://github.com/job/aclhound',
      author='Job Snijders',
      author_email='job@instituut.net',
      license='BSD 2-Clause',
      packages=find_packages(),
      install_requires=['grako==2.4.1', 'ipaddr==2.1.11'],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD 2-Clause License",
                   "Programming Language :: Python"
                   ],
      zip_safe=False,
      entry_points={'console_scripts': ['aclhound = aclhound.cli:main']})
