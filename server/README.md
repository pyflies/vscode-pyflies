# vscode-pyflies Language Server

vscode-pyflies Language Server contains all logic for providing features like:

- _Code completion_
- _Error reporting_
- _Quick fix for typos_
- _Find all refernces_
- _Go to definition_

The server uses  _[pygls](https://github.com/openlawlibrary/pygls)_ to expose all functionalities over
_[Language Server Protocol](https://microsoft.github.io/language-server-protocol/specification)_.