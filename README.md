#TestChooser
A Sublime Text 2 plugin for quickly executing a RSpec & Cucumber commands in [iTerm](http://iterm.sourceforge.net/) or Apple's Terminal.


## Description
It first checks the current file to see that it is either a "feature" or "spec" file. If so, it reads the file looking for "it", "describe", "context" or "scenario" keywords that are at the beginning of a line.

It then displays those lines for you to choose from. Once you select an item from the list and click "Run", the test is executed in [iTerm](http://iterm.sourceforge.net/) or Apple's Terminal, whichever you have set in preferences. The default is iTerm.


## Instructions
#### This Plugin
Install this plugin using [Package Control](http://wbond.net/sublime_packages/package_control), a
package manager for Sublime Text 2.

#### Key Bindings
There is a menu item to access the key binding for TestChooser.

"Preferences"->"Package Settings"->"TestChooser"->"Key Bindings - User"

This one uses a two-key combination. The "super" is the "command" key on a Mac.

`{ "keys": ["super+y", "super+y"], "command": "test_chooser" }`


#### Settings
"Preferences"->"Package Settings"->"TestChooser"->"Settings - User"

Choose your terminal. The default is iTerm but you can also choose Apple's Terminal by using the word "Terminal"

`"terminal": "iTerm"`

The search terms used when searching the RSpec and Cucumber files.

`"search_terms": ["it", "describe", "context", "Scenario"]`

Set the RSpec terminal command.

`"rspec_command": "bundle exec rspec --drb"`

Set the Cucumber terminal command.

`"cucumber_command": "bundle exec cucumber --drb -r features/"`

## License

Read the license text file included in this package... but it's MIT.

## Changelog

Changed the original plugin to now use [Package Conrol](http://wbond.net/sublime_packages/package_control)

Removed py-appscript dependency.