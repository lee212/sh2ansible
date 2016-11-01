import os
import os.path
import json
import yaml

def TBD():
    return

class sh2Ansible(object):
    """ Provide a converted ansible script from shell script 

        Currently these are supported:

        # 1. packages
        - [sudo] [package manager] [name(s)]
          => 
          {
            - name: [l0] sudo package manager names
              package: 
                name: value(s)
                become: true|false
          }

        # 2. shell commands
        - others -> shell: 
    
    """

    converted = []

    def __init__(self):
        pass

    def read_bash(self, stdin_or_path):

        if os.path.isfile(stdin_or_path):
            self.read_from_file(stdin_or_path)
        else:
            TBD
            #self.read_from_stdin(path)

    def read_from_file(self, filename):
        with open(filename, "r") as f:
            content = f.read()
        self.bash_content = content

    def convert(self):
        if not self.bash_content:
            return False

        bcontent = self.bash_content

        converted = self.converted
        line_number = 0
        # convert line by line
        for line in bcontent.split("\n"):
            # level of shell commands
            #
            # use case 1.
            # [elevate privileges] [package manager] (name)+
            # [sudo] [apt-get|yum|brew|dpkg|pip]

            # features 
            # - divided by white spaces

            if line == "":
                continue

            # model
            # { "task_name": [line number] + original command,
            #   "become": true|false,
            #   "module": package manager,
            #   "name": name(s),
            # }, ...

            linedict = Line(line)
            line_number += 1
            converted.append(dict(linedict))

    def export(self):
        self.converted = [{'hosts': 'all', 'tasks': self.converted}]
        return yaml.dump(self.converted, default_flow_style=False)

class Line(dict):
    pointer = 0
    divided = []
    def __init__(self, line):
        self.original = line
        self['name'] = line
        try:
            self.divided = line.split()
        except:
            self.divided = []
        self.parse()

    def parse(self):
        self.name = " ".join(self.original)
        self.become()
        self.module()
        self.options()
       
    def become(self):
        if self.divided[0] == "sudo":
            become = True
            self.pointer += 1
        else:
            become = False
        self["become"] = become

    def module(self):
        # TODO: dpkg, apt-cache, dnf, make, pkg are not included
        if self.divided[self.pointer] == "apt-get":
            module = "apt"
        if self.divided[self.pointer] == "yum":
            module = "yum"
        self.module = module
        self[module] = {}

    def options(self):
        func = getattr(self, self.module + "_options")
        func()

    def apt_options(self):
        cmd = self.divided[self.pointer + 1]
        options = self.divided[(self.pointer + 2):]
        module = self.module
        if cmd == "install":
            self[module]['state'] = 'present'
        elif cmd == "remove":
            self[module]['state'] = 'absent'
        elif cmd == "update":
            self[module]['update_cache'] = 'yes'
        elif cmd == "upgrade":
            self[module]['upgrade'] = "yes"
        elif cmd == "dist-upgrade":
            self[module]['upgrade'] = "dist"

        if "--no-install-recommends" in options:
            self[module]['install_recommends'] = "no"
            idx = options.index("--no-install-recommends")
            options.pop(idx)

        if len(options) > 1:
            self[module]['name'] = '{{ item }}'
            self['with_items'] = options
        else:
            self[module]['name'] = options

def main():

    sh2ansible = sh2Ansible()
    if len(os.sys.argv) > 1:
        sh2ansible.read_bash(os.sys.argv[1])
    sh2ansible.convert()
    print sh2ansible.export()

main()
