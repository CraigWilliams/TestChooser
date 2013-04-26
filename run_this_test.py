import os, subprocess
import sublime, sublime_plugin, io

class RunThisTestCommand(sublime_plugin.WindowCommand):

  def run(self, paths = [], name = ""):
    self.settings         = sublime.load_settings('TestChooser.sublime-settings')
    search_terms          = self.settings.get('search_terms')
    self.terminal         = self.settings.get('terminal')
    self.filepath         = self.window.active_view().file_name()
    self.filetype         = self.set_file_type()

    if self.filetype == 'unknown':
      self.exit_with_alert()
    else:
      line_number = self.window.active_view().rowcol(self.window.active_view().sel()[0].begin())[0]+1
      self.run_test(line_number)

  def run_test(self, line):
    formatted_line = self.format_line(line)

    if self.terminal == "iTerm":
      applescript = self.iterm_script()
      self.execute_cmd(applescript, formatted_line)
    else:
      applescript = self.terminal_script()
      self.execute_cmd(applescript, formatted_line)

    self.activate_sublime()

  def format_line(self, line):
    return "%s %s:%s" % (self.filetype, self.filepath, line)

  def execute_cmd(self, applescript, formatted_line):
    cmd = applescript.replace("$cmd", formatted_line)
    cmd = "osascript -e '%s'" % cmd
    os.system(cmd)

  def set_file_type(self):
    if 'feature' in self.filepath:
      return self.settings.get('cucumber_command')
    elif 'spec' in self.filepath:
      return self.settings.get('rspec_command')
    else:
      return 'unknown'

  def exit_with_alert(self):
    sublime.error_message('This is not a Cucumber or RSpec file.')

  def iterm_script(self):
    return """
      tell application "iTerm"
        tell current session of terminal 1
          write text "$cmd"
        end tell
      end tell
    """

  def terminal_script(self):
    return """
      tell application "Terminal"
        tell window 1
          do script "$cmd" in selected tab
        end tell
      end tell
    """

  def activate_sublime(self):
    subprocess.Popen("""osascript -e 'tell app "Sublime Text 2" to activate'""", shell=True)