[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog


### Version 5.6.0

- Using novelibre's word counter strategy.

API: 5.30
Based on novelibre 5.30.0


### Version 5.5.0

- Added/changed icons.

API: 5.27
Based on novelibre 5.29.7


### Version 5.4.2

- Fixed a bug where an unhandled exception is raised when deleting a section which was previously edited. 

Update for novelibre 5.27.

- Disabling the novelibre "Section" > "Edit" menu entry on lock.
- Processing Section.viewpoint.

API: 5.27
Based on novelibre 5.27.3


### Version 5.3.0

- Refactored the code for better maintainability:
  Reintegrated the controller mixin class into the view class.

API: 5.17
Based on novelibre 5.26.1

### Version 5.2.3

- Prevent flickering when opening the window.

API: 5.17
Based on novelibre 5.24.3

### Version 5.2.2

- Making sure that the editor window position doesn't change when reopening.

API: 5.17
Based on novelibre 5.24.3

### Version 5.2.1

- Updated the messaging.

API: 5.17
Based on novelibre 5.17.3

### Version 5.1.1

- Made the XML tag color configurable.

API: 5.0
Based on novelibre 5.1.3

### Version 5.1.0

Colorizing XML tags.

API: 5.0
Based on novelibre 5.1.3

### Version 5.0.5

Bugfix:
- No longer try saving editor changes although the corresponding section is deleted.

Library update:
- Refactor the code for better maintainability.

API: 5.0
Based on novelibre 5.0.28

### Version 4.6.2

- Change the message window title.
- Simplify the word counting algorithm.

Refactor the code for better maintainability:

- Replace global constants with class constants.
- Restore the names of settings and options from version 4.5.3.

Compatibility: novelibre 4.6 API
Based on novxlib 5.0.0

### Version 4.6.1

- Closing an editor window when the corresponding section is deleted.
- Fix a regression from version 4.5.4 where the geometry information is lost on closing the editor window.

Compatibility: novelibre 4.6 API
Based on novxlib 4.7.1

### Version 4.6.0

- Reading the editor color settings from the configuration file.

Compatibility: novelibre 4.6 API
Based on novxlib 4.7.1

### Version 4.5.4

- Prevent the same section from being loaded in more than one editor window at the same time. 

Compatibility: novelibre 4.6 API
Based on novxlib 4.7.1

### Version 4.5.3

Refactor:
- Move platform selector and keyboard settings into the new platform_settings module.

Compatibility: novelibre 4.6 API
Based on novxlib 4.6.4

### Version 4.5.2

- Refactor the event bindings.

Compatibility: novelibre 4.6 API
Based on novxlib 4.6.4

### Version 4.5.1

- Translate more accelerators.
- Provide shortcuts and key bindings for Mac OS.
- Automatically resize the setup window.

Compatibility: novelibre 4.6 API
Based on novxlib 4.6.4

### Version 4.5.0

- Provide shortcuts and key bindings for Mac OS.

Compatibility: novelibre 4.6 API
Based on novxlib 4.6.3

### Version 4.4.3

- Refactor: Change import order for a quick start.

Compatibility: novelibre 4.6 API
Based on novxlib 4.6.3

### Version 4.4.2

- Text box discarding illegal characters.

Compatibility: novelibre 4.6 API
Based on novxlib 4.6.2

### Version 4.4.1

- Refactor for future Python versions.

Compatibility: novelibre 4.6 API

### Version 4.4.0

- Provide context sensitive help via F1 key.

Compatibility: novelibre 4.6 API

### Version 4.3.0

- Provide radiobuttons for the color setting.
- Provide a checkbutton for the word count setting.

Compatibility: novelibre 4.3 API

### Version 4.2.3

- Handle minimized window.

Compatibility: novelibre 4.3 API

### Version 4.2.2

- Fix a regression from version 4.0 (novxlib API change not considered) 
  where section creation or splitting raises an exception.

Compatibility: novelibre 4.3 API

### Version 4.2.1

- Refactor the code for future API update,
  making the prefs argument of the Plugin.install() method optional.

Compatibility: novelibre 4.3 API

### Version 4.2.0

- Refactor the code for better maintainability.

Compatibility: novelibre 4.3 API

### Version 4.1.0

- Use a novelibre service factory method instead of importing the novxlib configuration module.

Compatibility: novelibre 4.1 API

### Version 3.0.2

- Fix a bug where the main status bar is blank after rewriting modified section content. 

Compatibility: novelibre 3.0 API

### Version 3.0.1

- Fix a bug where the keybindings are changed for the Text class instead of the section editor's TextBox instance. 

Compatibility: novelibre 3.0 API

### Version 3.0.0

- Refactor the code for v3.0 API.
- Enable the online help in German.

Compatibility: novelibre 3.0 API

### Version 2.1.3

- Button: Replace "Exit" with "Close". 

Compatibility: noveltree 2.1 API

### Version 2.1.2

- Under Windows, exit with Alt-F4 instead of Ctrl-Q.

Compatibility: noveltree 2.1 API

### Version 2.1.1

- Bugfix: Before creating a new section by splitting, check the split content for XML errors.

Compatibility: noveltree 2.1 API

### Version 2.1.0

- Update for "novelibre".

Compatibility: noveltree 2.1 API

### Version 2.0.0

Preparations for renaming the application:
- Refactor the code for v2.0 API.
- Change the installation directory in the setup script.

Compatibility: noveltree 2.0 API

### Version 1.1.0

- Re-structure the website; adjust links.

Compatibility: noveltree 1.8 API

### Version 1.0.2

- Switch the online help to https://peter88213.github.io/noveltree-help/.

Compatibility: noveltree 1.0 API

### Version 1.0.1

- Fix the plugin API version constant.

Compatibility: noveltree 1.0 API

### Version 1.0.0

- Release under the GPLv3 license.

Compatibility: noveltree 1.0 API