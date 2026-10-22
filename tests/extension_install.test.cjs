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

for (const [command, stack] of [
    ['installWorkspaceFlutter', 'flutter'],
    ['installWorkspaceFrappe', 'frappe'],
    ['installWorkspaceBE', 'backend'],
]) {
    test(`${command} projects the canonical handshake, a valid manifest and stack.json`, () => {
        const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-install-'));
        try {
            const workspace = path.join(temp, 'workspace');
            const { commands, errors } = host(workspace, path.join(temp, 'home'));
            commands.get(`coder-nexus.${command}`)();
            assert.deepEqual(errors, []);
            const installed = path.join(workspace, '.agents', 'plugins', 'coder-nexus');
            const protocol = 'shared_contracts/api_handshake_protocol.md';
            assert.equal(fs.readFileSync(path.join(installed, protocol), 'utf8'),
                fs.readFileSync(path.join(root, 'plugins', protocol), 'utf8'));
            const manifest = JSON.parse(fs.readFileSync(path.join(installed, 'bundle_manifest.json'), 'utf8'));
            assert.ok(manifest.required_resources.includes(protocol));
            for (const resource of manifest.required_resources) {
                assert.ok(fs.statSync(path.join(installed, resource)).isFile(), resource);
            }
            if (stack === 'flutter') {
                for (const relative of ['skills/work-item-contract/SKILL.md', 'rules/clean_architecture_rules.md']) {
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
            const stackFile = JSON.parse(fs.readFileSync(path.join(workspace, '.agents/stack.json'), 'utf8'));
            assert.deepEqual(stackFile.packs.map(p => p.stack), [stack]);
            assert.deepEqual(stackFile.packs[0].paths, ['.']);
        } finally {
            fs.rmSync(temp, { recursive: true, force: true });
        }
    });
}

test('adding a pack keeps the installed ones and removes the pre-2.8 plugins', () => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-multi-'));
    try {
        const workspace = path.join(temp, 'workspace');
        fs.mkdirSync(path.join(workspace, 'apps/mobile'), { recursive: true });
        fs.writeFileSync(path.join(workspace, 'apps/mobile/pubspec.yaml'), 'name: mobile\n');
        fs.mkdirSync(path.join(workspace, 'services/api'), { recursive: true });
        fs.writeFileSync(path.join(workspace, 'services/api/pyproject.toml'), '[project]\nname = "api"\n');
        fs.mkdirSync(path.join(workspace, '.agents/plugins/coder-nexus-fe'), { recursive: true });
        const { commands, errors } = host(workspace, path.join(temp, 'home'));
        commands.get('coder-nexus.installWorkspaceFlutter')();
        commands.get('coder-nexus.installWorkspaceBE')();
        assert.deepEqual(errors, []);
        const stackFile = JSON.parse(fs.readFileSync(path.join(workspace, '.agents/stack.json'), 'utf8'));
        assert.deepEqual(stackFile.packs.map(p => [p.stack, p.paths]), [['backend', ['services/api']], ['flutter', ['apps/mobile']]]);
        const skills = fs.readdirSync(path.join(workspace, '.agents/plugins/coder-nexus/skills'));
        assert.ok(skills.includes('flutter-core-usage') && skills.includes('backend-api-contracts'));
        assert.ok(!fs.existsSync(path.join(workspace, '.agents/plugins/coder-nexus-fe')));
        const writer = fs.readFileSync(path.join(workspace, '.agents/agents/code_writer.md'), 'utf8');
        assert.ok(writer.includes('## Stack rules') && writer.includes('## Backend rules') && writer.includes('## Flutter rules'));
    } finally {
        fs.rmSync(temp, { recursive: true, force: true });
    }
});

test('detectPacks finds monorepo project roots but not platform shells', () => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-detect-'));
    try {
        const sandbox = { module: { exports: {} }, console, require: name => name === 'vscode' ? {} : require(name) };
        vm.runInNewContext(source, sandbox, { filename: 'extension.js' });
        const { detectPacks } = sandbox.module.exports;
        fs.writeFileSync(path.join(temp, 'pubspec.yaml'), 'name: app\n');
        fs.mkdirSync(path.join(temp, 'android'), { recursive: true });
        fs.writeFileSync(path.join(temp, 'android/build.gradle'), '');
        fs.mkdirSync(path.join(temp, 'desk'), { recursive: true });
        fs.writeFileSync(path.join(temp, 'desk/package.json'), '{"dependencies":{"frappe-ui":"1"}}');
        assert.deepEqual(JSON.parse(JSON.stringify(detectPacks(temp))), { flutter: ['.'], frappe: ['desk'] });
    } finally {
        fs.rmSync(temp, { recursive: true, force: true });
    }
});

test('missing projection fails before replacing a workspace projection', () => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-install-'));
    try {
        const workspace = path.join(temp, 'workspace');
        const installed = path.join(workspace, '.agents/plugins/coder-nexus');
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
