cisco_ios_upgrade
=========

<<<<<<< HEAD
An Ansible role to maintain the system IOS software (backup, gather facts, cleaning, staging, verifying, and booting) on Cisco network devices.
=======
An Ansible role to maintain the system IOS/IOS-XE software (backup, gather facts, cleaning, staging, verifying, installing and
booting) on Cisco network devices.
>>>>>>> origin/dev
```
    cd roles
    git clone https://github.com/lorephoenix/ansible-cisco_ios_upgrade cisco_ios_upgrade
```

Requirements
------------

This role makes use of the Ansible Cisco IOS and ansible.netcommon collection.
Both collections includes a variety of Ansible content to help automate the management of Cisco network appliances. 

To install the collection:
```
    cd cisco_ios_upgrade
    ansible-galaxy collection install -r requirements.yml
```

Role Variables
--------------

#### 1. defaults/main.yml

The backup variables are needed when you want to copy the current running 
configuration to a specific path on the Ansible Controller.

* `backup`: Enable or disable the function to make backups of running-configs from remote devices.
* `backup_dir`: Configuration backups into hierarchy based in DIR.
* `backup_clean`: Enable or disable cleanup on the oldest stored configuration files.
* `backup_keep`: Only keep the `number` newest changed configuration files.
```
    backup: <Boolean>
    backup_dir: <String>
    backup_cleanup: <Boolean>
    backup_keep: <Integer>
```

* `booting`: Enable or disable the function to update the boot variable.
* `cleaning`: Enable or disable the function to do some cleanup on unused images.
* `data_transfer`: Only options are "download" or "upload". Download initiates the Cisco command "copy" on the remote network device to copy the image from a server. With upload it push the image from the Ansible controller to the remote device.
* `data_protocol`: Specify a network protocol.
* `data_upload_path`: Specify the location where the binary files are located.
* `reload_in`: Define the delayed time to reboot the network device.
  If the value is 0 then the reload will be initiated immediately.
* `remote_ssh_servers`: Specify a list of hostnames/IP addresses to get the images from.
```
    booting: <Boolean>
    cleaning: <Boolean>
    data_transfer: <String>
    data_protocol: <String>
    data_upload_path: <String>
    reload_in: <Integer>
    remote_ssh_servers: <List>
```

Below variables will enable or disable to display the debug variables.
```
    debug_all: <Boolean>
    debug_filter: <Boolean>
```

<<<<<<< HEAD
#### 2. vars/\<ansible_net_iostype\>/\<model_variant\>/\<model_variant\>.yml

The directory "vars" contains sub-directories. The sub-directories have uniqiue Cisco model variant names. 
The Cisco model variant name is an extraction from the gather facts variable "ansible_net_model".
=======
#### 2. vars/\<model_variant\>/\<model_variant\>.yml

The directory "vars" contains sub-directories. The sub-directories have uniqiue Cisco model variant names. 
The Cisco modell variant name is an extraction from the gather facts variable "ansible_net_model".
>>>>>>> origin/dev
Inside each sub-directory contains a filename with the same model variant string.

* `model_supported`: Flag if the model is supported or not.
* `required_ios_binary`: Specify the binary image filename.
* `required_ios_md5`: MD5 checksum value for the image.
* `required_ios_sha512`: SHA512 checksum value for the image.
* `required_ios_version`: Specify the image version number.
* `required_ios_size_kb`: Specify the file size of the binary image .
* `use_signature`: Which validation signature (MD5 or SHA512) it needs to use.

```
    model_supported: <Boolean>
    required_ios_binary: <String>
    required_ios_md5: <String>
    required_ios_sha512: <String>
    required_ios_size_kb: <Integer>
    required_ios_version: <String>
    use_signature: <String>
```

#### 3. Other variables for the role

You can store variables in the main inventory file or storing separate host and group variable files. Host and group variable files must use YAML syntax. Valid file extensions include ‘.yml’, ‘.yaml’, ‘.json’, or no file extension. 

* `ansible_become`: Equivalent of the become directive, decides if privilege escalation is used or not.
* `ansible_become_method`: Which privilege escalation method should be used.
* `ansible_become_password`: Set the privilege escalation password (never store this variable in plain text; always use a vault).
* `ansible_connection`: Connection type to the host. The string "ansible.netcommon.network_cli" is part of the ansible.netcommon collection.
* `ansible_network_os`: Informs Ansible which Network platform this hosts corresponds to. The string "ios" is part of the Cisco IOS collection.
* `ansible_user`: The default ssh user name to use.
* `ansible_password`: The ssh password to use (never store this variable in plain text; always use a vault).

```
    ansible_become: <Boolean>
    ansible_become_method: enable
    ansible_become_password: <Vault String>
    ansible_connection: ansible.netcommon.network_cli
    ansible_network_os: cisco.ios.ios
    ansible_user: <String>
    ansible_password: <Vault String>
```

Below variables are required when the variable "data_transfer", which is stored on "defaults/main.yml",  is set with the string "download".

* `remote_ssh_user`: The default ssh user name to use.
* `remote_ssh_password`: The ssh password to use (never store this variable in plain text; always use a vault).

```
    remote_ssh_user: <String>
    remote_ssh_password: <Vault String>
```


Modes of Operation
------------

The role has 6 distinct modes of operation following the same order as below:

* **backup**: Make running configuration backup from the remote device.
* **facts**: Just gather facts about the remote device and compare against the version it should be running
* **cleaning**: Clean unused images from the storage on the remote device to make room for new firmware.
* **staging**: Stage the software on the remote device storage.
* **verifying**: Check the checksum to make sure that the image is on the remote device storage and intact.
<<<<<<< HEAD
=======
* **installing**: Unpack & distribute the software and create a package configuration file. (only on IOS-XE software)
>>>>>>> origin/dev
* **booting**: Put the software into service and reboot.


Example Playbook
----------------

This is an example playbook:
```
    - hosts: cisco
      gather_fact: no
      roles:
         - cisco_ios_upgrade
```

To run a specific mode, simply specify the mode by using the tag attribute.

Using attribute tag 'backup' will only backup of the running configuration but it requires to enable the default variable 'backup'.
```
ansible-playbook your_playbook_name.yml -i your_inventory_file --tag backup -e "backup=yes"
```

Using attribute tag 'facts' will only gather device information.
```
ansible-playbook your_playbook_name.yml -i your_inventory_file --tag facts
```

Using the attribute tag 'cleaning' will only process the operation mode 'facts' and 'cleaning' in that same order.
```
ansible-playbook your_playbook_name.yml -i your_inventory_file --tag cleaning -e "cleaning=yes"
```

Using the attribute tag 'staging' to upload the IOS image from the Ansible Controller to a specific remote device.
If the mode operation 'facts' detect that the IOS image already exist then it stops after the operation 'facts'.
```
ansible-playbook your_playbook_name.yml -i your_inventory_file --tag staging \
    -e "data_transfer=upload" --limit inventory_hostname
```

<<<<<<< HEAD
=======
Open IOS-XE Caveats
--------------

* If you encounter issues during the IOS-XE verification task due to timeout then use the [new libssh connection plugin](https://www.ansible.com/blog/new-libssh-connection-plugin-for-ansible-network) instead of Paramiko connection plugin.
* No support for devices running IOS-XE with Bundle mode
* Only able to upgrade IOS-XE software from Fuji version, since it is required to have the command "install add file"
>>>>>>> origin/dev



License
-------

MIT

Author Information
------------------

- Christophe Vermeren | [GitHub](https://github.com/lorephoenix) | [Facebook](https://www.facebook.com/cvermeren)
<<<<<<< HEAD
=======

>>>>>>> origin/dev
