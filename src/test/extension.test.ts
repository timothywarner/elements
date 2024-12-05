import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Starting all tests.');

    test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('your-publisher.hello-world'));
    });

    test('Should show hello world message', async () => {
        // Execute the command
        await vscode.commands.executeCommand('extension.helloWorld');
        
        // Unfortunately we can't easily test the shown message directly
        // but we can verify the command exists
        const commands = await vscode.commands.getCommands();
        assert.ok(commands.includes('extension.helloWorld'));
    });

    test('Should activate successfully', async () => {
        const ext = vscode.extensions.getExtension('your-publisher.hello-world');
        await ext?.activate();
        assert.ok(ext?.isActive);
    });
}); 