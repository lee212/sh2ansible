sh2ansible
===============================================================================

sh2ansible converts a simple shell script to ansible script (playbook) in yaml
format with limitations.

For example, converting shell commands for caffe installation:

.. code-block::

        $ cat examples/caffe.ubuntu.14.04.sh
        sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
        sudo apt-get install --no-install-recommends libboost-all-dev
        sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev

Run sh2ansible script:

.. code-block::

        $ python sh2ansible.py examples/caffe.ubuntu.14.04.sh > caffe.yml

The converted caffe Ansible script:

.. code-block::

        - hosts: all
          tasks:
          - apt:
              name: '{{ item }}'
              state: present
            become: true
            name: sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev
              libhdf5-serial-dev protobuf-compiler
            with_items:
            - libprotobuf-dev
            - libleveldb-dev
            - libsnappy-dev
            - libopencv-dev
            - libhdf5-serial-dev
            - protobuf-compiler
          - apt:
              install_recommends: 'no'
              name:
              - libboost-all-dev
              state: present
            become: true
            name: sudo apt-get install --no-install-recommends libboost-all-dev
          - apt:
              name: '{{ item }}'
              state: present
            become: true
            name: sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev
            with_items:
            - libgflags-dev
            - libgoogle-glog-dev
            - liblmdb-dev


License
-------------------------------------------------------------------------------

GPLv3

Contact
-------------------------------------------------------------------------------

Hyungro Lee (hroe.lee@gmail.com)
