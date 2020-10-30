#!/bin/sh
# Build extension and run Code and install the extension in a clean environment

./build.sh
rm -fr code-extensions/*
code --extensions-dir code-extensions --install-extension vscode-pyflies-0.0.1.vsix
code --extensions-dir code-extensions
