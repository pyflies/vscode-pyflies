// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	var mdTableExtension = vscode.extensions.getExtension('TakumiI.markdowntable');

	if (mdTableExtension !== undefined) {
		if (mdTableExtension.isActive === false) {
			mdTableExtension.activate().then(
				function () {
					vscode.window.showInformationMessage("Markdown Table extension activated");
				},
				function () {
					vscode.window.showErrorMessage("Markdown Table activation failed");
				}
			);
		}
	} else {
		vscode.window.showErrorMessage("Markdown Table not found!");
	}
}

// this method is called when your extension is deactivated
export function deactivate() {
}
