from distutils.core import setup

setup(name='vmstack',
      version='0.1',
      py_modules=['user_server', 'vm_server', 'web_api', 'db_server', 'vm_table', 'user_table'],
      data_files=[('sites', [
          'templates/info.html',
          'templates/start.html',
          'templates/stop.html',
          'templates/delete.html',
          'templates/get_ip.html',
          'templates/login.html',
          'templates/index.html',
          'templates/register.html',
          'templates/clone.html',
          'templates/info_out.html',
          'templates/configs.html',
      ])]
      )