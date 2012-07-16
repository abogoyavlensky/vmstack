from distutils.core import setup

setup(name='vmstack',
      version='0.1',
      py_modules=['VMserver', 'WEBapi', 'ChangerPref', 'DBserver', 'VMtable', ],
      data_files=[('templates', ['*.html'])]
      )