from distutils.core import setup

setup(name="pytransmission",
      version="1.0",
      packages=['pytransmission',
                'pytransmission.popgen',
                'pytransmission.aggregation',
],
      author='Mark E. Madsen',
      author_email='mark@pytransmission.org',
      url='https://github.com/mmadsen/pytransmission',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7',
          'Topic :: Scientific/Engineering',
      ]
      )
