try:
  from appscript import *
  from osax import *
except ImportError, e:
  pass

import os
import sublime, sublime_plugin, io

class TestChooserCommand(sublime_plugin.WindowCommand):

  def run(self, paths = [], name = ""):

    if self.check_for_appscript_installation():
      settings              = sublime.load_settings('TestChooser.sublime-settings')
      search_terms          = settings.get('search_terms')
      terminal              = settings.get('terminal')
      self.filepath         = self.view.file_name()
      self.filetype         = self.set_file_type()
      self.last_choice_path = self.ensure_last_choice_path()

      if self.filetype == 'unknown':
        self.exit_with_alert()

      else:
        line_number = 0
        testable_lines = ["Run'em All"]

        for line in io.open(self.filepath, 'r'):
          line_number += 1
          for word in search_terms:
            if line.strip().startswith(word):
              testable_lines.append("%03d:%s" % (line_number, line))
              break

        chosen_test = self.choose_test(testable_lines)
        if chosen_test:
          cmd = self.format_line(chosen_test)

          if terminal == "":
            self.execute_cmd(cmd)
          else:
            self.execute_cmd_in_terminal(cmd)

  def choose_test(self, listitems):
    sa = OSAX()
    last_choice = self.get_last_choice()

    if last_choice != '':
      chosen_test = sa.choose_from_list(listitems,
                                        with_title=u'Choose a test to run.',
                                        default_items=[last_choice],
                                        multiple_selections_allowed=False,
                                        OK_button_name=u'Run')
    else:
      chosen_test = sa.choose_from_list(listitems,
                                        with_title=u'Choose a test to run.',
                                        multiple_selections_allowed=False,
                                        OK_button_name=u'Run')

    if chosen_test != False:
      chosen = chosen_test[0]
      self.set_last_choice(chosen)
      return chosen
    else:
      return False

  def format_line(self, line):
    if line == "Run'em All":
      return "bundle exec %s %s --drb" % (self.filetype, self.filepath)
    else:
      items = line.split(":")
      return "bundle exec %s %s:%s --drb" % (self.filetype, self.filepath, items[0])

  def execute_cmd(self, cmd):
    app(u'iTerm.app').terminals[1].current_session.write(text=cmd)

  def execute_cmd_in_terminal(self,cmd):
    app(u'Terminal.app').windows[1].do_script(cmd, in_=app.windows[1].selected_tab)

  def set_file_type(self):
    if 'feature' in self.filepath:
      return 'cucumber -r features/'
    elif 'spec' in self.filepath:
      return 'rspec'
    else:
      return 'unknown'

  def exit_with_alert(self):
    OSAX().display_dialog('This is not a Cucumber or RSpec file.', buttons=['OK'], default_button=1)

  def get_last_choice(self):
    return io.open(self.last_choice_path, 'r').readline()

  def set_last_choice(self, choice):
    f = open(self.last_choice_path, 'w')
    f.write(choice)
    f.close()

  def ensure_last_choice_path(self):
    path = self.last_choice_file('last_choice.txt')
    if not os.path.exists(path):
      f = open(path, 'w')
      f.write("Run'em All")
      f.close()
    return path

  def last_choice_file(self, name):
    return os.path.join(sublime.packages_path(), 'TestChooser', 'LastChoice', name)

  def check_for_appscript_installation(self):
    appscript_file_name = "appscript-1.0.0-py2.6-macosx-10.7-intel.egg"
    dir_path = os.path.dirname(sublime.packages_path())
    installed_packages_path = os.path.join(dir_path, appscript_file_name)
    if not os.path.exists(installed_packages_path):
      error_text = os.path.join(sublime.packages_path(), 'TestChooser', 'messages', 'install.txt')
      self.window.open_file(error_text)
      return False
    else:
      return True
