# catkin_package_creator
create an empty catkin package

Overview
------

This tool will create a ros package with specified nodes, libraries, messages, services and dependencies.

This code depends on `Qt4`.

Usage
------

```sh
$ git clone git@github.com:fmina/catkin_package_creator.git
$ cd catkin_package_creator
$ python create_package.py
```
The GUI will open. In the upper part please specify the package author's name, email, provide a short package description and specify the namespace and package name. 

The tabs below allow you to define nodes, libraries, messages ..etc. click `Add Node` button to add a new node.

Finally, press `Create Package` to select the directory where the package should be created, typically this will be a Catkin Workspace. 

The created package relies on `catkin_simple` https://github.com/catkin/catkin_simple to solve dependencies.
