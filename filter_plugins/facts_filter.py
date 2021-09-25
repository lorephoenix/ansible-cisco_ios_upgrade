<<<<<<< HEAD
#!/usr/bin/env python

import inspect
import re
from pprint import pprint

# require pip install --upgrade pandas
import pandas as pd

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


# ███████╗██╗██╗  ████████╗███████╗██████╗
# ██╔════╝██║██║  ╚══██╔══╝██╔════╝██╔══██╗
# █████╗  ██║██║     ██║   █████╗  ██████╔╝
# ██╔══╝  ██║██║     ██║   ██╔══╝  ██╔══██╗
# ██║     ██║███████╗██║   ███████╗██║  ██║
# ╚═╝     ╚═╝╚══════╝╚═╝   ╚══════╝╚═╝  ╚═╝
#     ███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗██╗     ███████╗
#     ████╗ ████║██╔═══██╗██╔══██╗██║   ██║██║     ██╔════╝
#     ██╔████╔██║██║   ██║██║  ██║██║   ██║██║     █████╗
#     ██║╚██╔╝██║██║   ██║██║  ██║██║   ██║██║     ██╔══╝
#     ██║ ╚═╝ ██║╚██████╔╝██████╔╝╚██████╔╝███████╗███████╗
#     ╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝

class FilterModule(object):

    def __init__(self):
        self.dp = Verbosity()
        self.debug = False
        self.error = False

    def filters(self):
        return {
            'filter_model': self.filter_model,
            'find_commands': self.find_commands,
            'find_image_file': self.find_image_file,
            'find_image_folder': self.find_image_folder,
            'parse_data_for_deletion': self.parse_data_for_deletion,
            'parse_filesystem_list': self.parse_filesystem_list,
            'parse_show_switch': self.parse_show_switch,
            'parse_show_version': self.parse_show_version,
        }

    # -------------------------------------------------------------------------
    #   ___ _   _ ___ _    ___ ___   __  __ ___ _____ _  _  ___  ___  ___
    # | _ \ | | | _ ) |  |_ _/ __| |  \/  | __|_   _| || |/ _ \|   \/ __|
    # |  _/ |_| | _ \ |__ | | (__  | |\/| | _|  | | | __ | (_) | |) \__ \
    # |_|  \___/|___/____|___\___| |_|  |_|___| |_| |_||_|\___/|___/|___/
    #
    # -------------------------------------------------------------------------

    def filter_model(self, model_arg, debug=False):
        ''' filter_model
            Matches the characters from keyword value at the start of each
            newline.

            Args:
                model: Cisco model
                debug: passing Boolean to enable/disable debug
        '''
        model = ""
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
        # End of if self.debug:

        if isinstance(model_arg, str):
            # The passed argument is a string

            if self.debug:
                message = "(" + self.__who_am_i() + ") The argument " + \
                    "model_arg is a string."
                self.dp.v_debug(message)
            # End of if self.debug:

            # Split a string into a list using character minus (-) as separator
            # but only keep the first 2 elements of the list.
            stripped_model = model_arg.split('-')[0:2]

            if stripped_model[0].upper() == 'WS':
                # The first element has the string 'WS', which stands for
                # Workgroup Switch.

                if self.debug:
                    message = "(" + self.__who_am_i() + ") Detected that " + \
                        "the string starts with the string 'WS'"
                    self.dp.v_debug(message)
                # End of if self.debug:
                model = '-'.join(stripped_model)
            # End of if stripped_model[0].upper() == 'WS':

            else:
                # The first element doesn't have the string 'WS'.
                # Most routers will start with the string CISCO or ISR but most
                # likely have the character slash '/'.

                if self.debug:
                    message = "(" + self.__who_am_i() + ") Detected that " + \
                        "the string doesn't start with string 'WS'"
                    self.dp.v_debug(message)
                # End of if self.debug:

                # Split string into a list using the character slash '/' as
                # separator and return with the first element of the list.
                model = stripped_model[0].split('/')[0]
            # End of else:
        # End of if isinstance(model_arg, str):

        else:
            # The passed argument is NOT a string
            message = "(" + self.__who_am_i() + ") The passed model " + \
                "argument isn't a string."
            self.dp.v_error(message)
            return model
        # End of else:

        if self.debug:
            message = "(" + self.__who_am_i() + ") model = '" + model + "'"
            self.dp.v_debug(message)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return model.upper()
    ''' End of def filter_model(self,model_arg, debug=False): '''

    def find_commands(self, data, command, debug=False):
        ''' find_commands
            Build a dictionary of Cisco exisiting upgrade commands that can be
            used.

            Args:
                data: contains the output from exec command '?'
                command: command string
                debug: passing Boolean to enable/disable debug
            '''
        flag = False
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
        # End of if self.debug:

        raw_list = self.__stdout(data, 'find_commands')

        if self.error:
            return False
        # End of if error:

        if not isinstance(command, str):
            message = "(" + self.__who_am_i() + \
                ") The passed command isn't a string."
            self.dp.error(message)
            return False
        # End of if not isinstance(command, str):

        # Split string into a list.
        command_list = command.split()

        if len(command_list) == 0:
            message = "(" + self.__who_am_i() + \
                ") The passed command is empty."
            self.dp.error(message)
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
                if self.debug:
                    message = "(" + self.__who_am_i() + ") Found line: " + \
                        line
                    self.dp.v_debug(message)
                # End of if self.debug:

                flag = True
            # End of if cond:
        # End of for line in raw_list:

        if self.debug:
            message = "(" + self.__who_am_i() + ") flag = " + \
                str(flag) + " <" + str(type(flag))
            message += ">"
            self.dp.v_debug(message)
            self.dp.v_debug("<<< End of def " + self.__who_am_i())
        # End of if self.debug:

        return flag
    ''' End of def find_commands(self, data, command, debug=False): '''

    def find_image_file(self, data, alist, binfile, debug=False):
        ''' find_image_file

            Args:
                data: contains the output from the running IOS command
                alist: passing list to append data into it
                binfile: passing string with name of binary file
                debug: passing Boolean to enable/disable debug
        '''
        data_list = []
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'data' is a " + str(type(data))
            self.dp.v_debug(message)
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'alist' is a " + str(type(alist))
            self.dp.v_debug(message)
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'binfile' is a " + str(type(binfile))
            self.dp.v_debug(message)
        # End of if self.debug:

        cond = (not isinstance(data, list) or not isinstance(
            alist, list) or not isinstance(binfile, str))

        if cond:
            message = "(" + self.__who_am_i() + ") One or both passed " + \
                "arguments wasn't able to pass the condition. " + \
                "'data' = <<list>>, 'folder' = <<string>>"
            self.dp.v_error(message)
            return data_list
        # End of if cond:

        for item in data:
            new_dict = {'filesystem': None, 'filename': None}

            if "item" in item:
                key = "item"
                label = "filesystem"
                new_dict['filesystem'] = self.__parse_find_file(
                    item, key, label)

                if "stdout" in item:
                    key = "stdout"
                    label = None

                    if self.debug:
                        message = "(" + self.__who_am_i() + ") Found " + \
                            "dictionary key 'stdout'."
                        self.dp.v_debug(message)

                    lines = self.__parse_find_file(item, key, label)

                    new_dict['filename'] = self.__parse_filefolder(
                        lines, binfile, '-rw', self.__who_am_i())
            # End of if "item" in item:

            data_list.append(new_dict)
        # End of for item in data:

        df1 = pd.DataFrame(alist).set_index('filesystem')
        df2 = pd.DataFrame(data_list).set_index('filesystem')
        df = df1.merge(df2, left_index=True, right_index=True)
        data_list = df.T.to_dict()

        if self.debug:
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return data_list
    ''' End of def find_image_file(data, alist, binfile, debug=False): '''

    def find_image_folder(self, data, folder, debug=False):
        ''' find_image_folder

            Args:
                data: contains the output from the running IOS command
                source: passing string with name of folder
                debug: passing Boolean to enable/disable debug
            '''
        data_list = []
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'data' is a " + str(type(data))
            self.dp.v_debug(message)
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'folder' is a " + str(type(folder))
            self.dp.v_debug(message)
        # End of if self.debug :

        for item in data:
            new_dict = {}
            new_dict['filesystem'] = ""
            new_dict['directory'] = ""

            if "item" in item:
                new_dict['filesystem'] = item['item']  # Set name of filesystem

                if "stdout" in item:
                    lines = item['stdout'][0].split('\n')

                    new_dict['directory'] = self.__parse_filefolder(
                        lines, folder, 'drw', 'find_image_folder')
                # End of if "stdout" in item:
            # End of if "item" in item:
            data_list.append(new_dict)
        # End of for item in data:

        if self.debug:
            message = "(" + self.__who_am_i() + ") " + str(type(data_list))
            message += " data_list = "
            self.dp.v_debug(message)
            pprint(data_list)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug :

        return data_list
    ''' End of def find_image_folder(data, folder, debug=False): '''

    def parse_filesystem_list(self, data, debug=False):
        ''' parse_filesystem_list

            Args:
                data: contains the output from the used Cisco command
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug
        data_dict = {}

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
        # End of if self.debug:

        if not isinstance(data, list):
            message = "(" + self.__who_am_i() + ") Passed argument 'data' " + \
                "isn't a list."
            self.dp.v_error(message)
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
                valuelabel = self.__parse_filesystem_space(lines)
            # End of if "stdout" in item:

            if keylabel is not None and valuelabel is not None:
                data_dict[keylabel] = valuelabel
            # End of if keylabel is not None and valuelabel is not None:

        if self.debug:
            self.dp.v_debug("(" + self.__who_am_i() + ") data_dict = ")
            pprint(data_dict)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return data_dict
    ''' End of def parse_filesystem_list(data, debug=False): '''

    def parse_data_for_deletion(self, data, running_ios, required_ios,
                                debug=False):
        ''' ios_parse_data_for_deletion

            Args:
                data: contains the output from the used Cisco command
                running_ios: running IOS software image name
                required_ios: required IOS software image name
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug
        new_list = []

        if self.debug:
            self.dp.v_debug("Start of " + self.__who_am_i())
        # End of if self.debug

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

        for item in data:
            # Loop through each member of the stacked device.
            # If the device isn't a stack then we only have 1 element inside
            # the list 'data'.

            if "item" in item and "stdout" in item:
                new_dict = {}
                new_dict['filesystem'] = item['item']

                # Retrieve list of files and directories where the string
                # starts with a part of the required IOS software name but
                # exclude the current running IOS binary file/directory and the
                # required IOS directory.
                new_dict['deletion'] = self.__parse_data_files(
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

        if self.debug:
            self.dp.v_debug("End of " + self.__who_am_i())
        # End of if self.debug

        return new_list
    ''' End of def parse_data_for_deletion(self, data, running_ios,
            required_ios, debug=False): '''

    def parse_show_switch(self, data, debug=False):
        ''' parse_show_switch

            Args:
                data: contains the output from the used Cisco command
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
        # End of if self.debug:

        show_switch = []
        raw_list = self.__stdout(data, self.__who_am_i())

        if self.error:
            return show_switch

        for line in raw_list:
            # Loop through each output line

            new_dict = {}

            line = line.strip()  # Remove leading and trailing spaces

            # Build condition to match line
            cond1 = re.match('^Switch#\\s+Role\\s+Mac\\sAddress\\s.*', line)

            # Build condition to match line
            cond2 = re.match(
                '^[\\*|\\d][\\d|\\s]\\s+(Master|Member|Active|Standby).*',
                line)

            if cond1:
                if self.debug:
                    self.dp.v_debug(
                        "(" + self.__who_am_i() + ") Found line: " + line)
                # End of if self.debug:
            # End of if cond1:

            if cond2:
                if self.debug:
                    self.dp.v_debug(
                        "(" + self.__who_am_i() + ") Found line: " + line)
                # End of if self.debug:

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

        if self.debug:
            message = "(" + self.__who_am_i() + ")" + \
                str(type(show_switch)) + " show_switch = "
            self.dp.v_debug(message)
            pprint(show_switch)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return show_switch
    ''' End of def parse_show_switch(data, debug=False): '''

    def parse_show_version(self, data, debug=False):
        ''' parse_show_version
            Matches the characters from keyword value at the start of each
            newline.

            Args:
                data: contains the output from the used Cisco command
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
        # End of if self.debug:

        device_type = "router"  # Initialize by default as 'router'
        show_version = []

        raw_list = self.__stdout(data, 'parse_show_version')

        if self.error:
            return show_version
        # End of if error:

        # Detect if it is a Switch or Router
        for line in raw_list:
            # Loop through each output line

            line = line.strip()  # Remove leading and trailing spaces

            # Build condition to match line
            cond = re.match('^Switch\\sPorts\\sModel\\s.*', line)

            if cond:
                if self.debug:
                    self.dp.v_debug(line)
                # End of if self.debug:

                device_type = "switch"
            # End of if cond:
        # End of for line in raw_list:

        # Device type is detected as switch
        if device_type == "switch":
            if self.debug:
                message = "(" + self.__who_am_i() + ") Variable " + \
                    "device_type is set with value '" + device_type + "'"
                self.dp.v_debug(message)
            # End of if self.debug:

            for line in raw_list:
                # Loop through each line

                line = line.strip()  # Remove leading and trailing spaces

                # Build condition to match line
                cond = re.match('^[\\*|\\d]\\s+[0-9]+\\s+.*', line)

                if cond:
                    if self.debug:
                        self.dp.v_debug(line)
                    # End of if self.debug:

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
            if self.debug:
                message = "(" + self.__who_am_i() + ") Variable " + \
                    "device_type is set with value '" + device_type + "'"
                self.dp.v_debug(message)
            # End of if self.debug:
        # End of elif device_type == "router":

        else:
            if self.debug:
                message = "(" + self.__who_am_i() + ") Variable " + \
                    "device_type is set with value '" + device_type + "'"
                self.dp.v_debug(message)
            # End of if self.debug:
        # End of else device_type == "router":

        if self.debug:
            message = "(" + self.__who_am_i() + ") " + \
                str(type(show_version)) + " show_version = "
            self.dp.v_debug(message)
            pprint(show_version)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return show_version
    ''' End of def parse_show_version(self, data, debug=False): '''

    # -------------------------------------------------------------------------
    #  ___ ___ _____   ___ _____ ___   __  __ ___ _____ _  _  ___  ___  ___
    # | _ \ _ \_ _\ \ / /_\_   _| __| |  \/  | __|_   _| || |/ _ \|   \/ __|
    # |  _/   /| | \ V / _ \| | | _|  | |\/| | _|  | | | __ | (_) | |) \__ \
    # |_| |_|_\___| \_/_/ \_\_| |___| |_|  |_|___| |_| |_||_|\___/|___/|___/
    #
    # -------------------------------------------------------------------------

    def __parse_data_files(self, lines, **kwargs):
        ''' __ios_parse_data_files

            Args:
                lines: contains the output of the dir of that specific
                kwargs: passing keyword ( or named) arguments
        '''

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())

        new_list = []

        runfile = re.escape(kwargs['running_ios'])
        rundir = re.escape(kwargs['running_dir'])
        reqdir = re.escape(kwargs['required_dir'])
        f = re.escape(kwargs['filter'])

        for line in lines:
            line = line.strip()  # Remove leading and trailing spaces

            # Build conditional to ignore the running IOS binary file,
            # if exist.
            cond1 = re.match('^[0-9]+\\s+(-rw).*\\s+(' + runfile + ')$', line)

            # Build conditional to ignore the directories that contains the
            # name of the running IOS and required IOS, if exist.
            cond2 = re.match(
                '^[0-9]+\\s+(drw).*\\s+(' + rundir + '|' + reqdir + ')$', line)

            # Build conditional to keep files and directories that contains the
            # model variant name that is extracted from the required IOS.
            cond3 = re.match('^[0-9]+\\s+.*\\s+(' + f + ').*$', line)

            if (not (cond1 or cond2)) and cond3:
                if self.debug:
                    self.dp.v_debug("Found line: " + line)
                # End of if self.debug:

                new_list.append(line.split()[-1])

            # End of if (not (cond1 and cond2)) and cond3:
        # End of for line in lines:

        if self.debug:
            self.dp.v_debug("<<< End of " + self.__who_am_i())

        return new_list
    ''' End of def __parse_data_files(lines, **kwargs): '''

    def __parse_filefolder(self, lines, source, mtype, from_function):
        ''' __parse_filefolder

            Args:
                data: contains the output from the used Cisco command
                source: name of file or folder
                mtype: file/folder to filter on
                from_function: passing the function name

        '''
        result = None
        s = re.escape(source)
        p = re.escape(mtype)

        for line in lines:
            line = line.strip()  # Remove leading and trailing spaces

            cond = re.match('^[0-9]+\\s+' + p + '.*' + s + '$', line)

            if cond:
                if self.debug:
                    self.dp.v_debug(
                        "(" + from_function + ") Found line: " + line)
                # End of if self.debug

                result = line.split()[-1]
            # End of if cond

            cond2 = re.match('^(No files in directory)$', line)

            if cond2:
                if self.debug:
                    message = "(" + from_function + ") Found line: " + \
                        "'No files in directory'"
                    self.dp.v_debug(message)
                # End of if self.debug

                result = None
            # End of if cond2:
        # End of for line in lines:

        if self.debug:
            message = "(" + from_function + ") " + str(type(result))
            message += " result = " + str(result)
            self.dp.v_debug(message)
        # End of if self.debug

        return result
    ''' End of def __parse_filefolder(lines, source, mtype, from_function): '''

    def __parse_filesystem_space(self, lines):
        ''' __parse_filesystem_space

            Args:
                data: contains the output from the used Cisco command
        '''
        data_dict = {}

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())

        for line in lines:
            line = line.strip()  # Remove leading and trailing spaces

            cond1 = re.match(
                '^[0-9]*\\s(bytes available).*', line)

            cond2 = re.match(
                '^[0-9]*\\s(bytes total).*', line)

            if cond1:
                if self.debug:
                    message = "(" + self.__who_am_i() + ") Found line: " + line
                    self.dp.v_debug(message)
                # End of if self.debug:

                free_kb = round(
                    int(
                        re.sub(
                            '\\s+(bytes available)\\s+.*', '', line)) / 1000)
                used_kb = round(int(
                    re.sub('.*\\(([0-9]+?)\\s(bytes used)\\)', '\\1', line)
                ) / 1000)

                data_dict['total_kb'] = free_kb + used_kb
                data_dict['free_kb'] = int(free_kb)
            # End of if cond1:

            elif cond2:
                if self.debug:
                    message = "(" + self.__who_am_i() + ") Found line: " + line
                    self.dp.v_debug(message)
                # End of if self.debug:

                total_kb = round(
                    int(re.sub('\\s+(bytes total)\\s+.*', '', line)) / 1000)
                free_kb = round(
                    int(
                        re.sub(
                            '.*\\(([0-9]+?)\\s(bytes free).*\\)', '\\1', line)
                    ) / 1000)

                data_dict['total_kb'] = int(total_kb)
                data_dict['free_kb'] = int(free_kb)
            # End of elif cond2:
        # End of for line in lines:

        if self.debug:
            self.dp.v_debug("(" + self.__who_am_i() + ") data_dict = ")
            pprint(data_dict)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        return data_dict
    ''' End of  def __parse_filesystem_space(self, lines): '''

    def __parse_find_file(self, item_object, key, label=None):
        '''  __parse_find_file

            Args:
            item_object: passing object
                key: passing key name
                label: passing label to find
        '''
        rvalue = None

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())

        if isinstance(item_object[key], dict):
            if self.debug:
                message = "(" + self.__who_am_i() + ") The variable item[" + \
                    key + "] is a dictionary."
                self.dp.v_debug(message)
            # End of if self.debug:

            if label in item_object[key]:
                rvalue = item_object[key][label]

                if self.debug:
                    message = "(" + self.__who_am_i() + \
                        ") The dictionary item[" + key
                    message += "] contains the key '" + label + "'."
                    self.dp.v_debug(message)
                    self.dp.v_debug(("(" + self.__who_am_i() + ") "
                                     "" + label + " = " + rvalue))
                # End of if self.debug:
            # End of if label in item_object[key]:
        # End of if isinstance(item_object[key], dict):

        elif isinstance(item_object[key], list):
            if self.debug:
                message = "(" + self.__who_am_i() + ") The variable item['" + \
                    key + "'] is a list."
                self.dp.v_debug(message)
            # End of if self.debug:
            rvalue = item_object[key][0].split('\n')

        elif isinstance(item_object[key], str):
            if self.debug:
                message = "(" + self.__who_am_i() + ") The variable item['" + \
                    key + "'] is a string."
                self.dp.v_debug(message)
            # End of if self.debug:

            rvalue = item_object[key]
        # End of elif isinstance(item_object[key], str):

        if self.debug:
            self.dp.v_debug("<< < End of " + self.__who_am_i())
        return rvalue
    ''' End of def __parse_find_file(item_object, key, label=None)'''

    # ███╗    ███████╗    ███╗
    # ██╔╝    ██╔════╝    ╚██║
    # ██║     ███████╗     ██║
    # ██║     ╚════██║     ██║
    # ███╗    ███████║    ███║
    # ╚══╝    ╚══════╝    ╚══╝

    def __stdout(self, data, from_method):
        ''' __stdout
            Determine if the passed variable 'data' is a list or string.

            Args:
                data: command output result
                from_method: method name
        '''
        raw_list = []  # Initialize an empty list

        if isinstance(data, str):
            # The variable 'data' is a string

            if self.debug:
                message = "(" + from_method + \
                    ") The argument 'data' is a string."
                self.dp.v_debug(message)
            # End of if self.debug:

            # Split a string into a list using newline as separator
            raw_list = data.split("\n")

        else:
            message = "(" + from_method + ") The passed argument 'data' is "
            message += "not a list nor string."
            self.dp.v_error(message)
            self.error = True
        # End of if isinstance(data, list):

        return raw_list
    ''' End of def __stdout(data, from_method): '''

    def __who_am_i(self):
        return inspect.stack()[1][3]
=======
#!/usr/bin/env python

import inspect
import re
from pprint import pprint

# require pip install --upgrade pandas
import pandas as pd

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


# ███████╗██╗██╗  ████████╗███████╗██████╗
# ██╔════╝██║██║  ╚══██╔══╝██╔════╝██╔══██╗
# █████╗  ██║██║     ██║   █████╗  ██████╔╝
# ██╔══╝  ██║██║     ██║   ██╔══╝  ██╔══██╗
# ██║     ██║███████╗██║   ███████╗██║  ██║
# ╚═╝     ╚═╝╚══════╝╚═╝   ╚══════╝╚═╝  ╚═╝
#     ███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗██╗     ███████╗
#     ████╗ ████║██╔═══██╗██╔══██╗██║   ██║██║     ██╔════╝
#     ██╔████╔██║██║   ██║██║  ██║██║   ██║██║     █████╗
#     ██║╚██╔╝██║██║   ██║██║  ██║██║   ██║██║     ██╔══╝
#     ██║ ╚═╝ ██║╚██████╔╝██████╔╝╚██████╔╝███████╗███████╗
#     ╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝

class FilterModule(object):

    def __init__(self):
        self.dp = Verbosity()
        self.debug = False
        self.error = False

    def filters(self):
        return {
            'filter_model': self.filter_model,
            'find_commands': self.find_commands,
            'find_image_file': self.find_image_file,
            'find_image_folder': self.find_image_folder,
            'iosxe_find_conf_file': self. iosxe_find_conf_file,
            'iosxe_find_image_file': self.iosxe_find_image_file,
            'iosxe_get_build_version': self.iosxe_get_build_version,
            'iosxe_install_cmd_usage': self.iosxe_install_cmd_usage,
            'iosxe_parse_inactive': self.iosxe_parse_inactive,
            'parse_data_for_deletion': self.parse_data_for_deletion,
            'parse_filesystem_list': self.parse_filesystem_list,
            'parse_show_switch': self.parse_show_switch,
            'parse_show_version': self.parse_show_version,
        }

    # -------------------------------------------------------------------------
    #  ___ _   _ ___ _    ___ ___   __  __ ___ _____ _  _  ___  ___  ___
    # | _ \ | | | _ ) |  |_ _/ __| |  \/  | __|_   _| || |/ _ \|   \/ __|
    # |  _/ |_| | _ \ |__ | | (__  | |\/| | _|  | | | __ | (_) | |) \__ \
    # |_|  \___/|___/____|___\___| |_|  |_|___| |_| |_||_|\___/|___/|___/
    #
    # -------------------------------------------------------------------------

    def filter_model(self, model_arg, debug=False):
        ''' filter_model
            Matches the characters from keyword value at the start of each
            newline.

            Args:
                model: Cisco model
                debug: passing Boolean to enable/disable debug
        '''
        model = ""
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
        # End of if self.debug:

        if isinstance(model_arg, str):
            # The passed argument is a string

            if self.debug:
                message = "(" + self.__who_am_i() + ") The argument " + \
                    "model_arg is a string."
                self.dp.v_debug(message)
            # End of if self.debug:

            # Split a string into a list using character minus (-) as separator
            # but only keep the first 2 elements of the list.
            stripped_model = model_arg.split('-')[0:2]

            if stripped_model[0].upper() == 'WS':
                # The first element has the string 'WS', which stands for
                # Workgroup Switch.

                if self.debug:
                    message = "(" + self.__who_am_i() + ") Detected that " + \
                        "the string starts with the string 'WS'"
                    self.dp.v_debug(message)
                # End of if self.debug:
                model = '-'.join(stripped_model)
            # End of if stripped_model[0].upper() == 'WS':

            else:
                # The first element doesn't have the string 'WS'.
                # Most routers will start with the string CISCO or ISR but most
                # likely have the character slash '/'.

                if self.debug:
                    message = "(" + self.__who_am_i() + ") Detected that " + \
                        "the string doesn't start with string 'WS'"
                    self.dp.v_debug(message)
                # End of if self.debug:

                # Split string into a list using the character slash '/' as
                # separator and return with the first element of the list.
                model = stripped_model[0].split('/')[0]
            # End of else:
        # End of if isinstance(model_arg, str):

        else:
            # The passed argument is NOT a string
            message = "(" + self.__who_am_i() + ") The passed model " + \
                "argument isn't a string."
            self.dp.v_error(message)
            return model
        # End of else:

        if self.debug:
            message = "(" + self.__who_am_i() + ") model = '" + model + "'"
            self.dp.v_debug(message)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return model.upper()
    ''' End of def filter_model(self,model_arg, debug=False): '''

    def find_commands(self, data, command, debug=False):
        ''' find_commands
            Build a dictionary of Cisco exisiting upgrade commands that can be
            used.

            Args:
                data: contains the output from exec command '?'
                command: command string
                debug: passing Boolean to enable/disable debug
            '''
        flag = False
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                      "'data' is a " + str(type(data))
            self.dp.v_debug(message)
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                      "'command' is a " + str(type(data))
            self.dp.v_debug(message)
        # End of if self.debug:

        raw_list = self.__stdout(data, 'find_commands')

        if self.error:
            return False
        # End of if error:

        if not isinstance(command, str):
            message = "(" + self.__who_am_i() + \
                ") The passed command isn't a string."
            self.dp.error(message)
            return False
        # End of if not isinstance(command, str):

        # Split string into a list.
        command_list = command.split()

        if len(command_list) == 0:
            message = "(" + self.__who_am_i() + \
                ") The passed command is empty."
            self.dp.error(message)
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
                if self.debug:
                    message = "(" + self.__who_am_i() + ") Found line: " + \
                        line
                    self.dp.v_debug(message)
                # End of if self.debug:

                flag = True
            # End of if cond:
        # End of for line in raw_list:

        if self.debug:
            message = "(" + self.__who_am_i() + ") flag = " + \
                str(flag) + " <" + str(type(flag))
            message += ">"
            self.dp.v_debug(message)
            self.dp.v_debug("<<< End of def " + self.__who_am_i())
        # End of if self.debug:

        return flag
    ''' End of def find_commands(self, data, command, debug=False): '''

    def find_image_file(self, data, alist, binfile, debug=False):
        ''' find_image_file

            Args:
                data: contains the output from the running IOS command
                alist: passing list to append data into it
                binfile: passing string with name of binary file
                debug: passing Boolean to enable/disable debug
        '''
        data_list = []
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'data' is a " + str(type(data))
            self.dp.v_debug(message)
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'alist' is a " + str(type(alist))
            self.dp.v_debug(message)
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'binfile' is a " + str(type(binfile))
            self.dp.v_debug(message)
        # End of if self.debug:

        cond = (not isinstance(data, list) or not isinstance(
            alist, list) or not isinstance(binfile, str))

        if cond:
            message = "(" + self.__who_am_i() + ") One or both passed " + \
                "arguments wasn't able to pass the condition. " + \
                "'data' = <<list>>, 'folder' = <<string>>"
            self.dp.v_error(message)
            return data_list
        # End of if cond:

        for item in data:
            new_dict = {'filesystem': None, 'filename': None}

            if "item" in item:
                key = "item"
                label = "filesystem"
                new_dict['filesystem'] = self.__parse_find_file(
                    item, key, label)

                if "stdout" in item:
                    key = "stdout"
                    label = None

                    if self.debug:
                        message = "(" + self.__who_am_i() + ") Found " + \
                            "dictionary key 'stdout'."
                        self.dp.v_debug(message)

                    lines = self.__parse_find_file(item, key, label)

                    new_dict['filename'] = self.__parse_filefolder(
                        lines, binfile, '-rw', self.__who_am_i())
            # End of if "item" in item:

            data_list.append(new_dict)
        # End of for item in data:

        df1 = pd.DataFrame(alist).set_index('filesystem')
        df2 = pd.DataFrame(data_list).set_index('filesystem')
        df = df1.merge(df2, left_index=True, right_index=True)
        data_list = df.T.to_dict()

        if self.debug:
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return data_list
    ''' End of def find_image_file(data, alist, binfile, debug=False): '''

    def find_image_folder(self, data, folder, debug=False):
        ''' find_image_folder

            Args:
                data: contains the output from the running IOS command
                source: passing string with name of folder
                debug: passing Boolean to enable/disable debug
            '''
        data_list = []
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'data' is a " + str(type(data))
            self.dp.v_debug(message)
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'folder' is a " + str(type(folder))
            self.dp.v_debug(message)
        # End of if self.debug :

        for item in data:
            new_dict = {}
            new_dict['filesystem'] = ""
            new_dict['directory'] = ""

            if "item" in item:
                new_dict['filesystem'] = item['item']  # Set name of filesystem

                if "stdout" in item:
                    lines = item['stdout'][0].split('\n')

                    new_dict['directory'] = self.__parse_filefolder(
                        lines, folder, 'drw', 'find_image_folder')
                # End of if "stdout" in item:
            # End of if "item" in item:
            data_list.append(new_dict)
        # End of for item in data:

        if self.debug:
            message = "(" + self.__who_am_i() + ") " + str(type(data_list))
            message += " data_list = "
            self.dp.v_debug(message)
            pprint(data_list)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug :

        return data_list
    ''' End of def find_image_folder(data, folder, debug=False): '''

    def iosxe_find_conf_file(self, data, conffile, debug=False):
        ''' iosxe_find_image_file

            Args:
                data: contains the output from the running IOS-XE command
                conffile: passing the name of the package version configuration
                          file
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug
        data_dict = {}
        data_list = []

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'data' is a " + str(type(data))
            self.dp.v_debug(message)
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'conffile' is a " + str(type(conffile))
            self.dp.v_debug(message)
        # End of if self.debug :

        for item in data:
            if "item" in item:
                key = "item"
                label = "filesystem"
                fs = self.__parse_find_file(item, key, label)
                data_dict[fs] = {}

                if "stdout" in item:
                    key = "stdout"
                    label = None

                    if self.debug:
                        message = "(" + self.__who_am_i() + ") Found " + \
                                  "dictionary key 'stdout'."
                        self.dp.v_debug(message)
                    # End of if self.debug:

                    lines = self.__parse_find_file(item, key, label)
                    data_dict[fs]['filename'] = self.__parse_filefolder(
                        lines,
                        conffile,
                        '-rw',
                        self.__who_am_i())
                # End of if "stdout" in item:
            # End of if "item" in item:
        # End of for item in data:

        for k in data_dict:
            if data_dict[k]['filename'] is None:
                data_list.append(False)
            else:
                data_list.append(True)
        # End of for k in data_dict:

        if self.debug:
            message = "(" + self.__who_am_i() + ") data_dict: "
            self.dp.v_debug(message)
            pprint(data_dict)
            message = "(" + self.__who_am_i() + ") data_list: "
            self.dp.v_debug(message)
            pprint(data_list)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return data_list
    ''' End of def iosxe_find_conf_file(self, data, conffile, debug=False): '''

    def iosxe_find_image_file(self, data, binfile, debug=False):
        ''' iosxe_find_image_file

            Args:
                data: contains the output from the running IOS-XE command
                binfile: passing string with name of binary file
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug
        data_dict = {}

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'data' is a " + str(type(data))
            self.dp.v_debug(message)
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'binfile' is a " + str(type(binfile))
            self.dp.v_debug(message)
        # End of if self.debug :

        for item in data:

            if "item" in item:
                key = "item"
                label = "filesystem"
                fs = self.__parse_find_file(item, key, label)
                data_dict[fs] = {}

                if "stdout" in item:
                    key = "stdout"
                    label = None

                    if self.debug:
                        message = "(" + self.__who_am_i() + ") Found " + \
                            "dictionary key 'stdout'."
                        self.dp.v_debug(message)
                    # End of if self.debug:

                    lines = self.__parse_find_file(item, key, label)
                    data_dict[fs]['filename'] = self.__parse_filefolder(
                        lines,
                        binfile,
                        '-rw',
                        self.__who_am_i())
                # End of if "stdout" in item:
            # End of if "item" in item:
        # End of for item in data:

        for fs in data_dict.copy():
            if 'filename' in data_dict[fs]:
                if data_dict[fs]['filename'] is None:
                    del data_dict[fs]  # remove key from dictionary

                # End of if data_dict[fs]['filename'] is None:
            # End of if 'filename' in data_dict[fs]:
        # End of for fs in data_dict.copy():

        if self.debug:
            message = "(" + self.__who_am_i() + ") data_dict: "
            self.dp.v_debug(message)
            pprint(data_dict)
            self.dp.v_debug("<<< End of " + self.__who_am_i())

        return data_dict
    ''' End of def iosxe_find_image_file(self, data, binfile, debug=False): '''

    def iosxe_get_build_version(self, data, required_version, debug=False):
        ''' iosxe_install_cmd_usage function

            Args:
                data: contains the output from the running IOS-XE command
                required_version: passing the IOS-XE version that is required
                                  to have
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug
        data_list = []

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'data' is a " + str(type(data))
            self.dp.v_debug(message)
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                "'required_version' is a " + str(type(required_version))
            self.dp.v_debug(message)
        # End of if self.debug :

        for item in data:
            flag = False

            if "stdout" in item:
                key = "stdout"
                label = ""
                lines = self.__parse_find_file(item, key, label)

                for line in lines:
                    line = line.strip()
                    cond = re.match('^(# pkginfo: Build:)\\s+('
                                    + re.escape(required_version) + ').*', line)

                    if cond:
                        flag = True
                        if self.debug:
                            message = "(" + self.__who_am_i() + ") Found " + \
                                      "line: " + line
                            self.dp.v_debug(message)
                        # End of if self.debug:
                    # End of if cond:
                # End of for line in lines:
                data_list.append(flag)
            # End of if "stdout" in item:
        # End of for item in data:

        if self.debug:
            message = "(" + self.__who_am_i() + ") data_list: "
            self.dp.v_debug(message)
            pprint(data_list)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return data_list
    ''' End of def iosxe_get_build_version( self, data, required_version,
                                            debug=False): '''

    def iosxe_install_cmd_usage(self, use_command, install_flag, request_flag,
                                software_flag, debug=False):
        ''' iosxe_install_cmd_usage function

            Args:
                use_command: empty string
                install_flag: Boolean object
                request_flag: Boolean object
                software_flag: Boolean object
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug
        use_command = ""

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())

        cond = (isinstance(install_flag, bool)
                and isinstance(request_flag, bool)
                and isinstance(software_flag, bool))

        if cond:
            if install_flag:
                use_command = "install"
            elif request_flag:
                use_command = "request"
            elif software_flag:
                use_command = "software"

        # End of if cond:

        if self.debug:
            message = "(" + self.__who_am_i() + ") use_command: " + use_command
            self.dp.v_debug(message)
            self.dp.v_debug("<<< End of " + self.__who_am_i())

        return use_command
    ''' End of def iosxe_install_cmd_usage( self, use_command, install_flag,
                                            request_flag, software_flag,
                                            debug=False): '''

    def iosxe_parse_inactive(self, data, required_version, debug=False):
        ''' iosxe_parse_inactive

            Args:
                data: contains the output from the used Cisco command
                required_version: passing the string to match with
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug
        flag = False

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                      "'data' is a " + str(type(data))
            self.dp.v_debug(message)
            message = "(" + self.__who_am_i() + ") The passed argument " + \
                      "'required_version' is a " + str(type(required_version))
            self.dp.v_debug(message)
        # End of if self.debug:

        raw_list = self.__stdout(data, 'iosxe_parse_inactive')

        for line in raw_list:
            line = line.strip()

            cond1 = re.match('^(No Inactive Packages).*', line)
            cond2 = re.match('.*(' + re.escape(required_version) + ').*', line)

            if cond1:
                if self.debug:
                    message = "(" + self.__who_am_i() + ") Found line: " + line
                    self.dp.v_debug(message)
                # End of if self.debug
            # End of if cond1:

            if cond2:
                flag = True
                if self.debug:
                    message = "(" + self.__who_am_i() + ") Found line: " + line
                    self.dp.v_debug(message)
                # End of if self.debug
            # End of if cond2:

        if self.debug:
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return flag
    ''' End of def iosxe_parse_inactive(self, data, required_version,
                                        debug=False): '''

    def parse_filesystem_list(self, data, debug=False):
        ''' parse_filesystem_list

            Args:
                data: contains the output from the used Cisco command
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug
        data_dict = {}

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
        # End of if self.debug:

        if not isinstance(data, list):
            message = "(" + self.__who_am_i() + ") Passed argument 'data' " + \
                "isn't a list."
            self.dp.v_error(message)
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
                valuelabel = self.__parse_filesystem_space(lines)
            # End of if "stdout" in item:

            if keylabel is not None and valuelabel is not None:
                data_dict[keylabel] = valuelabel
            # End of if keylabel is not None and valuelabel is not None:

        if self.debug:
            self.dp.v_debug("(" + self.__who_am_i() + ") data_dict = ")
            pprint(data_dict)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return data_dict
    ''' End of def parse_filesystem_list(data, debug=False): '''

    def parse_data_for_deletion(self, data, running_ios, required_ios,
                                debug=False):
        ''' ios_parse_data_for_deletion

            Args:
                data: contains the output from the used Cisco command
                running_ios: running IOS software image name
                required_ios: required IOS software image name
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug
        new_list = []

        if self.debug:
            self.dp.v_debug("Start of " + self.__who_am_i())
        # End of if self.debug

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

        for item in data:
            # Loop through each member of the stacked device.
            # If the device isn't a stack then we only have 1 element inside
            # the list 'data'.

            if "item" in item and "stdout" in item:
                new_dict = {}
                new_dict['filesystem'] = item['item']

                # Retrieve list of files and directories where the string
                # starts with a part of the required IOS software name but
                # exclude the current running IOS binary file/directory and the
                # required IOS directory.
                new_dict['deletion'] = self.__parse_data_files(
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

        if self.debug:
            self.dp.v_debug("End of " + self.__who_am_i())
        # End of if self.debug

        return new_list
    ''' End of def parse_data_for_deletion(self, data, running_ios,
            required_ios, debug=False): '''

    def parse_show_switch(self, data, debug=False):
        ''' parse_show_switch

            Args:
                data: contains the output from the used Cisco command
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
        # End of if self.debug:

        show_switch = []
        raw_list = self.__stdout(data, self.__who_am_i())

        if self.error:
            return show_switch

        for line in raw_list:
            # Loop through each output line

            new_dict = {}

            line = line.strip()  # Remove leading and trailing spaces

            # Build condition to match line
            cond1 = re.match('^Switch#\\s+Role\\s+Mac\\sAddress\\s.*', line)

            # Build condition to match line
            cond2 = re.match(
                '^[\\*|\\d][\\d|\\s]\\s+(Master|Member|Active|Standby).*',
                line)

            if cond1:
                if self.debug:
                    self.dp.v_debug(
                        "(" + self.__who_am_i() + ") Found line: " + line)
                # End of if self.debug:
            # End of if cond1:

            if cond2:
                if self.debug:
                    self.dp.v_debug(
                        "(" + self.__who_am_i() + ") Found line: " + line)
                # End of if self.debug:

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
                new_dict['H/W Version'] = line_list[4].strip()
                new_dict['Current State'] = line_list[5].strip()

                show_switch.append(new_dict)
            # End of if cond2:
        # End of for line in raw_list:

        if self.debug:
            message = "(" + self.__who_am_i() + ")" + \
                str(type(show_switch)) + " show_switch = "
            self.dp.v_debug(message)
            pprint(show_switch)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return show_switch
    ''' End of def parse_show_switch(data, debug=False): '''

    def parse_show_version(self, data, debug=False):
        ''' parse_show_version
            Matches the characters from keyword value at the start of each
            newline.

            Args:
                data: contains the output from the used Cisco command
                debug: passing Boolean to enable/disable debug
        '''
        self.debug = debug

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())
        # End of if self.debug:

        device_type = "router"  # Initialize by default as 'router'
        show_version = []

        raw_list = self.__stdout(data, 'parse_show_version')

        if self.error:
            return show_version
        # End of if error:

        # Detect if it is a Switch or Router
        for line in raw_list:
            # Loop through each output line

            line = line.strip()  # Remove leading and trailing spaces

            # Build condition to match line
            cond = re.match('^Switch\\sPorts\\sModel\\s.*', line)

            if cond:
                if self.debug:
                    self.dp.v_debug(line)
                # End of if self.debug:

                device_type = "switch"
            # End of if cond:
        # End of for line in raw_list:

        # Device type is detected as switch
        if device_type == "switch":
            if self.debug:
                message = "(" + self.__who_am_i() + ") Variable " + \
                    "device_type is set with value '" + device_type + "'"
                self.dp.v_debug(message)
            # End of if self.debug:

            for line in raw_list:
                # Loop through each line

                line = line.strip()  # Remove leading and trailing spaces

                # Build condition to match line
                cond = re.match('^[\\*|\\d]\\s+[0-9]+\\s+.*', line)

                if cond:
                    if self.debug:
                        self.dp.v_debug(line)
                    # End of if self.debug:

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
            if self.debug:
                message = "(" + self.__who_am_i() + ") Variable " + \
                    "device_type is set with value '" + device_type + "'"
                self.dp.v_debug(message)
            # End of if self.debug:
        # End of elif device_type == "router":

        else:
            if self.debug:
                message = "(" + self.__who_am_i() + ") Variable " + \
                    "device_type is set with value '" + device_type + "'"
                self.dp.v_debug(message)
            # End of if self.debug:
        # End of else device_type == "router":

        if self.debug:
            message = "(" + self.__who_am_i() + ") " + \
                str(type(show_version)) + " show_version = "
            self.dp.v_debug(message)
            pprint(show_version)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug:

        return show_version
    ''' End of def parse_show_version(self, data, debug=False): '''

    # -------------------------------------------------------------------------
    #  ___ ___ _____   ___ _____ ___   __  __ ___ _____ _  _  ___  ___  ___
    # | _ \ _ \_ _\ \ / /_\_   _| __| |  \/  | __|_   _| || |/ _ \|   \/ __|
    # |  _/   /| | \ V / _ \| | | _|  | |\/| | _|  | | | __ | (_) | |) \__ \
    # |_| |_|_\___| \_/_/ \_\_| |___| |_|  |_|___| |_| |_||_|\___/|___/|___/
    #
    # -------------------------------------------------------------------------

    def __parse_data_files(self, lines, **kwargs):
        ''' __ios_parse_data_files

            Args:
                lines: contains the output of the dir of that specific
                kwargs: passing keyword ( or named) arguments
        '''

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())

        new_list = []

        runfile = re.escape(kwargs['running_ios'])
        rundir = re.escape(kwargs['running_dir'])
        reqdir = re.escape(kwargs['required_dir'])
        f = re.escape(kwargs['filter'])

        for line in lines:
            line = line.strip()  # Remove leading and trailing spaces

            # Build conditional to ignore the running IOS binary file,
            # if exist.
            cond1 = re.match('^[0-9]+\\s+(-rw).*\\s+(' + runfile + ')$', line)

            # Build conditional to ignore the directories that contains the
            # name of the running IOS and required IOS, if exist.
            cond2 = re.match(
                '^[0-9]+\\s+(drw).*\\s+(' + rundir + '|' + reqdir + ')$', line)

            # Build conditional to keep files and directories that contains the
            # model variant name that is extracted from the required IOS.
            cond3 = re.match('^[0-9]+\\s+.*\\s+(' + f + ').*$', line)

            if (not (cond1 or cond2)) and cond3:
                if self.debug:
                    self.dp.v_debug("Found line: " + line)
                # End of if self.debug:

                new_list.append(line.split()[-1])

            # End of if (not (cond1 and cond2)) and cond3:
        # End of for line in lines:

        if self.debug:
            self.dp.v_debug("<<< End of " + self.__who_am_i())

        return new_list
    ''' End of def __parse_data_files(lines, **kwargs): '''

    def __parse_filefolder(self, lines, source, mtype, from_function):
        ''' __parse_filefolder

            Args:
                data: contains the output from the used Cisco command
                source: name of file or folder
                mtype: file/folder to filter on
                from_function: passing the function name

        '''
        result = None
        s = re.escape(source)
        p = re.escape(mtype)

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())

        for line in lines:
            line = line.strip()  # Remove leading and trailing spaces

            cond = re.match('^[0-9]+\\s+' + p + '.*' + s + '$', line)

            if cond:
                if self.debug:
                    self.dp.v_debug(
                        "(" + from_function + ") Found line: " + line)
                # End of if self.debug

                result = line.split()[-1]
            # End of if cond

            cond2 = re.match('^(No files in directory)$', line)

            if cond2:
                if self.debug:
                    message = "(" + from_function + ") Found line: " + \
                        "'No files in directory'"
                    self.dp.v_debug(message)
                # End of if self.debug

                result = None
            # End of if cond2:
        # End of for line in lines:

        if self.debug:
            message = "(" + from_function + ") " + str(type(result))
            message += " result = " + str(result)
            self.dp.v_debug(message)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        # End of if self.debug

        return result
    ''' End of def __parse_filefolder(lines, source, mtype, from_function): '''

    def __parse_filesystem_space(self, lines):
        ''' __parse_filesystem_space

            Args:
                data: contains the output from the used Cisco command
        '''
        data_dict = {}

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())

        for line in lines:
            line = line.strip()  # Remove leading and trailing spaces

            cond1 = re.match(
                '^[0-9]*\\s(bytes available).*', line)

            cond2 = re.match(
                '^[0-9]*\\s(bytes total).*', line)

            if cond1:
                if self.debug:
                    message = "(" + self.__who_am_i() + ") Found line: " + line
                    self.dp.v_debug(message)
                # End of if self.debug:

                free_kb = round(
                    int(
                        re.sub(
                            '\\s+(bytes available)\\s+.*', '', line)) / 1000)
                used_kb = round(int(
                    re.sub('.*\\(([0-9]+?)\\s(bytes used)\\)', '\\1', line)
                ) / 1000)

                data_dict['total_kb'] = free_kb + used_kb
                data_dict['free_kb'] = int(free_kb)
            # End of if cond1:

            elif cond2:
                if self.debug:
                    message = "(" + self.__who_am_i() + ") Found line: " + line
                    self.dp.v_debug(message)
                # End of if self.debug:

                total_kb = round(
                    int(re.sub('\\s+(bytes total)\\s+.*', '', line)) / 1000)
                free_kb = round(
                    int(
                        re.sub(
                            '.*\\(([0-9]+?)\\s(bytes free).*\\)', '\\1', line)
                    ) / 1000)

                data_dict['total_kb'] = int(total_kb)
                data_dict['free_kb'] = int(free_kb)
            # End of elif cond2:
        # End of for line in lines:

        if self.debug:
            self.dp.v_debug("(" + self.__who_am_i() + ") data_dict = ")
            pprint(data_dict)
            self.dp.v_debug("<<< End of " + self.__who_am_i())
        return data_dict
    ''' End of  def __parse_filesystem_space(self, lines): '''

    def __parse_find_file(self, item_object, key, label=None):
        '''  __parse_find_file

            Args:
            item_object: passing object
                key: passing key name
                label: passing label to find
        '''
        rvalue = None

        if self.debug:
            self.dp.v_debug(">>> Start of " + self.__who_am_i())

        if isinstance(item_object[key], dict):
            if self.debug:
                message = "(" + self.__who_am_i() + ") The variable item[" + \
                    key + "] is a dictionary."
                self.dp.v_debug(message)
            # End of if self.debug:

            if label in item_object[key]:
                rvalue = item_object[key][label]

                if self.debug:
                    message = "(" + self.__who_am_i() + \
                        ") The dictionary item[" + key
                    message += "] contains the key '" + label + "'."
                    self.dp.v_debug(message)
                    self.dp.v_debug(("(" + self.__who_am_i() + ") "
                                     "" + label + " = " + rvalue))
                # End of if self.debug:
            # End of if label in item_object[key]:
        # End of if isinstance(item_object[key], dict):

        elif isinstance(item_object[key], list):
            if self.debug:
                message = "(" + self.__who_am_i() + ") The variable item['" + \
                    key + "'] is a list."
                self.dp.v_debug(message)
            # End of if self.debug:
            rvalue = item_object[key][0].split('\n')

        elif isinstance(item_object[key], str):
            if self.debug:
                message = "(" + self.__who_am_i() + ") The variable item['" + \
                    key + "'] is a string."
                self.dp.v_debug(message)
            # End of if self.debug:

            rvalue = item_object[key]
        # End of elif isinstance(item_object[key], str):

        if self.debug:
            self.dp.v_debug("<< < End of " + self.__who_am_i())
        return rvalue
    ''' End of def __parse_find_file(item_object, key, label=None)'''

    # ███╗    ███████╗    ███╗
    # ██╔╝    ██╔════╝    ╚██║
    # ██║     ███████╗     ██║
    # ██║     ╚════██║     ██║
    # ███╗    ███████║    ███║
    # ╚══╝    ╚══════╝    ╚══╝

    def __stdout(self, data, from_method):
        ''' __stdout
            Determine if the passed variable 'data' is a list or string.

            Args:
                data: command output result
                from_method: method name
        '''
        raw_list = []  # Initialize an empty list

        if isinstance(data, str):
            # The variable 'data' is a string

            if self.debug:
                message = "(" + from_method + \
                    ") The argument 'data' is a string."
                self.dp.v_debug(message)
            # End of if self.debug:

            # Split a string into a list using newline as separator
            raw_list = data.split("\n")

        else:
            message = "(" + from_method + ") The passed argument 'data' is "
            message += "not a list nor string."
            self.dp.v_error(message)
            self.error = True
        # End of if isinstance(data, list):

        return raw_list
    ''' End of def __stdout(data, from_method): '''

    def __who_am_i(self):
        return inspect.stack()[1][3]
>>>>>>> origin/dev
