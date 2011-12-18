#TestChooser
A Sublime Text 2 plugin for quickly executing a RSpec & Cucumber commands in [iTerm](http://iterm.sourceforge.net/) or Apple's Terminal.

Since this plugin uses [py-appscript](http://appscript.sourceforge.net/py-appscript/index.html), an AppleScript bridge for Python, it is only usable on OS X.

## Description
It first checks the current file to see that it is either a "feature" or "spec" file. If so, it reads the file looking for "it", "describe", "context" or "scenario" keywords that are at the beginning of a line.

It then displays those lines for you to choose from. Once you select an item from the list and click "Run", the test is executed in [iTerm](http://iterm.sourceforge.net/) or Apple's Terminal, whichever you have set in preferences.

On each successive run of the plugin, the previously chosen command will automatically be selected for convenience.

## Instructions
#### Install py-appscript
Sublime Text 2 uses its own Python and its version is 2.6. We need to install appscript with the same version that Sublime is using.

`sudo easy_install-2.6 appscript`

This will create "appscript-1.0.0-py2.6-macosx-10.7-intel.egg" file in /Library/Python/2.6/site-packages

In Sublime, choose "Preferences"->"Browse Packages"

Copy the .egg file into the "Installed Packages" folder and restart Sublime.

#### This Plugin
Install this plugin using [Package Control](http://wbond.net/sublime_packages/package_control), a
package manager for Sublime.

#### Key Bindings
There is a menu item to access the key binding for TestChooser.

"Preferences"->"Package Settings"->"TestChooser"->"Key Bindings - User"

This one uses a two-key combination. The "super" is the "command" key on a Mac.

`{ "keys": ["super+y", "super+y"], "command": "test_chooser" }`


#### Settings
There are two settings available.

"Preferences"->"Package Settings"->"TestChooser"->"Settings - User"

This defaults to iTerm but you can also choose Apple's Terminal by using the word "Terminal"

`"terminal": "iTerm"`

The search terms used when searching the RSpec and Cucumber files.

`"search_terms": ["it", "describe", "context", "Scenario"]`


## License

Read the license text file included in this package... but it's MIT.

## Changelog

Changed the original plugin to now use [Package Conrol](http://wbond.net/sublime_packages/package_control)