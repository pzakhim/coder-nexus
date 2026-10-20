const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

const root = path.resolve(__dirname, '..');

// The extension only copies prebuilt projections; build them from source first.
const built = require('node:child_process').spawnSync(
    process.env.PYTHON || 'python3', ['-m', 'coder_nexus.plugin_build'],
    { cwd: root, env: { ...process.env, PYTHONPATH: path.join(root, 'src') }, encoding: 'utf8' },
);
if (built.status !== 0) throw new Error(`plugin_build failed: ${built.stderr}`);
const source = fs.readFileSync(path.join(root, 'extension.js'), 'utf8');

function host(workspace, home, extensionPath = root) {
    const commands = new Map();
    const errors = [];
    const vscode = {
        commands: { registerCommand: (name, fn) => { commands.set(name, fn); return {}; } },
        workspace: { workspaceFolders: [{ uri: { fsPath: workspace } }] },
        window: {
            showErrorMessage: text => errors.push(text),
            showInformationMessage: () => {},
        },
    };
    const sandbox = {
        module: { exports: {} }, console,
        require: name => name === 'vscode' ? vscode : name === 'os' ? { homedir: () => home } : require(name),
    };
    vm.runInNewContext(source, sandbox, { filename: 'extension.js' });
    sandbox.module.exports.activate({ extensionPath, subscriptions: [] });
    return { commands, errors };
}

for (const [command, plugin, framework] of [
    ['installWorkspaceFlutter', 'coder-nexus-fe', 'flutter'],
    ['installWorkspaceFrappe', 'coder-nexus-fe', 'frappe'],
    ['installWorkspaceBE', 'coder-nexus-be', null],
]) {
    test(`${command} projects the canonical handshake and valid manifest`, () => {
        const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-install-'));
        try {
            const workspace = path.join(temp, 'workspace');
            const { commands, errors } = host(workspace, path.join(temp, 'home'));
            commands.get(`coder-nexus.${command}`)();
            assert.deepEqual(errors, []);
            const installed = path.join(workspace, '.agents', 'plugins', plugin);
            const protocol = 'shared_contracts/api_handshake_protocol.md';
            assert.equal(fs.readFileSync(path.join(installed, protocol), 'utf8'),
                fs.readFileSync(path.join(root, 'plugins', protocol), 'utf8'));
            const manifest = JSON.parse(fs.readFileSync(path.join(installed, 'bundle_manifest.json'), 'utf8'));
            assert.ok(manifest.required_resources.includes(protocol));
            for (const resource of manifest.required_resources) {
                assert.ok(fs.statSync(path.join(installed, resource)).isFile(), resource);
            }
            if (framework === 'flutter') {
                for (const relative of ['skills/work-items/SKILL.md', 'rules/clean_architecture_rules.md']) {
                    const document = path.join(installed, relative);
                    for (const [, link] of fs.readFileSync(document, 'utf8').matchAll(/\]\(([^)]+)\)/g)) {
                        assert.ok(fs.statSync(path.resolve(path.dirname(document), link)).isFile(), link);
                    }
                }
                for (const ref of ['01_profile_imespro.md', '02_profile_external_structured.md', '03_profile_external_standard.md']) {
                    assert.ok(fs.existsSync(path.join(installed, 'skills/flutter-core-usage/references', ref)));
                }
            }
            assert.ok(fs.existsSync(path.join(workspace, '.agents/agents/code_reviewer.md')));
            assert.ok(!fs.existsSync(path.join(installed, 'agents')), 'agents must not be duplicated inside the plugin');
            const stamp = JSON.parse(fs.readFileSync(path.join(installed, 'installed_version.json'), 'utf8'));
            assert.equal(stamp.plugin_version, manifest.plugin_version);
        } finally {
            fs.rmSync(temp, { recursive: true, force: true });
        }
    });
}

test('missing shared protocol fails before replacing a workspace projection', () => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-install-'));
    try {
        const workspace = path.join(temp, 'workspace');
        const installed = path.join(workspace, '.agents/plugins/coder-nexus-fe');
        fs.mkdirSync(installed, { recursive: true });
        fs.writeFileSync(path.join(installed, 'existing.txt'), 'preserve');
        const extensionPath = path.join(temp, 'extension');
        fs.mkdirSync(path.join(extensionPath, 'plugins/coder-nexus-fe'), { recursive: true });
        const { commands, errors } = host(workspace, path.join(temp, 'home'), extensionPath);
        commands.get('coder-nexus.installWorkspaceFlutter')();
        assert.equal(errors.length, 1);
        assert.equal(fs.readFileSync(path.join(installed, 'existing.txt'), 'utf8'), 'preserve');
    } finally {
        fs.rmSync(temp, { recursive: true, force: true });
    }
});

test('extension registers quickActions and checkHealth commands', () => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-cmds-'));
    try {
        const workspace = path.join(temp, 'workspace');
        const { commands } = host(workspace, path.join(temp, 'home'));
        assert.ok(commands.has('coder-nexus.quickActions'));
        assert.ok(commands.has('coder-nexus.checkHealth'));
        assert.ok(commands.has('coder-nexus.installCli'));
    } finally {
        fs.rmSync(temp, { recursive: true, force: true });
    }
});
