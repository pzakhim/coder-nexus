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
    const prompts = [];  // modal questions; `answer` is what the user clicks
    const state = { answer: undefined };
    const vscode = {
        commands: { registerCommand: (name, fn) => { commands.set(name, fn); return {}; } },
        workspace: { workspaceFolders: [{ uri: { fsPath: workspace } }] },
        window: {
            showErrorMessage: text => errors.push(text),
            showInformationMessage: () => {},
            showWarningMessage: (text, options) => {
                if (options && options.modal) {
                    prompts.push(text);
                    return Promise.resolve(state.answer);
                }
                return Promise.resolve(undefined);
            },
        },
    };
    const sandbox = {
        module: { exports: {} }, console,
        require: name => name === 'vscode' ? vscode : name === 'os' ? { homedir: () => home } : require(name),
    };
    vm.runInNewContext(source, sandbox, { filename: 'extension.js' });
    sandbox.module.exports.activate({ extensionPath, subscriptions: [] });
    return { commands, errors, prompts, state };
}

for (const [command, stack] of [
    ['installWorkspaceFlutter', 'flutter'],
    ['installWorkspaceBE', 'backend'],
]) {
    test(`${command} projects the canonical handshake, a valid manifest and stack.json`, async () => {
        const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-install-'));
        try {
            const workspace = path.join(temp, 'workspace');
            const { commands, errors } = host(workspace, path.join(temp, 'home'));
            assert.equal(await commands.get(`coder-nexus.${command}`)(), true);
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

test('a different pack replaces the installed one only after the user confirms; the same pack refreshes', async () => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-replace-'));
    try {
        const workspace = path.join(temp, 'workspace');
        fs.mkdirSync(path.join(workspace, 'apps/mobile'), { recursive: true });
        fs.writeFileSync(path.join(workspace, 'apps/mobile/pubspec.yaml'), 'name: mobile\n');
        fs.mkdirSync(path.join(workspace, 'services/api'), { recursive: true });
        fs.writeFileSync(path.join(workspace, 'services/api/pyproject.toml'), '[project]\nname = "api"\n');
        fs.mkdirSync(path.join(workspace, '.agents/plugins/coder-nexus-fe'), { recursive: true });
        const { commands, errors, prompts, state } = host(workspace, path.join(temp, 'home'));
        const skillsDir = path.join(workspace, '.agents/plugins/coder-nexus/skills');
        const stackOf = () => JSON.parse(fs.readFileSync(path.join(workspace, '.agents/stack.json'), 'utf8'))
            .packs.map(p => [p.stack, p.paths]);

        assert.equal(await commands.get('coder-nexus.installWorkspaceFlutter')(), true);
        assert.deepEqual(stackOf(), [['flutter', ['apps/mobile']]]);
        assert.ok(!fs.existsSync(path.join(workspace, '.agents/plugins/coder-nexus-fe')), 'pre-2.8 plugins are removed');

        // Same pack: refresh without asking.
        assert.equal(await commands.get('coder-nexus.installWorkspaceFE')(), true);
        assert.deepEqual(prompts, []);
        assert.deepEqual(stackOf(), [['flutter', ['apps/mobile']]]);

        // Different pack, dialog dismissed: nothing changes.
        assert.equal(await commands.get('coder-nexus.installWorkspaceBE')(), false);
        assert.equal(prompts.length, 1);
        assert.match(prompts[0], /Replace it with/);
        assert.deepEqual(stackOf(), [['flutter', ['apps/mobile']]]);
        assert.ok(fs.readdirSync(skillsDir).includes('flutter-core-usage'));

        // Different pack, user confirms: replaced, never merged.
        state.answer = 'Replace';
        assert.equal(await commands.get('coder-nexus.installWorkspaceBE')(), true);
        assert.equal(prompts.length, 2);
        assert.deepEqual(errors, []);
        assert.deepEqual(stackOf(), [['backend', ['services/api']]]);
        const skills = fs.readdirSync(skillsDir);
        assert.ok(skills.includes('backend-api-contracts'));
        assert.ok(!skills.some(name => name.startsWith('flutter-')), skills.join(','));
        const writer = fs.readFileSync(path.join(workspace, '.agents/agents/code_writer.md'), 'utf8');
        assert.ok(writer.includes('## Backend rules') && !writer.includes('## Flutter rules'));
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
        fs.mkdirSync(path.join(temp, 'api'), { recursive: true });
        fs.writeFileSync(path.join(temp, 'api/pyproject.toml'), '[project]\nname = "api"\n');
        // Frappe was removed in 3.2.0: its markers no longer select a pack.
        fs.mkdirSync(path.join(temp, 'desk'), { recursive: true });
        fs.writeFileSync(path.join(temp, 'desk/package.json'), '{"dependencies":{"frappe-ui":"1"}}');
        fs.writeFileSync(path.join(temp, 'desk/hooks.py'), '');
        assert.deepEqual(JSON.parse(JSON.stringify(detectPacks(temp))), { flutter: ['.'], backend: ['api'] });
    } finally {
        fs.rmSync(temp, { recursive: true, force: true });
    }
});

test('missing projection fails before replacing a workspace projection', async () => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'nexus-install-'));
    try {
        const workspace = path.join(temp, 'workspace');
        const installed = path.join(workspace, '.agents/plugins/coder-nexus');
        fs.mkdirSync(installed, { recursive: true });
        fs.writeFileSync(path.join(installed, 'existing.txt'), 'preserve');
        const extensionPath = path.join(temp, 'extension');
        fs.mkdirSync(path.join(extensionPath, 'plugins/coder-nexus-fe'), { recursive: true });
        const { commands, errors } = host(workspace, path.join(temp, 'home'), extensionPath);
        assert.equal(await commands.get('coder-nexus.installWorkspaceFlutter')(), false);
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
