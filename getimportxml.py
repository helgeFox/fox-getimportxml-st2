import sublime, sublime_plugin, sys, os

from suds.client import Client

class ShowContentsCommand(sublime_plugin.TextCommand):
  def run(self, edit, content):
    for region in self.view.sel():
      self.view.replace(edit, region, content)

class getimportxmlCommand(sublime_plugin.TextCommand):

  url = ''
  environments = {
    'Stage': 'http://ws.prod.stage.foxpublish.net/EditorService.asmx?WSDL',
    'Prod': 'http://ws.prod.foxpublish.net/EditorService.asmx?WSDL'
    }
  env_options = ['Stage', 'Prod']
  clip = ''

  def is_enabled(self):
    return True

  def run(self, edit):
    self.clip = sublime.get_clipboard()
    self.view.window().show_quick_panel(self.env_options, self.on_env_changed)

  def on_env_changed(self, index):
    self.url = self.environments[self.env_options[index]]
    self.check_clipboard()

  def check_clipboard(self):
    options = ['SessionID \'' + self.clip + '\'', 'Type it...'];
    self.view.window().show_quick_panel(options, self.on_clip_selected)

  def on_clip_selected(self, index):
    if index == 0:
      self.on_panel_done(self.clip)
    else:
      self.request_sessoinid()

  def request_sessoinid(self):
    caption = "Set sessionid"
    initial_text = ""
    panel = self.view.window().show_input_panel (
      caption, 
      initial_text, 
      self.on_panel_done,
      self.on_panel_change,
      self.on_cancel)

  def on_panel_done(self, sessionid):
    if sessionid:
      client = Client(self.url)
      result = client.service.GetImportXml(sessionid)
      try:
        self.show_result(result)
      except:
        sublime.message_dialog('No xml returned from service.')

  def show_result(self, content):
    view = sublime.active_window().new_file()
    view.run_command('show_contents', {"content": content.Xml})
    view.run_command('fox_cleanup_xml')

  def on_panel_change(self, abbr):
    if abbr:
      print ("Input: " + abbr)
      return

  def on_cancel(self):
    print ('GetImportXml cancelled')
    return
