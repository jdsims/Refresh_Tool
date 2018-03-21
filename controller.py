#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2017 - 2018 Acumen Solutions, Inc. The Sandbox Refresh Tool was
# created by Acumen Solutions. Except for the limited rights to use and make
# copies of the Software as provided in a License Agreement, all rights are
# reserved.

from subprocess import call
from shutil import rmtree, copytree
from os import mkdir, listdir
from simple_salesforce import Salesforce
from datetime import datetime
import xml.etree.ElementTree as ET
import string
import time
import getpass
import sys

# "login_information" Holds the login information for use during the
# Tooling API calls.
login_information = {}

# "selected_refresh_scripts" Holds the position of the selected scripts
# in get_refresh_options()
selected_refresh_scripts = []

# Declaring namespace to make ElementTree lines more readable
ET.register_namespace('', 'http://soap.sforce.com/2006/04/metadata')


class RefreshMethods():
    """The methods used to manipulate, download, and upload the refresh
    data.
    """

    # Variable for the ElementTree namespace. Make later lines more
    # readable.
    nsPrePend = '{http://soap.sforce.com/2006/04/metadata}'

    # Initialize constants for folder references
    RETRIEVED = 'retrieved'
    TOGGLE = 'toggle'
    SETTING = 'setting'
    COPY_TOGGLE = 'copyToggle'
    WORKFLOW_PATH = 'toggle/workflows/'
    OBJECT_PATH = 'toggle/objects/'
    TRIGGER_PATH = 'toggle/triggers/'
    FLOW_PATH = 'toggle/flowDefinitions/'
    RETRIEVED_OBJECT_PATH = 'retrieved/objects/'
    RETRIEVED_WORKFLOW_PATH = 'retrieved/workflows/'
    RETRIEVED_EMAIL_PATH = 'retrieved/email/'

    # List out the triggers that need to be disabled
    triggers_to_toggle = (
        'contactTrigger',
        'accountTrigger'
    )

    # List out the objects that need their workflows toggled off
    object_workflows_to_toggle = (
        'Account',
        'Contact'
    )

    @staticmethod
    def on_complete_refresh(org_name, server):
        RefreshMethods().save_connection_information(org_name, server)
        refresh_options = RefreshOptions()
        refresh_options.refresh_main_refresh_steps()

    @staticmethod
    def run_specified_steps(org_name, server, steps):
        refresh_options = RefreshOptions()
        RefreshMethods().save_connection_information(org_name, server)
        method_dict = {}
        for func in dir(RefreshOptions):
            if func.startswith('refresh_'):
                method_dict[string.capwords(func.replace('refresh_','').replace('_', ' '))] = func
        for step in steps:
            method = getattr(refresh_options, method_dict[step])
            method()

    @staticmethod
    def save_connection_information(org_name, server):
        admin_username = 'adminuser@refreshautomation.com.' + org_name
        admin_password = 'useradmin1'
        server = server
        RefreshMethods.save_login_info(admin_username, admin_password, "", 'https://' + server + '.salesforce.com')

    @staticmethod
    def save_login_info(username, password, security_token, server):
        """Save the user login information in the build.properties file
            for the Salesforce Migration Tool and add it to the
            login_information dictionary.
        """
        global login_information
        login_information['sf.username'] = username
        login_information['sf.passwordWithToken'] = password + security_token
        login_information['sf.password'] = password
        login_information['sf.securityToken'] = security_token
        login_information['sf.serverurl'] = server
        if not server:
            login_information['sf.serverurl'] = 'https://test.salesforce.com'
        else:
            login_information['sf.serverurl'] = server

        updated_lines = []
        with open('build.properties') as file:
            for line in file:  
                splitter = line.split(' ')
                if line.strip().startswith('sf.username'):
                    line = splitter[0] + ' = ' + username + '\n'
                elif line.strip().startswith('sf.passwordWithToken'):
                    line = splitter[0] + ' = ' + password + security_token + '\n'
                elif line.strip().startswith('sf.password'):
                    line = splitter[0] + ' = ' + password + '\n'
                elif line.strip().startswith('sf.securityToken'):
                    line = splitter[0] + ' = ' + security_token + '\n'
                elif line.strip().startswith('sf.serverurl'):
                    if not server:
                        line = splitter[0] + ' = https://test.salesforce.com/'
                    else:
                        line = splitter[0] + ' = ' + server
                updated_lines.append(line)
        with open('build.properties', 'w') as file:
            for line in updated_lines:
                file.write(line)

    @staticmethod
    def remove_login_information():
        """Remove the saved user information from the build.properties
            file.
        """
        updated_lines = []
        with open('build.properties') as file:
            for line in file:
                splitter = line.split(' ')
                if line.strip().startswith('sf.username'):
                    line = splitter[0] + ' = username\n'
                elif line.strip().startswith('sf.passwordWithToken'):
                    line = splitter[0] + ' = passwordSecurityToken\n'
                elif line.strip().startswith('sf.password'):
                    line = splitter[0] + ' = password\n'
                elif line.strip().startswith('sf.securityToken'):
                    line = splitter[0] + ' = securityToken\n'
                elif line.strip().startswith('sf.serverurl'):
                    line = splitter[0] + ' = url'
                updated_lines.append(line)
        with open('build.properties', 'w') as file:
            for line in updated_lines:
                file.write(line)

    @staticmethod
    def connect_to_simplesalesforce():
        """Initialize the SimpleSalesforce connection. Returns
            the active connection.
        """
        global login_information
        print('Connecting with SimpleSalesforce...')
        salesf = Salesforce(
            username=login_information['sf.username'],
            password=login_information['sf.password'],
            security_token=login_information['sf.securityToken'],
            custom_url=login_information['sf.serverurl']
        )
        return salesf
    @staticmethod
    def end_of_script_reminders():
        """Return a string containing the end of refresh reminders.
        """
        reminder_string = 'Please finish the remaining manual steps:'
        reminder_string += '\nUpdate the stored Secret and Key for connected apps.'
        return reminder_string

    @staticmethod
    def before_execution_reminders():
        """Return a string containing the before execution reminders.
        """
        reminder_string = 'Prior to refreshing:'
        reminder_string += '\nEnsure email deliverability is set to "System Only".'
        return reminder_string

    @staticmethod
    def url_example_text():
        """Return a string containing the valid url examples.
        """
        url_example = 'Use a full url like:'
        url_example += '\nhttps://example.my.salesforce.com'
        url_example += '\nhttps://cs91.salesforce.com'
        return url_example

    @staticmethod
    def get_refresh_options_display():
        """Return the list of method display names in class RefreshOptions that
            are prepended with "refresh_".
        """
        method_list = [string.capwords(func.replace('refresh_','').replace('_', ' ')) for func in dir(RefreshOptions) if func.startswith('refresh_')]
        method_list.sort()
        return method_list

    @staticmethod
    def get_refresh_options():
        """Return the list of method display names in class RefreshOptions that
            are prepended with "refresh_".
        """
        method_list = [func for func in dir(RefreshOptions) if func.startswith('refresh_')]
        method_list.sort()
        return method_list

    @staticmethod
    def refresh_the_environment():
        """Begin the refresh of the logged in environment.
        """
        global selected_refresh_scripts
        refresh = RefreshOptions()
        additional_refresh_methods = RefreshMethods().get_refresh_options()
        for pos in selected_refresh_scripts:
            method = getattr(refresh, additional_refresh_methods[pos])
            method()

    @staticmethod
    def validate_credentials(username, password, url):
        """Validate the username is not blank, password is not blank,
            and url is a valid url. Returns an error message that is
            blank if no errors are found.
        """
        error_message = ''
        if not username:
            error_message += 'A username is required.\n'
        if not password:
            error_message += 'A password is required.\n'
        if not url:
            error_message += 'A login URL is required.\n'
        if not url.startswith('https://'):
            error_message += 'The login URL must start with "https://".\n'
        return error_message

    def call_shell(self, args):
        """Call the shell with the specified arguement.
        """
        print('Calling shell with ' + args)
        return call(args, shell=True)

    def clean_directory(self, directory):
        """Delete an existing directory and remake it as an empty
            directory.
        """
        print('Cleaning ' + directory + ' directory...')
        rmtree(directory)
        mkdir(directory)
        print(directory + ' directory deleted.')

    def replace_values(self, directory, tag_name, original, replacement):
        """Replace the "original" value with the "replacement" value in
            the specified "directory" between all instances of the
            "tag_name". "tag_name" does not include brackets.
        """
        print('Looking for replacements...')
        for fileName in listdir(directory):
            updatedLines = []
            with open(directory + fileName) as file:
                for line in file:
                    if line.strip().startswith('<' + tag_name + '>'):
                        print('Found a matching {tag_name} in {fileName}')
                        line = line.replace(original, replacement)
                    updatedLines.append(line)
            with open(directory + fileName, 'w') as file:
                for line in updatedLines:
                    file.write(line)

    def disable_triggers(self):
        """Disable all triggers in the triggers_to_toggle list.
        """
        print('Disabling triggers...')
        for trigger in self.triggers_to_toggle:
            tree = ET.parse(self.TRIGGER_PATH + trigger + '.trigger-meta.xml')
            root = tree.getroot()
            for status in root.findall(self.nsPrePend + 'status'):
                status.text = 'Inactive'
            tree.write(self.TRIGGER_PATH + trigger + '.trigger-meta.xml',
                       encoding='UTF-8',
                       xml_declaration = True)

    def disable_active_workflows(self):
        """Disable all workflows on the objects listed in the
            object_workflows_to_toggle list.
        """
        print('Disabling workflows...')
        for object in self.object_workflows_to_toggle:
            tree = ET.parse(self.WORKFLOW_PATH + object + '.workflow')
            root = tree.getroot()
            for rule in root.findall(self.nsPrePend + 'rules'):
                node = rule.find(self.nsPrePend + 'active')
                if node.text == 'true':
                    node.text = 'false'
            tree.write(self.WORKFLOW_PATH + object + '.workflow',
                       encoding='UTF-8',
                       xml_declaration = True)

    def copy_toggle_directory(self):
        """Copy the TOGGLE directory into the COPY_TOGGLE directory.
        """
        rmtree(self.COPY_TOGGLE)
        copytree(self.TOGGLE, self.COPY_TOGGLE)

    def queue_apex_batch(self, class_name):
        """Queue a queueable apex batch for execution.
        """
        print('Queueing apex batch ' + class_name + '...')
        salesf = self.connect_to_simplesalesforce()
        tooling_access = 'executeAnonymous'
        script = 'ID jobID = System.enqueueJob(new ' + class_name + '());'
        parameters = {'anonymousBody': script}
        salesf.tooling(path=tooling_access, params=parameters)

    def update_formula_field_on_object(self, object_api_name, field_api_name,
                                       original_value, new_value):
        """Update the formula field "field_api_name" on the object
            "object_api_name". Replace the "original_value" with the
            "new_value".
        """
        print('Updating custom links on Contact...')
        tree = ET.parse(self.RETRIEVED_OBJECT_PATH + object_api_name +'.object')
        root = tree.getroot()
        for field in root.findall(self.nsPrePend + 'fields'):
            node = field.find(self.nsPrePend + 'fullName')
            link = field.find(self.nsPrePend + 'formula')
            if node.text == field_api_name:
                link.text = link.text.replace(original_value, new_value)
        tree.write(self.RETRIEVED_OBJECT_PATH + object_api_name + '.object',
                   encoding = "UTF-8",
                   xml_declaration = True)

    def disable_additional_send_to_emails_in_alerts(self):
        """Disable all emails listed as "Additional Send To Emails"
            on email alerts by appending ".off" to them.
        """
        print('Disabling additional send to emails...')
        for file_name in listdir(self.RETRIEVED_WORKFLOW_PATH):
            tree = ET.parse(self.RETRIEVED_WORKFLOW_PATH + file_name)
            root = tree.getroot()
            for node in root.findall(self.nsPrePend + 'alerts'):
                for email in node.findall(self.nsPrePend + 'ccEmails'):
                    email.text = email.text + '.off'
            tree.write(self.RETRIEVED_WORKFLOW_PATH + file_name,
                       encoding = "UTF-8",
                       xml_declaration = True)

    def update_hardcoded_email_template(self, email_api_name, orginal_value,
                                        replacement_value, line_identifier):
        """Update the URL that is hard coded in an email template.
        """
        print('Updating hardcoded email templates...')
        updated_lines = []
        with open(self.RETRIEVED_EMAIL_PATH + 'VF/' + email_api_name + '.email') as file:
            for line in file:
                if line_identifier in line:
                    line = line.replace(orginal_value, replacement_value)
                updated_lines.append(line)
        with open(self.RETRIEVED_EMAIL_PATH + 'VF/' + email_api_name + '.email', 'w') as file:
            for line in updated_lines:
                file.write(line)


# Begin the update script steps ###############################################
class RefreshOptions():
    """The different refresh options available.
    """

    methods = RefreshMethods()

    def refresh_main_refresh_steps(self):
        """Execute the main refresh steps.
        """
        self.methods.clean_directory(self.methods.TOGGLE)
        self.methods.call_shell('ant pullToggle')
        self.methods.copy_toggle_directory()
        self.methods.disable_triggers()
        self.methods.disable_active_workflows()
        self.methods.call_shell('ant deployToggle')
        self.methods.clean_directory(self.methods.RETRIEVED)
        self.methods.call_shell('ant pull')
        self.methods.update_formula_field_on_object('Contact', 'Custom_Formula__c', '||', '&&')
        self.methods.disable_additional_send_to_emails_in_alerts()
        self.methods.update_hardcoded_email_template('Custom_VF_Email', 'login', 'test', 'https://')
        self.methods.call_shell('ant deploy')
        self.methods.call_shell('ant deployCopyToggle')

    def refresh_fix_admin_emails(self):
        """Fix emails on admin users.
        """
        self.methods.call_shell('ant deployFixAdminEmails')
        self.methods.queue_apex_batch('RefreshApex1')

    def refresh_create_test_records(self):
        """Create test data records.
        """
        self.methods.call_shell('ant deployCreateTestRecords')
        self.methods.queue_apex_batch('RefreshApex2')

# End the update script steps #################################################
