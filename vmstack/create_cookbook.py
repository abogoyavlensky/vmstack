import argparse
from cookbook_generator import CookbookGenerator

def main():
    parser = argparse.ArgumentParser(description="Cookbook Generator")

    parser.add_argument('-n', '--name_of_cookbook',default= 'my_cookbook',help='Specify the name of your cookbook')
    parser.add_argument('-p', '--name_of_packages', nargs='*',default = '', help='Specify the name of your packages')
    args = parser.parse_args()

   # name_folder_cb = 'my_cookbook'
    dict_args = vars(args)
    if dict_args['name_of_cookbook']==None:
        print 'Enter the name your cookbook'
    else:
        packages = []
        arg_packs = dict_args['name_of_packages']
        if arg_packs!=None:
            for x in arg_packs:
                if x!=None:
                    packages.append(x)
        cookbook_obj = CookbookGenerator()
        cookbook_obj.generate_cookbook(packages,dict_args['name_of_cookbook'])


if __name__=='__main__':
    main()
