#!/usr/bin/env python

import re
from pprint import pprint

# require pip install --upgrade pandas
import pandas as pd


# ███╗    ███████╗    ███╗
# ██╔╝    ██╔════╝    ╚██║
# ██║     █████╗       ██║
# ██║     ██╔══╝       ██║
# ███╗    ██║         ███║
# ╚══╝    ╚═╝         ╚══╝

#    __ _ _ _                                 _      _
#   / _(_) | |_ ___ _ __  _ __ ___   ___   __| | ___| |
#  | |_| | | __/ _ \ '__|| '_ ` _ \ / _ \ / _` |/ _ \ |
#  |  _| | | ||  __/ |   | | | | | | (_) | (_| |  __/ |
#  |_| |_|_|\__\___|_|___|_| |_| |_|\___/ \__,_|\___|_|
#                   |_____|
#


def filter_model(model_arg, debug=False):
    ''' filter_model
        Matches the characters from keyword value at the start of each
        newline.

        Args:
            model: Cisco model
            debug: passing Boolean to enable/disable debug
    '''

    dp = Verbosity()
    model = ""

    if debug:
        dp.v_debug("Start of def filter_model()")
    # End of if debug:

    if isinstance(model_arg, str):
        # The passed argument is a string

        if debug:
            dp.v_debug("(filter_model) The arhument model_arg is a string.")

        # Split a string into a list using character minus (-) as separator
        # but only keep the first 2 elements of the list.
        stripped_model = model_arg.split('-')[0:2]

        if stripped_model[0].upper() == 'WS':
            # The first element has the string 'WS', which stands for
            # Workgroup Switch.

            if debug:
                dp.v_debug(
                    "(filter_model) Detected that the string starts with 'WS'")
            # End of if debug:
            model = '-'.join(stripped_model)
        # End of if stripped_model[0].upper() == 'WS':

        else:
            # The first element doesn't have the string 'WS'.
            # This can be a router or the latest Cisco Catalyst switches
            # which start with the character 'C' like :
            # C9200-24T, C9200L-24P-4X, C9300-24U, ...
            # Most routers will start with the string CISCO or ISR but most
            # likely have the character slash '/'.

            if debug:
                dp.v_debug((
                    "(filter_model) Detected that the string doesn't start "
                    "with 'WS'"))
            # End of if debug:

            # Split string into a list using the character slash '/' as
            # separator and return with the first element of the list.
            model = stripped_model[0].split('/')[0]
        # End of else:
    # End of if isinstance(model_arg, str):

    else:
        # The passed argument is NOT a string
        message = "(filter_model) The passed model argument isn't a string."
        dp.v_error(message)
        return model
    # End of else:

    if debug:
        dp.v_debug("(filter_model) model = '" + model + "'")
        dp.v_debug("End of def filter_model()")
    # End of if debug:

    return model.upper()

#    __ _           _                                                  _
#   / _(_)_ __   __| |    ___ ___  _ __ ___  _ __ ___   __ _ _ __   __| |___
#  | |_| | '_ \ / _` |   / __/ _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` / __|
#  |  _| | | | | (_| |  | (_| (_) | | | | | | | | | | | (_| | | | | (_| \__ \
#  |_| |_|_| |_|\__,_|___\___\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|___/
#                   |_____|


def find_commands(data, command, debug=False):
    ''' find_commands
        Build a dictionary of Cisco exisiting upgrade commands that can be
        used.

        Args:
            data: contains the output from exec command '?'
            command: command string
            debug: passing Boolean to enable/disable debug
        '''
    dp = Verbosity()
    flag = False

    if debug:
        dp.v_debug("Start of def find_commands()")
    # End of if debug:

    [error, raw_list] = stdout(data, 'find_commands')

    if error:
        return False
    # End of if error:

    if not isinstance(command, str):
        dp.error("(find_commands) The passed command isn't a string.")
        return False
    # End of if not isinstance(command, str):

    # Split string into a list.
    command_list = command.split()

    if len(command_list) == 0:
        dp.error("(find_commands) The passed command is empty.")
        return False
    # End of if len(command_list) == 0:

    elif len(command_list) == 1:
        set_cmd = command_list[0].strip()
    # End of elif len(command_list) == 1:

    else:
        set_cmd = command_list[-1].strip()
    # End of else:

    for line in raw_list:
        # Loop through each output line

        line = line.strip()  # Remove leading and trailing spaces

        cond = re.match('^(' + re.escape(set_cmd) + ')\\s+', line)

        if cond:
            if debug:
                dp.v_debug("Found line: " + line)
            # End of if debug:

            flag = True
        # End of if cond:
    # End of for line in raw_list:

    if debug:
        message = "(find_commands) flag = " + \
            str(flag) + " <" + str(type(flag))
        message += ">"
        dp.v_debug(message)
        dp.v_debug("End of def find_commands()")
    # End of if debug:

    return flag

#    __ _           _      __ _ _                     _
#   / _(_)_ __   __| |    / _(_) | ___  ___ ___ _   _| |_ ___ _ __ ___  ___
#  | |_| | '_ \ / _` |   | |_| | |/ _ \/ __/ __| | | | __/ _ \ '_ ` _ \/ __|
#  |  _| | | | | (_| |   |  _| | |  __/\__ \__ \ |_| | ||  __/ | | | | \__ \
#  |_| |_|_| |_|\__,_|___|_| |_|_|\___||___/___/\__, |\__\___|_| |_| |_|___/
#                   |_____|                     |___/


def find_filesystems(data, version_list, default_fs, debug=False):
    ''' find_filesystems
        Build a dictionary of Cisco exisiting upgrade commands that can be
        used.

        Args:
            data: contains the output from exec command 'show ?'
            version_list: a list of possible switch memmbers
            default_fs
            debug: passing Boolean to enable/disable debug
        '''
    dp = Verbosity()
    filesystems = []  # Initialize empty list
    extract = default_fs.split(':')[0]

    if debug:
        dp.v_debug("Start of def find_filesystems()")
    # End of if debug:

    [error, raw_list] = stdout(data, 'find_filesystems')

    if len(version_list) == 0:
        # From previous task a 'show version' will not generate any data for
        # router devices.
        filesystems.append(default_fs)
    # End of if len(version_list) == 0:

    elif len(version_list) == 1:
        # From previous task a 'show version' on standalone switch will contain
        # only 1 element on the version_list.
        filesystems.append(default_fs)
    # End of elif len(version_list) == 1:

    else:
        for item in version_list:
            if 'Switch' in item:
                # Found key 'Switch' on dict

                for line in raw_list:
                    line = line.strip()  # Remove leading and trailing spaces

                    string1 = extract + '-' + item['Switch'] + ':'
                    string2 = extract + item['Switch'] + ':'
                    cond1 = re.match('^(' + re.escape(string1) + ')\\s+', line)
                    cond2 = re.match(
                        '^(' + re.escape(string2) + ':)\\s+', line)

                    if cond1:
                        filesystems.append(string1)
                        if debug:
                            dp.v_debug("Found line: " + line)
                        # End of if debug:
                    # End of if cond1:

                    if cond2:
                        filesystems.append(string2)
                        if debug:
                            dp.v_debug("Found line: " + line)
                        # End of if debug:
                    # End of if cond2:
                # End of for line in raw_list:
            # End of if 'Switch' in item:
        # End of for item in version_list:
    # End of else:

    if debug:
        dp.v_debug("End of def find_filesystems()")
    # End of if debug:

    return filesystems


# ███╗    ██╗    ███╗
# ██╔╝    ██║    ╚██║
# ██║     ██║     ██║
# ██║     ██║     ██║
# ███╗    ██║    ███║
# ╚══╝    ╚═╝    ╚══╝


#   _                __ _           _  __ _ _
#  (_) ___  ___     / _(_)_ __   __| |/ _(_) | ___
#  | |/ _ \/ __|   | |_| | '_ \ / _` | |_| | |/ _ \
#  | | (_) \__ \   |  _| | | | | (_| |  _| | |  __/
#  |_|\___/|___/___|_| |_|_| |_|\__,_|_| |_|_|\___|
#             |_____|

def ios_findfile(data, alist, binfile, debug=False):
    ''' ios_findfolder

        Args:
            data: contains the output from the running IOS command
            alist: passing list to append data into it
            binfile: passing string with name of binary file
            debug: passing Boolean to enable/disable debug
        '''
    dp = Verbosity()
    data_list = []

    if debug:
        dp.v_debug("Start of def ios_findfile()")
        message = "(ios_findfile) The passed argument 'data' is a " + \
            str(type(data))
        dp.v_debug(message)
        message = "(ios_findfile) The passed argument 'alist' is a " + \
            str(type(alist))
        dp.v_debug(message)
        message = "(ios_findfile) The passed argument 'binfile' is a " + \
            str(type(binfile))
        dp.v_debug(message)
    # End of if debug:

    cond = (not isinstance(data, list) or not isinstance(
        alist, list) or not isinstance(binfile, str))

    if cond:
        message = "(ios_findfile) One or both passed arguments wasn't " + \
            "able to pass the condition. 'data' = <<list>> , 'folder' = " + \
            "<<string>>"
        dp.v_error(message)
        return data_list

    for item in data:
        new_dict = {'filesystem': None, 'filename': None}

        if "item" in item:
            key = "item"
            label = "filesystem"
            new_dict['filesystem'] = ios_findfile_item(
                item, key, label, 'ios_findfile', debug)

            if "stdout" in item:
                key = "stdout"
                label = None

                if debug:
                    dp.v_debug("(ios_findfile) Found dictionary key 'stdout'.")

                lines = ios_findfile_item(item, key, label, debug)

                new_dict['filename'] = parse_filefolder(
                    lines, binfile, '-rw', 'ios_findfile', debug)
        # End of if "item" in item:

        data_list.append(new_dict)
    # End of for item in data:

    df1 = pd.DataFrame(alist).set_index('filesystem')
    df2 = pd.DataFrame(data_list).set_index('filesystem')
    df = df1.merge(df2, left_index=True, right_index=True)
    data_list = df.T.to_dict()

    if debug:
        dp.v_debug("End of def ios_findfile()")
    # End of if debug:

    return data_list


def ios_findfile_item(item_object, key, label=None,
                      from_function=None, debug=False):
    ''' ios_findfile_item

        Args:
            item_object: passing object
            key: passing key name
            label: passing label to find
            from_function: passing function name that initiate this function
            debug: passing Boolean to enable/disable debug

    '''
    dp = Verbosity()
    rvalue = None

    if debug:
        dp.v_debug("Start of def ios_findfile_item()")

    if isinstance(item_object[key], dict):
        if debug:
            message = "(" + from_function + ") The variable item[" + key + \
                "] is a dictionary."
            dp.v_debug(message)
        # End of if debug:

        if label in item_object[key]:
            rvalue = item_object[key][label]

            if debug:
                message = "(" + from_function + ") The dictionary item[" + key
                message += "] contains the key '" + label + "'."
                dp.v_debug(message)
                dp.v_debug("(" + from_function + ") " + label + " = " + rvalue)
            # End of if debug:
        # End of if label in item_object[key]:
    # End of if isinstance(item_object[key], dict):

    elif isinstance(item_object[key], list):
        if debug:
            message = "(" + from_function + ") The variable item['" + key + \
                "'] is a list."
            dp.v_debug(message)
        # End of if debug:
        rvalue = item_object[key][0].split('\n')

    elif isinstance(item_object[key], str):
        if debug:
            message = "(" + from_function + ") The variable item['" + key + \
                "'] is a string."
            dp.v_debug(message)
        # End of if debug:

        rvalue = item_object[key]
    # End of elif isinstance(item_object[key], str):

    if debug:
        dp.v_debug("End of def ios_findfile_item()")
    return rvalue

#   _                __ _           _  __       _     _
#  (_) ___  ___     / _(_)_ __   __| |/ _| ___ | | __| | ___ _ __
#  | |/ _ \/ __|   | |_| | '_ \ / _` | |_ / _ \| |/ _` |/ _ \ '__|
#  | | (_) \__ \   |  _| | | | | (_| |  _| (_) | | (_| |  __/ |
#  |_|\___/|___/___|_| |_|_| |_|\__,_|_|  \___/|_|\__,_|\___|_|
#             |_____|


def ios_findfolder(data, folder, debug=False):
    ''' ios_findfolder

        Args:
            data: contains the output from the running IOS command
            source: passing string with name of folder
            debug: passing Boolean to enable/disable debug
        '''
    dp = Verbosity()
    data_list = []

    if debug:
        dp.v_debug("Start of def ios_findfolder()")
        message = "(ios_findfolder) The passed argument 'data' is a " + \
            str(type(data))
        dp.v_debug(message)
        message = "(ios_findfolder) The passed argument 'folder' is a " + \
            str(type(folder))
        dp.v_debug(message)
    # End of if debug:

    if not isinstance(data, list) or not isinstance(folder, str):
        message = "(ios_findfolder) One or both passed arguments wasn't " + \
            "able to pass the condition. 'data' = <<list>> , 'folder' = " + \
            "<<string>>"
        dp.v_error(message)
        return data_list

    for item in data:
        new_dict = {}
        new_dict['filesystem'] = ""
        new_dict['directory'] = ""

        if "item" in item:
            new_dict['filesystem'] = item['item']  # Set name of filesystem

            if "stdout" in item:
                lines = item['stdout'][0].split('\n')

                new_dict['directory'] = parse_filefolder(
                    lines, folder, 'drw', 'ios_findfolder', debug)
            # End of if "stdout" in item:
        # End of if "item" in item:
        data_list.append(new_dict)
    # End of for item in data:

    if debug:
        message = "(ios_findfolder) " + str(type(data_list))
        message += " data_list = "
        dp.v_debug(message)
        pprint(data_list)
        dp.v_debug("End of def ios_findfolder()")
    # End of if debug:

    return data_list


#   _
#  (_) ___  ___      _ __   __ _ _ __ ___  ___
#  | |/ _ \/ __|    | '_ \ / _` | '__/ __|/ _ \
#  | | (_) \__ \    | |_) | (_| | |  \__ \  __/
#  |_|\___/|___/____| .__/ \__,_|_|  |___/\___|
#           _ |_____|_|           __ _ _
#        __| | __ _| |_ __ _     / _(_) | ___  ___
#       / _` |/ _` | __/ _` |   | |_| | |/ _ \/ __|
#      | (_| | (_| | || (_| |   |  _| | |  __/\__ \
#   ____\__,_|\__,_|\__\__,_|___|_| |_|_|\___||___/
#  |_____|                 |_____|

def ios_parse_data_files(lines, **kwargs):
    ''' ios_parse_data_files

        Args:
            lines: contains the output of the dir of that specific
            kwargs: passing keyword ( or named) arguments
    '''
    dp = Verbosity()
    new_list = []

    runfile = re.escape(kwargs['running_ios'])
    rundir = re.escape(kwargs['running_dir'])
    reqdir = re.escape(kwargs['required_dir'])
    f = re.escape(kwargs['filter'])

    for line in lines:
        line = line.strip()  # Remove leading and trailing spaces

        # Build conditional to ignore the running IOS binary file, if exist.
        cond1 = re.match('^[0-9]+\\s+(-rw).*\\s+(' + runfile + ')$', line)

        # Build conditional to ignore the directories that contains the name of
        # the running IOS and required IOS, if exist.
        cond2 = re.match(
            '^[0-9]+\\s+(drw).*\\s+(' + rundir + '|' + reqdir + ')$', line)

        # Build conditional to keep files and directories that contains the
        # model variant name that is extracted from the required IOS.
        cond3 = re.match('^[0-9]+\\s+.*\\s+(' + f + ').*$', line)

        if (not (cond1 or cond2)) and cond3:
            if kwargs['debug']:
                dp.v_debug("Found line: " + line)
            # End of if kwargs['debug']:

            new_list.append(line.split()[-1])

        # End of if (not (cond1 and cond2)) and cond3:
    # End of for line in lines:

    return new_list

#   _                                              _       _
#  (_)                                            | |     | |
#   _  ___  ___     _ __   __ _ _ __ ___  ___   __| | __ _| |_ __ _
#  | |/ _ \/ __|   | '_ \ / _` | '__/ __|/ _ \ / _` |/ _` | __/ _` |
#  | | (_) \__ \   | |_) | (_| | |  \__ \  __/| (_| | (_| | || (_| |
#  |_|\___/|___/   | .__/ \__,_|_|  |___/\___| \__,_|\__,_|\__\__,_|
#            ______| |                     ______                ______
#    __     |______|_|      _      _   _  |______|              |______|
#   / _|            | |    | |    | | (_)
#  | |_ ___  _ __ __| | ___| | ___| |_ _  ___  _ __
#  |  _/ _ \| '__/ _` |/ _ \ |/ _ \ __| |/ _ \| '_ \
#  | || (_) | | | (_| |  __/ |  __/ |_| | (_) | | | |
#  |_| \___/|_|  \__,_|\___|_|\___|\__|_|\___/|_| |_|
#           ______
#          |______|


def ios_parse_data_for_deletion(data, running_ios, required_ios, debug=False):
    ''' ios_parse_data_for_deletion

        Args:
            data: contains the output from the used Cisco command
            running_ios: running IOS software image name
            required_ios: required IOS software image name
            debug: passing Boolean to enable/disable debug
    '''
    dp = Verbosity()
    new_list = []

    if debug:
        dp.v_debug("Start of def ios_parse_data_for_deletion()")
    # End of if debug

    if ":" in running_ios:
        running_ios = running_ios.split(":")[-1]
    # End of if ":" in running_ios:

    if "/" in running_ios:
        running_ios = running_ios.split("/")[-1]
    # End of if "/" in running_ios:

    if ":" in required_ios:
        required_ios = required_ios.split(":")[-1]
    # End of if ":" in required_ios:

    if "/" in required_ios:
        required_ios = required_ios.split("/")[-1]
    # End of if "/" in required_ios:

    # Build a dictionary
    kwargs = {}
    kwargs['running_ios'] = running_ios
    kwargs['running_dir'] = re.sub('(.bin)$', '', running_ios)
    kwargs['required_ios'] = required_ios
    kwargs['required_dir'] = re.sub('(.bin)$', '', required_ios)
    kwargs['filter'] = required_ios.split('-')[0]
    kwargs['debug'] = debug

    for item in data:
        # Loop through each member of the stacked device.
        # If the device isn't a stack then we only have 1 element inside the
        # list 'data'.

        if "item" in item and "stdout" in item:
            new_dict = {}
            new_dict['filesystem'] = item['item']

            # Retrieve list of files and directories where the string starts
            # with a part of the required IOS software name but exclude the
            # current running IOS binary file/directory and the required IOS
            # directory.
            new_dict['deletion'] = ios_parse_data_files(
                item['stdout'][0].split('\n'), **kwargs)

            # Build dictionary
            # new_dict =
            #   {
            #       'filesystem' : 'flash:'
            #       'deletion' : [ <filename1>, <directory1> ]
            #   }
            new_list.append(new_dict)

        # End of if "item" in item and "stdout" in item:
    # End of for item in data:

    if debug:
        dp.v_debug("End of def ios_parse_data_for_deletion()")
    # End of if debug

    return new_list


def iosxe_find_required_binary(data, required_bin, debug=False):
    ''' iosxe_find_required_binary
        Build a dictionary of Cisco exisiting upgrade commands that can be
        used.

        Args:
            data: contains the output from exec command '?'
            required_bin: the binary image name that is required to have
            debug: passing Boolean to enable/disable debug
        '''
    dp = Verbosity()
    flag = False  # Initialize default Boolean

    if debug:
        dp.v_debug("Start of def iosxe_find_required_binary()")
    # End of if debug:

    [error, raw_list] = stdout(data, 'iosxe_find_required_binary')

    if not isinstance(required_bin, str):
        dp.error(("(iosxe_find_required_binary) The passed argument "
                  "'required_bin' isn't a string."))
        return flag
    # End of if not isinstance(required_bin, str):

    if error:
        return flag
    # End of if error:

    for line in raw_list:

        line = line.strip()  # Remove leading and trailing spaces
        cond = re.match('^[0-9]+\\s+.*' + re.escape(required_bin) + '$', line)

        if cond:
            flag = True
            if debug:
                dp.v_debug("Found line: " + line)

            # End of if debug:
        # End of if cond:
    # End of for line in raw_list:

    if debug:
        dp.v_debug("End of def iosxe_find_required_binary()")
    # End of if debug:

    return flag


def iosxe_install_cmd_usage(use_command, install_flag, request_flag,
                            software_flag, debug=False):
    ''' iosxe_install_cmd_usage function

        Args:
            use_command: empty string
            install_flag: Boolean object
            request_flag: Boolean object
            software_flag: Boolean object
            debug: passing Boolean to enable/disable debug
    '''
    dp = Verbosity()

    if debug:
        dp.v_debug("Start of def iosxe_install_cmd_usage()")

    cond = (isinstance(install_flag, bool) and isinstance(
        request_flag, bool) and isinstance(software_flag, bool))

    if cond:
        if install_flag:
            use_command = "install"
        elif request_flag:
            use_command = "request"
        elif software_flag:
            use_command = "software"

    # End of if cond:
    if debug:
        dp.v_debug("use_command: " + use_command)
        dp.v_debug("End of def iosxe_install_cmd_usage()")

    return use_command


def iosxe_parse_dir_output(data, version, debug=False):
    ''' iosxe_parse_dir_output

        Args:
            data: contains the output from the used Cisco command
            version: required software version
            debug: passing Boolean to enable/disable debug
    '''
    dp = Verbosity()

    if debug:
        dp.v_debug("Start of def iosxe_parse_dir_output()")
    # End of if debug:

    data_list = []

    if not isinstance(data, list):
        dp.error(("(iosxe_parse_dir_output) The passed argument 'data' isn't"
                  " a list."))
        return False
    elif not isinstance(version, str):
        dp.error(("(iosxe_parse_dir_output) The passed argument 'version' "
                  "isn't a string."))
        return False

    for member in data:

        new_dict = {}
        pkg_list = []
        conf_file = ""

        if not isinstance(member, dict):
            dp.error(("(iosxe_parse_dir_output) The element inside list 'data'"
                      " isn't a dict."))
            return False

        if not ('stdout' in member):
            dp.error(("(iosxe_parse_dir_output) No dict. key 'stdout' found "
                      "inside list element 'data'."))
            return False
        if len(member['stdout']) != 1:
            dp.error(("(iosxe_parse_dir_output) The length of the list behind "
                      "key 'stdout' isn't 1."))
            return False

        lines = member['stdout'][0].split('\n')

        for line in lines:
            line = line.strip()  # Remove leading and trailing spaces

            pkg_cond = re.match(
                '.*(' + re.escape(version) + ').*(.pkg)$', line)
            conf_cond = re.match(
                '.*(' + re.escape(version) + ').*(.conf)$', line)
            filesystem_cond = re.match('^(Directory of)\\s+.*', line)

            if pkg_cond:
                if debug:
                    dp.v_debug("Found pkg line: " + line)
                # End of if debug:
                pkg_list.append(line.split()[-1])
            # End of if pkg_cond:

            if conf_cond:
                if debug:
                    dp.v_debug("Found conf line: " + line)
                # End of if debug:
                conf_file = line.split()[-1]
            # End of if conf_cond:

            if filesystem_cond:
                if debug:
                    dp.v_debug("Found Directory line: " + line)
                fs = line.split()[-1][:-1]
        # for line in lines:

        # Append to list
        new_dict['pkg files'] = pkg_list
        new_dict['pkg count'] = len(pkg_list)
        new_dict['conf file'] = conf_file
        new_dict['filesystem'] = fs

        data_list.append(new_dict)
    # End of for member in data

    if debug:
        dp.v_debug("End of def iosxe_parse_dir_output()")
    # End of if debug:

    return data_list


def iosxe_parse_inactive(data, required_version, debug=False):
    ''' iosxe_parse_inactive

        Args:
            data: contains the output from the used Cisco command
            required_version: required IOS software version number
            debug: passing Boolean to enable/disable debug
    '''
    dp = Verbosity()
    flag = False

    if debug:
        dp.v_debug("Start of def iosxe_parse_inactive()")

    [error, raw_list] = stdout(data, 'iosxe_parse_inactive')

    version_list = required_version.split('.')
    version = [item.lstrip('0') for item in version_list]

    if error:
        return False

    for line in raw_list:
        # Loop through each output line

        line = line.strip()  # Remove leading and trailing spaces
        cond = re.match(
            '^IMG\\s+I\\s+.*' + re.escape('.'.join(version)) + '.*', line)

        if cond:
            if debug:
                dp.v_debug("Found line: " + line)
            flag = True

    if debug:
        dp.v_debug("End of def iosxe_parse_inactive()")

    return flag


# ███╗    ██████╗     ███╗
# ██╔╝    ██╔══██╗    ╚██║
# ██║     ██████╔╝     ██║
# ██║     ██╔═══╝      ██║
# ███╗    ██║         ███║
# ╚══╝    ╚═╝         ╚══╝

#                                  __ _ _       __       _     _
#   _ __   __ _ _ __ ___  ___     / _(_) | ___ / _| ___ | | __| | ___ _ __
#  | '_ \ / _` | '__/ __|/ _ \   | |_| | |/ _ \ |_ / _ \| |/ _` |/ _ \ '__|
#  | |_) | (_| | |  \__ \  __/   |  _| | |  __/  _| (_) | | (_| |  __/ |
#  | .__/ \__,_|_|  |___/\___|___|_| |_|_|\___|_|  \___/|_|\__,_|\___|_|
#  |_|                      |_____|

def parse_filefolder(lines, source, mtype, from_function, debug=False):
    ''' parse_filefolder

        Args:
            data: contains the output from the used Cisco command
            source: name of file or folder
            mtype: file/folder to filter on
            from_function: passing the function name
            debug: passing Boolean to enable/disable debug
    '''
    dp = Verbosity()

    result = None
    s = re.escape(source)
    p = re.escape(mtype)

    for line in lines:
        line = line.strip()  # Remove leading and trailing spaces

        cond = re.match('^[0-9]+\\s+' + p + '.*' + s + '$', line)

        if cond:
            if debug:
                dp.v_debug("(" + from_function + ") Found line: " + line)
            # End of if debug

            result = line.split()[-1]
        # End of if cond

        cond2 = re.match('^(No files in directory)$', line)

        if cond2:
            if debug:
                message = "(" + from_function + ") Found line: 'No files " + \
                    "in directory'"
                dp.v_debug(message)
            # End of if debug

            result = None
        # End of if cond2:
    # End of for line in lines:

    if debug:
        message = "(" + from_function + ") " + str(type(result))
        message += " result = " + str(result)
        dp.v_debug(message)
    # End of if debug

    return result


#                                  __ _ _                     _
#  _ __   __ _ _ __ ___  ___     / _(_) | ___  ___ _   _ ___| |_ ___ _ __ ___
# | '_ \ / _` | '__/ __|/ _ \   | |_| | |/ _ \/ __| | | / __| __/ _ \ '_ ` _ \
# | |_) | (_| | |  \__ \  __/   |  _| | |  __/\__ \ |_| \__ \ ||  __/ | | | | |
# | .__/_\__,_|_|  |___/\___|___|_| |_|_|\___||___/\__, |___/\__\___|_| |_| |_|
# |_|  | (_)___| |_        |_____|                 |___/
#      | | / __| __|
#      | | \__ \ |_
#  ____|_|_|___/\__|
# |_____|

def parse_filesystem_list(data, debug=False):
    ''' parse_filesystem_list

        Args:
            data: contains the output from the used Cisco command
            debug: passing Boolean to enable/disable debug
    '''
    dp = Verbosity()
    data_dict = {}

    if debug:
        dp.v_debug("Start of def parse_filesystem_list()")
    # End of if debug:

    if not isinstance(data, list):
        dp.error(("(parse_filesystem_list) Passed argument 'data' isn't a "
                  "list."))
        return data_dict
    # End of if not isinstance(data, list):

    for item in data:
        keylabel = None
        valuelabel = None

        if "item" in item:
            keylabel = item['item']
        # End of if "item" in item:

        if "stdout" in item:
            lines = item['stdout'][0].split('\n')
            valuelabel = parse_filesystem_space(lines, debug)
        # End of if "stdout" in item:

        if keylabel is not None and valuelabel is not None:
            data_dict[keylabel] = valuelabel
        # End of if keylabel is not None and valuelabel is not None:

    if debug:
        dp.v_debug("End of def parse_filesystem_list()")
    # End of if debug:

    return data_dict


#                                 __ _ _                     _
#  _ __   __ _ _ __ ___  ___     / _(_) | ___  ___ _   _ ___| |_ ___ _ __ ___
# | '_ \ / _` | '__/ __|/ _ \   | |_| | |/ _ \/ __| | | / __| __/ _ \ '_ ` _ \
# | |_) | (_| | |  \__ \  __/   |  _| | |  __/\__ \ |_| \__ \ ||  __/ | | | | |
# | .__/ \__,_|_|  |___/\___|___|_| |_|_|\___||___/\__, |___/\__\___|_| |_| |_|
# |_|   ___ _ __   __ _  __|_____|                 |___/
#      / __| '_ \ / _` |/ __/ _ \
#      \__ \ |_) | (_| | (_|  __/
#  ____|___/ .__/ \__,_|\___\___|
# |_____|  |_|

def parse_filesystem_space(lines, debug=False):
    ''' parse_filesystem_space

        Args:
            data: contains the output from the used Cisco command
            debug: passing Boolean to enable/disable debug
    '''
    dp = Verbosity()
    data_dict = {}

    for line in lines:
        line = line.strip()  # Remove leading and trailing spaces

        cond1 = re.match(
            '^[0-9]*\\s(bytes available).*', line)

        cond2 = re.match(
            '^[0-9]*\\s(bytes total).*', line)

        if cond1:
            if debug:
                dp.v_debug("Found line: " + line)
            # End of if debug:

            free_kb = round(
                int(re.sub('\\s+(bytes available)\\s+.*', '', line)) / 1000)
            used_kb = round(int(
                re.sub('.*\\(([0-9]+?)\\s(bytes used)\\)', '\\1', line)
            ) / 1000)

            data_dict['total_kb'] = free_kb + used_kb
            data_dict['free_kb'] = int(free_kb)
        # End of if cond1:

        elif cond2:
            if debug:
                dp.v_debug("Found line: " + line)
            # End of if debug:

            total_kb = round(
                int(re.sub('\\s+(bytes total)\\s+.*', '', line)) / 1000)
            free_kb = round(
                int(
                    re.sub('.*\\(([0-9]+?)\\s(bytes free).*\\)', '\\1', line)
                ) / 1000)

            data_dict['total_kb'] = int(total_kb)
            data_dict['free_kb'] = int(free_kb)
        # End of elif cond2:

    # End of for line in lines:

    return data_dict


#                                     _
#   _ __   __ _ _ __ ___  ___     ___| |__   _____      __
#  | '_ \ / _` | '__/ __|/ _ \   / __| '_ \ / _ \ \ /\ / /
#  | |_) | (_| | |  \__ \  __/   \__ \ | | | (_) \ V  V /
#  | .__/ \__,_|_|  |___/\___|___|___/_| |_|\___/ \_/\_/
#  |_|                _ _   |_____|
#        _____      _(_) |_ ___| |__
#       / __\ \ /\ / / | __/ __| '_ \
#       \__ \\ V  V /| | || (__| | | |
#   ____|___/ \_/\_/ |_|\__\___|_| |_|
#  |_____|

def parse_show_switch(data, debug=False):
    ''' parse_show_switch

        Args:
            data: contains the output from the used Cisco command
            debug: passing Boolean to enable/disable debug
    '''
    dp = Verbosity()

    if debug:
        dp.v_debug("Start of def parse_show_switch()")
    # End of if debug:

    show_switch = []
    [error, raw_list] = stdout(data, 'parse_show_switch')

    if error:
        return show_switch

    for line in raw_list:
        # Loop through each output line

        new_dict = {}

        line = line.strip()  # Remove leading and trailing spaces

        # Build condition to match line
        cond1 = re.match('^Switch#\\s+Role\\s+Mac\\sAddress\\s.*', line)

        # Build condition to match line
        cond2 = re.match(
            '^[\\*|\\d][\\d|\\s]\\s+(Master|Member|Active|Standby).*', line)

        if cond1:
            if debug:
                dp.v_debug("(parse_show_switch) Found line: " + line)
            # End of if debug:
        # End of if cond1:

        if cond2:
            if debug:
                dp.v_debug("(parse_show_switch) Found line: " + line)
            # End of if debug:

            # Replace any whitespace character (one and unlimited)
            # times with 1 whitespace character.
            replaced_line = re.sub('\\s+', ' ', line)

            replaced_line = replaced_line.replace('*', '')
            stripped_line = replaced_line.strip()
            line_list = stripped_line.split()

            new_dict['Switch'] = int(line_list[0].strip())
            new_dict['Role'] = line_list[1].strip()
            new_dict['Mac Address'] = line_list[2].strip()
            new_dict['Priority'] = int(line_list[3].strip())
            new_dict['H/W Version'] = int(line_list[4].strip())
            new_dict['Current State'] = line_list[5].strip()

            show_switch.append(new_dict)
        # End of if cond2:
    # End of for line in raw_list:

    if debug:
        message = "(parse_show_switch) " + \
            str(type(show_switch)) + " show_switch = "
        dp.v_debug(message)
        pprint(show_switch)
        dp.v_debug("End of def parse_show_switch()")
    # End of if debug:

    return show_switch


#                                     _
#   _ __   __ _ _ __ ___  ___     ___| |__   _____      __
#  | '_ \ / _` | '__/ __|/ _ \   / __| '_ \ / _ \ \ /\ / /
#  | |_) | (_| | |  \__ \  __/   \__ \ | | | (_) \ V  V /
#  | .__/ \__,_|_|  |___/\___|___|___/_| |_|\___/ \_/\_/
#  |_|__   _____ _ __ ___(_)|_____| __
#     \ \ / / _ \ '__/ __| |/ _ \| '_ \
#      \ V /  __/ |  \__ \ | (_) | | | |
#   ____\_/ \___|_|  |___/_|\___/|_| |_|
#  |_____|

def parse_show_version(data, debug=False):
    ''' parse_show_version
        Matches the characters from keyword value at the start of each
        newline.

        Args:
            data: contains the output from the used Cisco command
            debug: passing Boolean to enable/disable debug
    '''
    error = False

    dp = Verbosity()

    if debug:
        dp.v_debug("Start of def parse_show_version()")
    # End of if debug:

    device_type = "router"  # Initialize by default as 'router'
    show_version = []

    [error, raw_list] = stdout(data, 'parse_show_version', debug)

    if error:
        return show_version
    # End of if error:

    # Detect if it is a Switch or Router
    for line in raw_list:
        # Loop through each output line

        line = line.strip()  # Remove leading and trailing spaces

        # Build condition to match line
        cond = re.match('^Switch\\sPorts\\sModel\\s.*', line)

        if cond:
            if debug:
                dp.v_debug(line)
            # End of if debug:

            device_type = "switch"
        # End of if cond:
    # End of for line in raw_list:

    # Device type is detected as switch
    if device_type == "switch":
        if debug:
            message = "(parse_show_version) Variable device_type is set with "
            message += " value '" + device_type + "'"
            dp.v_debug(message)
        # End of if debug:

        for line in raw_list:
            # Loop through each line

            line = line.strip()  # Remove leading and trailing spaces

            # Build condition to match line
            cond = re.match('^[\\*|\\d]\\s+[0-9]+\\s+.*', line)

            if cond:
                if debug:
                    dp.v_debug(line)
                # End of if debug:

                new_dict = {}

                # Replace any whitespace character (one and unlimited)
                # times with 1 whitespace character.
                replaced_line = re.sub('\\s+', ' ', line)

                replaced_line = replaced_line.replace('*', '')
                stripped_line = replaced_line.strip()

                line_list = stripped_line.split()

                new_dict['Switch'] = int(line_list[0].strip())
                new_dict['Ports'] = int(line_list[1].strip())
                new_dict['Model'] = line_list[2].strip()
                new_dict['SW Version'] = line_list[3].strip()
                new_dict['SW Image'] = line_list[4].strip()

                if len(line_list) == 6:
                    new_dict['Mode'] = line_list[5].strip()
                # End of if len(line_list) == 6:

                show_version.append(new_dict)
            # End of if cond:
        # End of for line in raw_list:
    # End of if device_type == "switch":

    elif device_type == "router":
        if debug:
            message = "(parse_show_version) Variable device_type is set with "
            message += " value '" + device_type + "'"
            dp.v_debug(message)
        # End of if debug:
    # End of elif device_type == "router":

    else:
        if debug:
            message = "(parse_show_version) Variable device_type is set with "
            message += " value '" + device_type + "'"
            dp.v_debug(message)
        # End of if debug:
    # End of else device_type == "router":

    if debug:
        message = "(parse_show_version) " + \
            str(type(show_version)) + " show_version = "
        dp.v_debug(message)
        pprint(show_version)
        dp.v_debug("End of def parse_show_version()")
    # End of if debug:

    return show_version


# ███╗    ███████╗    ███╗
# ██╔╝    ██╔════╝    ╚██║
# ██║     ███████╗     ██║
# ██║     ╚════██║     ██║
# ███╗    ███████║    ███║
# ╚══╝    ╚══════╝    ╚══╝

def stdout(data, from_method, debug=False):
    ''' stdout
        Determine if the passed variable 'data' is a list or string.

        Args:
            data: command output result
            from_method: method name
            debug: passing Boolean to enable/disable debug
    '''

    dp = Verbosity()

    error = False  # Initialize the default error flag with a Boolean
    raw_list = []  # Initialize an empty list

    if isinstance(data, str):
        # The variable 'data' is a string

        if debug:
            message = "(" + from_method + ") The argument 'data' is a string."
            dp.v_debug(message)
        # End of if debug:

        # Split a string into a list using newline as separator
        raw_list = data.split("\n")

    else:
        message = "(" + from_method + ") The passed argument 'data' is "
        message += "not a list nor string."
        dp.v_error(message)
        error = True
    # End of if isinstance(data, list):

    return [error, raw_list]


class FilterModule(object):
    def filters(self):
        return {
            'filter_model': filter_model,
            'find_commands': find_commands,
            'find_filesystems': find_filesystems,
            'ios_findfile': ios_findfile,
            'ios_findfolder': ios_findfolder,
            'ios_parse_data_for_deletion': ios_parse_data_for_deletion,
            'parse_filesystem_list': parse_filesystem_list,
            'parse_show_switch': parse_show_switch,
            'parse_show_version': parse_show_version,
        }


# ██╗   ██╗███████╗██████╗ ██████╗  ██████╗ ███████╗██╗████████╗██╗   ██╗
# ██║   ██║██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║╚══██╔══╝╚██╗ ██╔╝
# ██║   ██║█████╗  ██████╔╝██████╔╝██║   ██║███████╗██║   ██║    ╚████╔╝
# ╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══██╗██║   ██║╚════██║██║   ██║     ╚██╔╝
#  ╚████╔╝ ███████╗██║  ██║██████╔╝╚██████╔╝███████║██║   ██║      ██║
#   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝╚═╝   ╚═╝      ╚═╝

class Verbosity:
    ''' class Verbosity
        Provide a colorfull output to make it better visible '''

    # Private variables
    __red = '\033[31m'
    __green = '\033[32m'
    __orange = '\033[33m'
    __blue = '\033[34m'
    __purple = '\033[35m'
    __cyan = '\033[36m'
    __lightgrey = '\033[37m'
    __darkgrey = '\033[90m'
    __lightred = '\033[91m'
    __lightgreen = '\033[92m'
    __yellow = '\033[93m'
    __lightblue = '\033[94m'
    __pink = '\033[95m'
    __lightcyan = '\033[96m'
    __reset = '\033[0m'

    def __init__(self, **args):
        ''' Constructor
            Is a reserved method in Python classes.
            This method called when an object is created from the class and
            it allow the class to initialize the attributes of a class '''

        self.message = None
        self.error = False
        super(Verbosity, self).__init__()
    ''' End of def __init__(self, **args): '''

    def v_debug(self, message):
        ''' Display an error message '''
        print(self.__purple + '[DEBUG] ' + self.__reset + message)

    def v_error(self, message):
        ''' Display an error message '''
        print(self.__red + '[ERROR] ' + self.__reset + message)
