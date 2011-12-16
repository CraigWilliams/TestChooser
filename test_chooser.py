from appscript import *
from osax import *
import os
import sublime, sublime_plugin, io

class TestChooserCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		search_terms = set(['it', 'describe', 'context', 'Scenario'])
		self.last_choice_path = self.ensure_last_choice_path()

		self.filepath = self.view.file_name()
		self.filetype = self.set_file_type()

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
				self.execute_cmd(cmd)

	def choose_test(self, listitems):
		sa = OSAX()
		last_choice = self.get_last_choice()

		if last_choice != '':
			chosen_test = sa.choose_from_list(listitems, default_items=[last_choice])
		else:
			chosen_test = sa.choose_from_list(listitems)

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
		io.open(self.last_choice_path, 'w').write(choice)

	def ensure_last_choice_path(self):
		path = os.path.join(os.getcwd(), 'last_choice.txt')
		if not os.path.exists(path):
			open(path, 'w').close()
		return path