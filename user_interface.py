# Copyright © 2017 - 2018 Acumen Solutions, Inc. The Sandbox Refresh Tool was
# created by Acumen Solutions. Except for the limited rights to use and make
# copies of the Software as provided in a License Agreement, all rights are
# reserved.

import wx
import controller as controller_

# pylint: disable=no-member


class LoginPanel(wx.Panel):
    """The first panel that prompts the user for their login
        information.
    """

    def __init__(self, parent):
        """Initialize the LoginPanel.
        """
        self.parent = parent
        super(LoginPanel, self).__init__(parent)

        self.init_login_ui()
        self.Centre()
        self.Show()

    def init_login_ui(self):
        """Initialize the user interface for the LoginPanel.
        """
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(0,0)

        self.text_username = wx.StaticText(self.panel,
                                           label = 'Username:')
        self.sizer.Add(self.text_username,
                       pos = (0, 0),
                       flag = wx.ALL,
                       border = 5)

        self.tc_username = wx.TextCtrl(self.panel)
        self.sizer.Add(self.tc_username,
                       pos = (0, 1),
                       span = (1, 2),
                       flag = wx.EXPAND | wx.ALL,
                       border = 5)

        self.text_password = wx.StaticText(self.panel,
                                           label = 'Password:')
        self.sizer.Add(self.text_password,
                       pos = (1, 0),
                       flag = wx.ALL,
                       border = 5)

        self.tc_password = wx.TextCtrl(self.panel,
                                       style = wx.TE_PASSWORD)
        self.sizer.Add(self.tc_password,
                       pos = (1, 1),
                       span = (1, 2),
                       flag = wx.EXPAND | wx.ALL,
                       border = 5)

        self.text_token = wx.StaticText(self.panel,
                                        label = 'Security Token:')
        self.sizer.Add(self.text_token,
                       pos = (2, 0),
                       flag = wx.ALL,
                       border = 5)

        self.tc_token = wx.TextCtrl(self.panel,
                                    style = wx.TE_PASSWORD)
        self.sizer.Add(self.tc_token,
                       pos = (2, 1),
                       span = (1, 2),
                       flag = wx.EXPAND | wx.ALL,
                       border = 5)

        self.text_url = wx.StaticText(self.panel,
                                      label = 'Login URL:')
        self.sizer.Add(self.text_url,
                       pos = (3, 0),
                       flag = wx.ALL,
                       border = 5)

        self.tc_url = wx.TextCtrl(self.panel)
        self.sizer.Add(self.tc_url,
                       pos = (3, 1),
                       span = (1, 2),
                       flag = wx.EXPAND | wx.ALL,
                       border = 5)

        self.text_url_help = wx.StaticText(self.panel,
                                           label = controller_.RefreshMethods.url_example_text())
        self.sizer.Add(self.text_url_help,
                       pos = (4, 0),
                       span = (1, 2),
                       flag = wx.ALL,
                       border = 5)

        self.button_submit = wx.Button(self.panel,
                                       label = 'Submit')
        self.Bind(wx.EVT_BUTTON,
                  self.on_submit_button_clicked,
                  self.button_submit)
        self.sizer.Add(self.button_submit,
                       pos = (5, 1),
                       flag = wx.ALL,
                       border = 5)

        self.button_clear = wx.Button(self.panel,
                                      label = 'Clear')
        self.Bind(wx.EVT_BUTTON,
                  self.on_clear_button_clicked,
                  self.button_clear)
        self.sizer.Add(self.button_clear,
                       pos = (5, 2),
                       flag = wx.ALL,
                       border = 5)

        self.panel.SetSizerAndFit(self.sizer)

    def on_submit_button_clicked(self, e):
        """Validate that required fields are populated. Perform a rest
            login to validate user credentials.
        """
        self.credentials_error_message = controller_.RefreshMethods.validate_credentials(self.tc_username.GetValue(),
                                                                                         self.tc_password.GetValue(),
                                                                                         self.tc_url.GetValue())
        if self.credentials_error_message:
            self.warning = wx.MessageDialog(self.panel,
                                            self.credentials_error_message,
                                            'Invalid Information',
                                            wx.OK | wx.ICON_WARNING)
            self.warning.ShowModal()
            self.warning.Destroy()
        else:
            controller_.RefreshMethods.save_login_info(self.tc_username.GetValue(),
                                                       self.tc_password.GetValue(),
                                                       self.tc_token.GetValue(),
                                                       self.tc_url.GetValue())
            try:
                # pylint: disable=unused-variable
                salesf = controller_.RefreshMethods.connect_to_simplesalesforce()
            except Exception as ex:
                self.warning = wx.MessageDialog(self.panel,
                                                ex.message,
                                                'Error Connecting With Credentials',
                                                wx.OK | wx.ICON_WARNING)
                self.warning.ShowModal()
                self.warning.Destroy()
            else:
                self.parent.close_login_open_script_selector()
        e.Skip()

    def on_clear_button_clicked(self, e):
        """Clear out the values of the user login information fields.
        """
        self.tc_username.ChangeValue('')
        self.tc_password.ChangeValue('')
        self.tc_token.ChangeValue('')
        self.tc_url.ChangeValue('')
        e.Skip()

    def remove_circular_references(self):
        """Remove the circular reference to the parent to faciliate
            with garbage collection.
        """
        del self.parent


class ScriptSelectorPanel(wx.Panel):
    """The panel after a user has entered their credentials. The user
        selects the refresh scripts to run in the environment.
    """

    def __init__(self, parent):
        """Initialize the ScriptSelectorPanel.
        """
        self.parent = parent
        super(ScriptSelectorPanel, self).__init__(parent)

        self.init_selector_ui()
        self.Show()

    def init_selector_ui(self):
        """Initialize the user interface for the ScriptSelectorPanel.
        """
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(0,0)

        self.text_login_as = wx.StaticText(self.panel,
                                           label = 'Logged in as:')
        self.sizer.Add(self.text_login_as,
                       pos = (0, 0),
                       flag = wx.ALL,
                       border = 5)

        self.text_username = wx.StaticText(self.panel,
                                           label = controller_.login_information['sf.username'])
        self.sizer.Add(self.text_username,
                       pos = (0, 1),
                       flag = wx.ALL,
                       border = 5)

        self.text_select_instructions = wx.StaticText(self.panel,
                                                      label = 'Select the refresh scripts to run:')
        self.sizer.Add(self.text_select_instructions,
                       pos = (1, 0),
                       span = (1, 2),
                       flag = wx.ALL,
                       border = 5)

        self.sl_script_List = wx.ListBox(self.panel,
                                         style = wx.LB_MULTIPLE,
                                         choices = controller_.RefreshMethods.get_refresh_options())
        self.sizer.Add(self.sl_script_List,
                       pos = (2, 0),
                       span = (1, 2),
                       flag = wx.ALL,
                       border = 5)

        self.text_reminders = wx.StaticText(self.panel,
                                            label = controller_.RefreshMethods.before_execution_reminders())
        self.sizer.Add(self.text_reminders,
                       pos = (3, 0),
                       span = (1, 2),
                       flag = wx.ALL,
                       border = 5)

        self.button_refresh = wx.Button(self.panel,
                                        label = 'Refresh')
        self.Bind(wx.EVT_BUTTON,
                  self.on_refresh_button_clicked,
                  self.button_refresh)
        self.sizer.Add(self.button_refresh,
                       pos = (4, 0),
                       flag = wx.ALL,
                       border = 5)

        self.panel.SetSizerAndFit(self.sizer)

    def on_refresh_button_clicked(self, e):
        """Start the refresh using the selected refresh scripts.
        """
        controller_.selected_refresh_scripts = self.sl_script_List.GetSelections()
        controller_.RefreshMethods.refresh_the_environment()
        self.parent.close_script_selector_open_finish_panel()
        e.Skip()

    def remove_circular_references(self):
        """Remove the circular reference to the parent to faciliate
            with garbage collection.
        """
        del self.parent


class FinishPanel(wx.Panel):
    """The final panel that confirms the script finished successfully.
        Also displays a reminder of after script manual steps left.
    """

    def __init__(self, parent):
        """Initialize the FinishPanel.
        """
        self.parent = parent
        super(FinishPanel, self).__init__(parent)

        self.init_finish_ui()
        self.Centre()
        self.Show()

    def init_finish_ui(self):
        """Initialize the user interface for the FinishPanel.
        """
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(0,0)

        self.text_login_as = wx.StaticText(self.panel,
                                           label = 'Logged in as:')
        self.sizer.Add(self.text_login_as,
                       pos = (0, 0),
                       flag = wx.ALL,
                       border = 5)

        self.text_username = wx.StaticText(self.panel,
                                           label = controller_.login_information['sf.username'])
        self.sizer.Add(self.text_username,
                       pos = (0, 1),
                       flag = wx.ALL,
                       border = 5)

        self.text_complete = wx.StaticText(self.panel,
                                           label = 'The refresh is complete.')
        self.sizer.Add(self.text_complete,
                       pos = (1, 0),
                       span = (1, 2),
                       flag = wx.EXPAND | wx.ALL,
                       border = 5)

        self.text_reminders = wx.StaticText(self.panel,
                                            label = controller_.RefreshMethods.end_of_script_reminders())
        self.sizer.Add(self.text_reminders,
                       pos = (2, 0),
                       span = (1, 2),
                       flag = wx.EXPAND | wx.ALL,
                       border = 5)

        self.button_close = wx.Button(self.panel,
                                      label = 'Close')
        self.Bind(wx.EVT_BUTTON,
                  self.on_close_button_clicked,
                  self.button_close)
        self.sizer.Add(self.button_close,
                       pos = (3, 0),
                       span = (1, 2),
                       flag = wx.EXPAND | wx.ALL,
                       border = 5)

        self.panel.SetSizerAndFit(self.sizer)

    def on_close_button_clicked(self, e):
        """Close the application when the close button is clicked.
        """
        self.parent.Close()
        e.Skip()

    def remove_circular_references(self):
        """Remove the circular reference to the parent to faciliate
            with garbage collection.
        """
        del self.parent


class RefreshTool(wx.Frame):
    """Parent class for all the children panels for the refresh tool.
    """

    def __init__(self,parent):
        """Initalize the refresh tool.
        """
        super(RefreshTool, self).__init__(parent)
        self.init_ui()
        self.Bind(wx.EVT_CLOSE,
                  self.OnCloseOfApp,
                  self)

    def init_ui(self):
        """Initialize the user interface for the refresh tool starting
            with the login panel.
        """
        self.login_panel = LoginPanel(self)

        self.SetTitle('Sandbox Refresh Tool')
        self.Centre()
        self.Show(True)

    def close_login_open_script_selector(self):
        """Close the login panel and open the script selector panel.
        """
        self.login_panel.remove_circular_references()
        self.login_panel.Destroy()
        self.script_selector_panel = ScriptSelectorPanel(self)
        self.SendSizeEvent()

    def close_script_selector_open_finish_panel(self):
        """Close the script selector panel and open the finish panel.
        """
        self.script_selector_panel.remove_circular_references()
        self.script_selector_panel.Destroy()
        self.finish_panel = FinishPanel(self)
        self.SendSizeEvent()

    def OnCloseOfApp(self, e):
        """When application closes remove the login information
            that was stored for the ANT tool.
        """
        controller_.RefreshMethods.remove_login_information()
        e.Skip()


ex = wx.App()
RefreshTool(None)
ex.MainLoop()