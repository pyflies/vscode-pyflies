// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as net from "net";
import * as path from "path";

import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind
} from 'vscode-languageclient/node';

let client: LanguageClient;

function getClientOptions(): LanguageClientOptions {
    return {
        // Register the server for plain text documents
        documentSelector: ["*"],
        outputChannelName: "pyFlies",
    };
}

function isStartedInDebugMode(): boolean {
    return process.env.VSCODE_DEBUG_MODE === "true";
}

function startLangServerTCP(addr: number): LanguageClient {
    const serverOptions: ServerOptions = () => {
        return new Promise((resolve /*, reject */) => {
            const clientSocket = new net.Socket();
            clientSocket.connect(addr, "127.0.0.1", () => {
                resolve({
                    reader: clientSocket,
                    writer: clientSocket,
                });
            });
        });
    };

    // 'pyFlies LS (port ${addr})'
    return new LanguageClient(
        `tcp lang server (port ${addr})`,
        serverOptions,
        getClientOptions()
    );
}

function startLangServer(
    command: string,
    args: string[],
    cwd: string
): LanguageClient {
    const serverOptions: ServerOptions = {
        args,
        command,
        options: { cwd },
    };

    return new LanguageClient(command, serverOptions, getClientOptions());
}


// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
    if (isStartedInDebugMode()){
        // Development - Run the server manually
        client = startLangServerTCP(2087);
    } else {
        // Production - Client is going to run the server (for use within `.vsix` package)
        const cwd = path.join(__dirname, "..", "..");
        const pythonPath = vscode.workspace
            .getConfiguration("python")
            .get<string>("pythonPath");

        if (!pythonPath) {
            throw new Error("`python.pythonPath` is not set");
        }

        client = startLangServer(pythonPath, ["-m", "server"], cwd);
    }

    context.subscriptions.push(client.start());

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
export function deactivate(): Thenable<void> {
    return client ? client.stop() : Promise.resolve();
}
