from setuptools import setup, find_packages
import os
import sys

version = "0.6"

if sys.argv[-1] == 'publish':
    os.system('python2.7 setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

setup(name="aclhound",
      version=version,
      description='ACL compiler',
      url='https://github.com/job/aclhound',
      author='Job Snijders',
      author_email='job@instituut.net',
      license='BSD 2-Clause',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['grako==2.4.1', 'ipaddr==2.1.11'],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Programming Language :: Python"
                   ],
      zip_safe=False,
      entry_points={'console_scripts': ['aclhound = aclhound.cli:main']})

if 'install' in sys.argv:
    pwd = os.path.dirname(os.path.abspath(__file__))
    man_path = '/usr/share/man/man7/'
    if os.path.exists(man_path):
        print "Installing man pages"
        path = "%s/doc/aclhound.7" % pwd
        input_file = file(path).read()
        ouput_file = file(man_path + 'aclhound.7', 'wa')
        ouput_file.write(input_file)
