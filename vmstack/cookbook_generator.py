import os
import json

class CookbookGenerator(object):
    """ This class create a dir cookbook with subdirs and all
        needed files for cookbook.
    """
    def generate_cookbook(self,packages,name_folder_cb):
        """ Create all dirs for cookbook with name: name_folder_cb in folder where the program is running,
            else if dir already exists then print error message.
            packages - list of packages to be installed
            Exemple struct of dirs:
            |-my_cookbook
                |-chefsoloconfig.rb
                |-roles
                    -ottobib.json
                |-packages
                    |-recipes
                        -default.rb
        """
    #create dirs structure of cookbook
        path_base = os.getcwd()
        path_cb_dir = path_base + '/' + name_folder_cb
        path_cb_roles = path_cb_dir + '/' + 'roles'
        path_cb_packages = path_cb_dir + '/' + 'packages' + '/' + 'recipes'
        try:
            os.makedirs(path_cb_dir)
            os.makedirs(path_cb_roles)
            os.makedirs(path_cb_packages)
        except OSError:
            print 'Directory with that name already exists!'

    #create chef config file
        name_config_file = 'chefsoloconfig.rb'
        lines_config = []
        lines_config.append('file_cache_path  ' + '"%s/chef-solo"'% path_base)
        lines_config.append('\ncookbook_path    ' + '"%s"' % path_cb_dir)
        lines_config.append('\nlog_level        ' + ':info')
        lines_config.append('\nlog_location     ' + 'STDOUT')
        lines_config.append('\nssl_verify_mode  ' + ':verify_none')
        self._create_files(path_cb_dir,name_config_file,lines_config)

    #create recipes file
        name_recipes_file = 'default.rb'
        lines_recipes = []
        for x in packages:
            lines_recipes.append('package(' + '"%s")\n'% x)
        self._create_files(path_cb_packages,name_recipes_file,lines_recipes)

    #create roles .json - file
        name_roles_file = 'roles_default'
        dict_roles = {}
        dict_roles['name'] = name_roles_file
        dict_roles['run_list'] = ['package']
        lines_roles = json.dumps(dict_roles,indent=4)
        name_roles_file = '%s.json' % name_roles_file
        self._create_files(path_cb_roles,name_roles_file,lines_roles)

    def _create_files(self,path,name_file,lines):
        """ Create files with name: name_file, in dir: path and with
            content: lines
        """
        if os.path.exists(path):
            path = path + '/' + name_file
            f = open(path,'w')
            f.writelines(lines)
            f.close()
        else:
            print 'That path not exist'