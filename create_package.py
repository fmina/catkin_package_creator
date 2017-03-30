import sys
from PyQt4.QtGui import *
from PyQt4.uic import *
import os
import datetime

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi('main.ui', self)
        self.show()
        #nodes
        self.AddNodeButton.clicked.connect(self.addNodeButtonCallback)
        self.DeleteNodeButton.clicked.connect(self.deleteNodeButtonCallback)

        #libs
        self.AddLibraryButton.clicked.connect(self.addLibraryButtonCallback)
        self.DeleteLibraryButton.clicked.connect(self.deleteLibraryButtonCallback)

        #msgs
        self.AddMessageButton.clicked.connect(self.addMessageButtonCallback)
        self.DeleteMessageButton.clicked.connect(self.deleteMessageButtonCallback)

        #srvs
        self.AddServiceButton.clicked.connect(self.addServiceButtonCallback)
        self.DeleteServiceButton.clicked.connect(self.deleteServiceButtonCallback)

        #depndencies
        self.AddDependencyButton.clicked.connect(self.addDependencyButtonCallback)
        self.DeleteDependencyButton.clicked.connect(self.deleteDependencyButtonCallback)

        self.CreatePackageButton.clicked.connect(self.createPackageCallback)

        self.templates_dir = 'templates'


    def addNodeButtonCallback(self):
        text, ok = QInputDialog.getText(self, 'Node Name','Enter node name: ')
        if ok:
            text = text.toLower()
            self.NodesList.addItem(text)

    def deleteNodeButtonCallback(self):
        for item in self.NodesList.selectedItems():
            self.NodesList.takeItem(self.NodesList.row(item))

    def addLibraryButtonCallback(self):
        text, ok = QInputDialog.getText(self, 'Library Name','Enter library name:')
        if ok:
            text = text.toLower()
            text.replace(" ", "")
            if not self.isValidName(text):
                return
            self.LibraryList.addItem(text)

    def deleteLibraryButtonCallback(self):
        for item in self.LibraryList.selectedItems():
            self.LibraryList.takeItem(self.LibraryList.row(item))

    def addMessageButtonCallback(self):
        text, ok = QInputDialog.getText(self, 'Message Name','Enter message name:')
        if ok:
            text = text.toLower()
            text.replace(" ", "")
            if not self.isValidName(text):
                return
            self.MessageList.addItem(text)

    def deleteMessageButtonCallback(self):
        for item in self.MessageList.selectedItems():
            self.MessageList.takeItem(self.MessageList.row(item))

    def addServiceButtonCallback(self):
        text, ok = QInputDialog.getText(self, 'Service Name','Enter service name:')
        if ok:
            text = text.toLower()
            text.replace(" ", "")
            if not self.isValidName(text):
                return
            self.ServiceList.addItem(text)

    def deleteServiceButtonCallback(self):
        for item in self.ServiceList.selectedItems():
            self.ServiceList.takeItem(self.ServiceList.row(item))

    def addDependencyButtonCallback(self):
        text, ok = QInputDialog.getText(self, 'Dependency Name','Enter dependency name:')
        if ok:
            text = text.toLower()
            text.replace(" ", "")
            if not self.isValidName(text):
                return
            self.DependencyList.addItem(text)

    def deleteDependencyButtonCallback(self):
        for item in self.DependencyList.selectedItems():
            self.DependencyList.takeItem(self.DependencyList.row(item))


    def createPackageCallback(self):
        main_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if not main_dir:
            return

        package_name = self.PackageNameLineEdit.text()
        package_name.replace(" ", "")
        package_name = package_name.toLower()

        self.author_name = str(self.AuthorNameLineEdit.text())
        self.author_email = str(self.AuthorEmailLineEdit.text())
        self.pacakge_description = str(self.PackageDescriptionLineEdit.text())

        if not self.author_name:
            print "Error: author name should not be empty"
            return

        if not self.author_email:
            print "Error: author_email should not be empty"
            return

        if not self.pacakge_description:
            print "Error: pacakge_descriptionshould not be empty"
            return

        namespace = self.NamespaceLineEdit.text()
        namespace.replace(" ", "")
        namespace = namespace.toLower()
        self.namespace = str(namespace)

        if not self.isValidName(package_name):
            self.PackageNameLineEdit.clear()
            return

        package_name = str(package_name)
        self.packge_name = package_name

        main_dir = main_dir + '/' + package_name
        src_dir = main_dir + '/src'
        include_dir = main_dir + '/include/' + package_name
        msg_dir = main_dir + '/msg'
        srv_dir = main_dir + '/srv'

        if not os.path.exists(main_dir):
            os.makedirs(main_dir)

        #create nodes and libs
        if self.NodesList.count() > 0 or self.LibraryList.count() > 0:
            if not os.path.exists(src_dir):
                os.makedirs(src_dir)
            if not os.path.exists(include_dir):
                os.makedirs(include_dir)
        nodes_list = []
        for i in range(self.NodesList.count()):
            node_name = str(self.NodesList.item(i).text())
            nodes_list.append(node_name)
            self.createNodeSrcFile(src_dir, node_name)

        libs_list = []
        for i in range(self.LibraryList.count()):
            lib_name = str(self.LibraryList.item(i).text())
            libs_list.append(lib_name)
            self.createLibrarySrcFile(src_dir, lib_name)
            self.createLibraryHeaderFile(include_dir, lib_name)

        #create msgs
        if self.MessageList.count() > 0:
            if not os.path.exists(msg_dir):
                os.makedirs(msg_dir)

        for i in range(self.MessageList.count()):
            msg_name = str(self.MessageList.item(i).text())
            self.createMessageFile(msg_dir, msg_name)

        #create srvs
        if self.ServiceList.count() > 0:
            if not os.path.exists(srv_dir):
                os.makedirs(srv_dir)

        for i in range(self.ServiceList.count()):
            srv_name = str(self.ServiceList.item(i).text())
            self.createServiceFile(srv_dir, srv_name)

        #create package.xml
        dependency_string = ""
        for i in range(self.DependencyList.count()):
            dependency = str(self.DependencyList.item(i).text())
            dependency_string = dependency_string + "  <depend>"+dependency+"</depend>\n"

        self.createPackageXML(main_dir, dependency_string)

        #create cmakelists.txt
        self.createCmakeLists(main_dir, libs_list, nodes_list)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Success")
        msg.setInformativeText("Successfully created package in \n" + main_dir)
        msg.setWindowTitle("Message")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def isValidName(self, string):
        if not string.at(0).isLetter():
            print "Error: invalid name"
            return False

        return True

    def createNodeSrcFile(self, dir, node_name):
        file_name = dir + '/' + node_name + '_node.cpp'
        file = open(file_name, 'w')
        template_file = open(self.templates_dir + '/NODE_SRC', 'r')
        for line in template_file:
            now = datetime.datetime.now()
            new_line = line.replace('@###Year####', str(now.year))
            new_line = new_line.replace('@###PackageAuthor####', self.author_name)
            new_line = new_line.replace('@###AuthorEmail####', self.author_email)

            tmp1 = node_name.replace("_", " ")
            tmp2 = tmp1.replace("-", " ")
            tmp3 = tmp2.title()
            camel_case_name = tmp3.replace(" ", "")
            camel_case_name = camel_case_name + "Node"
            new_line = new_line.replace('@###NodeName####', camel_case_name)
            file.write(new_line)

        file.close()
        template_file.close()

    def createLibrarySrcFile(self, dir, lib_name):
        file_name = dir + '/' + lib_name + '.cpp'
        file = open(file_name, 'w')
        template_file = open(self.templates_dir + '/LIB_SRC', 'r')
        for line in template_file:
            now = datetime.datetime.now()
            new_line = line.replace('@###Year####', str(now.year))
            new_line = new_line.replace('@###PackageAuthor####', self.author_name)
            new_line = new_line.replace('@###AuthorEmail####', self.author_email)
            new_line = new_line.replace('@###Namespace####', self.namespace)
            new_line = new_line.replace('@###PackageName####', self.packge_name)
            new_line = new_line.replace('@###LibraryHeaderFileName####', lib_name + '.h')


            tmp1 = lib_name.replace("_", " ")
            tmp2 = tmp1.replace("-", " ")
            tmp3 = tmp2.title()
            camel_case_name = tmp3.replace(" ", "")
            new_line = new_line.replace('@###LibraryName####', camel_case_name)
            file.write(new_line)

        file.close()
        template_file.close()

    def createLibraryHeaderFile(self, dir, lib_name):
        file_name = dir + '/' + lib_name + '.h'
        file = open(file_name, 'w')
        template_file = open(self.templates_dir + '/LIB_HEADER', 'r')
        for line in template_file:
            now = datetime.datetime.now()
            new_line = line.replace('@###Year####', str(now.year))
            new_line = new_line.replace('@###PackageAuthor####', self.author_name)
            new_line = new_line.replace('@###AuthorEmail####', self.author_email)
            new_line = new_line.replace('@###Namespace####', self.namespace)
            include_guard = self.packge_name + '_include_'+ self.packge_name + '_' + lib_name + '_h'
            include_guard = include_guard.upper()
            new_line = new_line.replace('@###IncludeGuard####', include_guard)

            tmp1 = lib_name.replace("_", " ")
            tmp2 = tmp1.replace("-", " ")
            tmp3 = tmp2.title()
            camel_case_name = tmp3.replace(" ", "")
            new_line = new_line.replace('@###LibraryName####', camel_case_name)
            file.write(new_line)

        file.close()
        template_file.close()

    def createMessageFile(self, dir, msg_name):
        file_name = dir + '/' + msg_name + '.msg'
        file = open(file_name, 'w')
        file.close()

    def createServiceFile(self, dir, srv_name):
        file_name = dir + '/' + srv_name + '.srv'
        file = open(file_name, 'w')
        file.close()

    def createPackageXML(self, dir, dependency_string):
        file_name = dir + '/' + 'package.xml'
        file = open(file_name, 'w')
        template_file = open(self.templates_dir + '/PACKAGE_XML', 'r')
        for line in template_file:
            new_line = line.replace('@###PackageName####', self.packge_name)
            new_line = new_line.replace('@###PackageAuthor####', self.author_name)
            new_line = new_line.replace('@###AuthorEmail####', self.author_email)
            new_line = new_line.replace('@###PackageDescription####', self.pacakge_description)
            new_line = new_line.replace('@###DependenciesHere####', dependency_string)
            file.write(new_line)

        file.close()
        template_file.close()


    def createCmakeLists(self, dir, libs_list, nodes_list):
        add_libs_string = "\n"
        for lib in libs_list:
            add_libs_string = add_libs_string + "cs_add_library(" + lib + "_lib " + "src/" + lib + ".cpp)\n"

        add_exec_string = "\n"
        for node in nodes_list:
            add_exec_string = add_exec_string + "cs_add_executable(" + node + "_node " + "src/" + node + "_node.cpp)\n"

        linking_string = "\n"
        for node in nodes_list:
            for lib in libs_list:
                linking_string = linking_string + "target_link_libraries(" + node + "_node " + lib + "_lib)\n"

        #if there is msg or srv, add depenency on exported target to compile in the correct order
        if self.MessageList.count() > 0 or self.ServiceList.count() > 0:
            for lib in libs_list:
                linking_string = linking_string + "add_dependencies(" + lib + "_lib " + "${PROJECT_NAME}_EXPORTED_TARGETS)\n"

        file_name = dir + '/' + 'CMakeLists.txt'
        file = open(file_name, 'w')
        template_file = open(self.templates_dir + '/CMAKELISTS', 'r')
        for line in template_file:
            new_line = line.replace('@###PackageName####', self.packge_name)
            new_line = new_line.replace('@###AddLibrariesHere####', add_libs_string)
            new_line = new_line.replace('@###AddExecutablesHere####', add_exec_string)
            new_line = new_line.replace('@###LinkLibrariesHere####', linking_string)
            file.write(new_line)

        file.close()
        template_file.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())