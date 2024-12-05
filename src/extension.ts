import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension "hello-world" is now active!');

    let disposable = vscode.commands.registerCommand('extension.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World from your extension!');
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {} 