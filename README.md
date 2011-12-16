#TestChooser
A Sublime Text 2 plugin for quickly executing an RSpec command in [iTerm](http://iterm.sourceforge.net/).

## What It Does
It first checks the current file to see that it is either a "feature" or "spec" file. If so, it read the file looking for "it", "describe", "context" or "scenario" keywords that are at the beginning of a line.

It then displays a those lines found for you to choose from. Once you select an item from the list and click "Run", the test is executed in [iTerm](http://iterm.sourceforge.net/).

On each successive run of the plugin, the previously chosen command will automatically be selected for convenience.

## Instructions
#### Install py-appscript
Sublime Text 2 uses its own Python and its version is 2.6. OS X comes with 2.7 so we need to install appscript with the same version as Sublime is using.

`sudo easy_install-2.6 appscript`

This will create an .egg file in /Library/Python/2.6/site-packages

In Sublime, choose "Preferences"->"Browse Packages"

Copy the .egg file into the "Installed Packages" folder.

#### This Plugin
Next, add test_chooser.py to the "Packages/User" folder.

#### Key Binding
Add this line to the User key bindings file. Change the key bindings to your liking.

This one uses a two-key combination. The "super" is the "command" key on a Mac.

`{ "keys": ["super+t", "super+y"], "command": "test_chooser" }`

## ToDo
Make this a full package plugin.


## License
BSD