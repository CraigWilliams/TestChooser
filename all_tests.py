import os, subprocess
import sublime, sublime_plugin, io

class AllTestsCommand(sublime_plugin.WindowCommand):

  def run(self, paths = [], name = ""):
    self.settings         = sublime.load_settings('TestChooser.sublime-settings')
    search_terms          = self.settings.get('search_terms')
    self.terminal         = self.settings.get('terminal')
    self.filepath         = self.window.active_view().file_name()
    self.testable_lines   = ["Run'em All", "Run All Specs", "Run All Features"]

    chosen_test = self.choose_test()

  def choose_test(self):
    self.window.show_quick_panel(self.testable_lines, self.chose_item)

  def chose_item(self, chosen_test):
    if chosen_test != -1:
      test_command = self.pick_test_to_run(self.testable_lines[chosen_test])

      if self.terminal == "iTerm":
        applescript = self.iterm_script()
        self.execute_cmd(applescript, test_command)
      else:
        applescript = self.terminal_script()
        self.execute_cmd(applescript, test_command)

    self.activate_sublime()

  def pick_test_to_run(self, chosen_test):
    if chosen_test == "Run All Specs":
      return "%s ." % (self.settings.get('rspec_command'))
    elif chosen_test == "Run All Features":
      return "%s*.features" % (self.settings.get('cucumber_command'))
    else:
      return "%s; %s*.features" % (self.settings.get('rspec_command'), self.settings.get('cucumber_command'))

  def execute_cmd(self, applescript, test_command):
    cmd = applescript.replace("$cmd", test_command)
    cmd = "osascript -e '%s'" % cmd
    os.system(cmd)

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