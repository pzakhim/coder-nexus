const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const os = require('os');
const cp = require('child_process');

/**
 * Recursively copy folder contents from source to destination.
 */
function copyFolderSync(from, to) {
    if (!fs.existsSync(to)) {
        fs.mkdirSync(to, { recursive: true });
    }
    const entries = fs.readdirSync(from, { withFileTypes: true });
    for (const entry of entries) {
        const srcPath = path.join(from, entry.name);
        const destPath = path.join(to, entry.name);
        if (entry.isDirectory()) {
            copyFolderSync(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    }
}

function extensionVersion(context) {
    try {
        return JSON.parse(fs.readFileSync(path.join(context.extensionPath, 'package.json'), 'utf8')).version || 'UNKNOWN';
    } catch (_) {
        return 'UNKNOWN';
    }
}

function bundledPluginVersion(context) {
    // plugin_version and the extension version are kept identical by scripts/sync_version.py.
    const version = extensionVersion(context);
    return version === 'UNKNOWN' ? null : version;
}

function installedPluginVersion(pluginDir) {
    for (const file of ['installed_version.json', 'bundle_manifest.json']) {
        try {
            const version = JSON.parse(fs.readFileSync(path.join(pluginDir, file), 'utf8')).plugin_version;
            if (version) return version;
        } catch (_) {}
    }
    return null;
}

const BE_SIGNATURES = [
    'go.mod', 'pom.xml', 'build.gradle', 'build.gradle.kts',
    'requirements.txt', 'pyproject.toml', 'Cargo.toml',
    'Dockerfile', 'docker-compose.yml'
];
// Folders that never hold a separate project root (platform shells, build output, tooling).
const SCAN_SKIP = new Set([
    'node_modules', '.git', '.agents', '.superpowers', '.dart_tool', '.idea', '.vscode', 'build', 'dist',
    'ios', 'android', 'macos', 'linux', 'windows', 'web', 'test', 'tests', 'assets', 'docs',
    'venv', '.venv', '__pycache__', 'coverage', 'target', 'vendor'
]);

/**
 * Detect the stack pack ('flutter', 'frappe' or 'backend') whose signature is in `dir`, else null.
 */
function detectStackAt(dir) {
    if (fs.existsSync(path.join(dir, 'pubspec.yaml'))) return 'flutter';
    const pkgPath = path.join(dir, 'package.json');
    if (fs.existsSync(pkgPath)) {
        try {
            if (fs.readFileSync(pkgPath, 'utf8').includes('frappe-ui')) return 'frappe';
        } catch (_) {}
    }
    if (fs.existsSync(path.join(dir, 'hooks.py'))) return 'frappe';
    if (BE_SIGNATURES.some(sig => fs.existsSync(path.join(dir, sig)))) return 'backend';
    return null;
}

/**
 * Find project roots in the workspace (the root and up to two folder levels below it).
 * Returns { stack: [relative paths] }; a folder that is a project root is not scanned further.
 */
function detectPacks(workspacePath) {
    const found = {};
    const visit = (dir, rel, depth) => {
        const stack = detectStackAt(dir);
        if (stack) {
            (found[stack] = found[stack] || []).push(rel || '.');
            if (rel) return;
        }
        if (depth >= 2) return;
        let entries = [];
        try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch (_) { return; }
        for (const entry of entries) {
            if (!entry.isDirectory() || SCAN_SKIP.has(entry.name) || entry.name.startsWith('.')) continue;
            visit(path.join(dir, entry.name), rel ? `${rel}/${entry.name}` : entry.name, depth + 1);
        }
    };
    visit(workspacePath, '', 0);
    return found;
}

/**
 * Backward-compatible single answer: 'flutter', 'frappe' or 'be' for the workspace root.
 */
function detectProjectRole(workspacePath) {
    const stack = detectStackAt(workspacePath);
    return stack === 'backend' ? 'be' : stack || 'flutter';
}

function isRecognizedWorkspace(workspacePath) {
    return Object.keys(detectPacks(workspacePath)).length > 0;
}

/**
 * Copy a projection built by `python -m coder_nexus.plugin_build` (plugins/dist/<layout>-<packs>).
 * All composition and filtering happens at build time; this only replaces the managed paths.
 */
function applyProjection(projectionDir, destRoot) {
    const spec = JSON.parse(fs.readFileSync(path.join(projectionDir, 'projection.json'), 'utf8'));
    if (!Array.isArray(spec.managed) || spec.managed.length === 0) {
        throw new Error(`Invalid projection: ${projectionDir}`);
    }
    for (const rel of [...(spec.remove || []), ...spec.managed]) {
        fs.rmSync(path.join(destRoot, rel), { recursive: true, force: true });
    }
    for (const rel of spec.managed) {
        const src = path.join(projectionDir, 'files', rel);
        const dest = path.join(destRoot, rel);
        if (fs.statSync(src).isDirectory()) {
            copyFolderSync(src, dest);
        } else {
            fs.mkdirSync(path.dirname(dest), { recursive: true });
            fs.copyFileSync(src, dest);
        }
    }
    return spec;
}

function bundledPacks(context) {
    try {
        return JSON.parse(fs.readFileSync(path.join(context.extensionPath, 'plugins', 'dist', 'packs.json'), 'utf8')).packs || [];
    } catch (_) {
        return [];
    }
}

function readStackFile(workspacePath) {
    try {
        return JSON.parse(fs.readFileSync(path.join(workspacePath, '.agents', 'stack.json'), 'utf8'));
    } catch (_) {
        return { packs: [] };
    }
}

function installedPacks(workspacePath) {
    return (readStackFile(workspacePath).packs || []).map(pack => pack.stack).filter(Boolean);
}

/**
 * Record the installed packs and the workspace paths each owns (same schema as the CLI).
 */
function writeStackFile(workspacePath, spec, paths) {
    const data = {
        plugin_version: spec.plugin_version || 'UNKNOWN',
        packs: (spec.packs || []).map(pack => ({ ...pack, paths: (paths[pack.stack] && paths[pack.stack].length) ? paths[pack.stack] : ['.'] })),
    };
    const file = path.join(workspacePath, '.agents', 'stack.json');
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n', 'utf8');
    return data;
}

/**
 * Paths for each pack: keep what stack.json already records, else what detection found.
 */
function packPaths(workspacePath, packs) {
    const recorded = {};
    for (const pack of readStackFile(workspacePath).packs || []) recorded[pack.stack] = pack.paths;
    const detected = detectPacks(workspacePath);
    const paths = {};
    for (const stack of packs) paths[stack] = recorded[stack] || detected[stack] || ['.'];
    return paths;
}

/**
 * Install or update the Coder Nexus plugin from its prebuilt projection.
 * Workspace: `packs` is the full set to install (any combination). Global: exactly one pack.
 */
function installAntigravityPlugin(context, targetWorkspace = null, silent = false, packs = ['flutter']) {
    const layout = targetWorkspace ? 'workspace' : 'global';
    const selected = [...new Set(packs)].sort();
    const projectionDir = path.join(context.extensionPath, 'plugins', 'dist', `${layout}-${selected.join('+')}`);
    if (!selected.length || !fs.existsSync(path.join(projectionDir, 'projection.json'))) {
        if (!silent) {
            vscode.window.showErrorMessage(`Coder Nexus plugin assets for ${selected.join(' + ') || 'no pack'} (${layout}) not found inside extension path.`);
        }
        return false;
    }

    try {
        const destRoot = targetWorkspace || path.join(os.homedir(), '.gemini', 'config', 'plugins');
        const paths = targetWorkspace ? packPaths(targetWorkspace, selected) : {};
        const spec = applyProjection(projectionDir, destRoot);
        const destPath = path.join(destRoot, spec.managed[0]);
        if (targetWorkspace) writeStackFile(targetWorkspace, spec, paths);

        // GUI-launched IDEs may not have ~/.local/bin in PATH; point MCP at the absolute CLI when present.
        const mcpConfigPath = path.join(destPath, 'mcp_config.json');
        if (fs.existsSync(mcpConfigPath) && fs.existsSync(localCliPath())) {
            const mcp = JSON.parse(fs.readFileSync(mcpConfigPath, 'utf8'));
            if (mcp.mcpServers && mcp.mcpServers['coder-nexus']) {
                mcp.mcpServers['coder-nexus'].command = localCliPath();
                fs.writeFileSync(mcpConfigPath, JSON.stringify(mcp, null, 2) + '\n', 'utf8');
            }
        }

        // Ensure bundled Ponytail plugin is installed if not already present on host/workspace
        ensurePonytailPlugin(context, targetWorkspace, silent);

        const placeholders = Object.entries(spec.stubs || {}).filter(([, kind]) => kind === 'blocked').map(([name]) => name);
        if (!silent && placeholders.length && typeof vscode.window.showWarningMessage === 'function') {
            const preview = (spec.packs || []).filter(p => p.status === 'preview').map(p => p.title).join(', ');
            vscode.window.showWarningMessage(
                `Coder Nexus: ${preview} ${preview.includes(',') ? 'are preview packs' : 'is a preview pack'}. ${placeholders.length} skills are placeholders (${placeholders.join(', ')}); agents stop with BLOCKED at those steps instead of guessing.`
            );
        }

        const label = (spec.packs || []).map(p => p.title).join(' + ');
        if (!silent) {
            const msg = `✅ Coder Nexus synced ${label} to Antigravity (${destPath})`;
            if (vscode.window && typeof vscode.window.showInformationMessage === 'function') {
                const p = vscode.window.showInformationMessage(msg, 'Open Dashboard', 'Check Environment');
                if (p && typeof p.then === 'function') {
                    p.then(choice => {
                        if (choice === 'Open Dashboard') {
                            vscode.commands.executeCommand('coder-nexus.showArchitecture');
                        } else if (choice === 'Check Environment') {
                            vscode.commands.executeCommand('coder-nexus.checkHealth');
                        }
                    });
                }
            }
        }
        return true;
    } catch (err) {
        if (!silent) {
            vscode.window.showErrorMessage(`❌ Failed to sync Coder Nexus (${selected.join(' + ')}): ${err.message}`);
        }
        return false;
    }
}

/**
 * Ensure the bundled Ponytail plugin is installed if not already present.
 */
function ensurePonytailPlugin(context, targetWorkspace = null, silent = true) {
    const ponytailSource = path.join(context.extensionPath, 'plugins', 'ponytail');
    if (!fs.existsSync(ponytailSource)) {
        return;
    }

    const home = os.homedir();
    const globalPonytail = path.join(home, '.gemini', 'config', 'plugins', 'ponytail');
    const wsPonytail = targetWorkspace ? path.join(targetWorkspace, '.agents', 'plugins', 'ponytail') : null;

    const isInstalledGlobally = fs.existsSync(globalPonytail);
    const isInstalledWorkspace = wsPonytail && fs.existsSync(wsPonytail);

    try {
        if (targetWorkspace) {
            if (!isInstalledWorkspace && !isInstalledGlobally) {
                copyFolderSync(ponytailSource, wsPonytail);
                if (!silent) {
                    vscode.window.showInformationMessage(`✅ Bundled Ponytail plugin synced to workspace (${wsPonytail})`);
                }
            }
        } else {
            if (!isInstalledGlobally) {
                copyFolderSync(ponytailSource, globalPonytail);
                if (!silent) {
                    vscode.window.showInformationMessage(`✅ Bundled Ponytail plugin synced globally (${globalPonytail})`);
                }
            }
        }
    } catch (e) {
        console.error('Failed to sync bundled Ponytail plugin:', e);
    }
}

const REPO_URL = 'https://github.com/pzakhim/coder-nexus';
const IS_WIN = path.sep === '\\';

/**
 * Absolute path where `uv tool install` places the CLI (GUI-launched IDEs often miss it in PATH).
 */
function localCliPath() {
    const bin = IS_WIN ? 'coder-nexus.exe' : 'coder-nexus';
    return path.join(os.homedir(), '.local', 'bin', bin);
}

/**
 * Open a terminal that installs uv (if missing) and the CLI pinned to this extension's release tag.
 */
function installCli(context) {
    let version = '';
    try {
        version = JSON.parse(fs.readFileSync(path.join(context.extensionPath, 'package.json'), 'utf8')).version;
    } catch (_) {}
    const source = `git+${REPO_URL}.git${version ? `@v${version}` : ''}`;
    const term = vscode.window.createTerminal('Coder Nexus Setup');
    term.show();
    term.sendText(IS_WIN
        ? `if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" }; $env:Path = "$HOME\\.local\\bin;$env:Path"; uv tool install --force ${source}`
        : `(command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh) && export PATH="$HOME/.local/bin:$PATH" && uv tool install --force ${source}`);
}

/**
 * Check if the coder-nexus CLI is available (PATH or ~/.local/bin).
 */
function checkCliHealth(context, silent = false) {
    return new Promise(resolve => {
        cp.exec('coder-nexus --help', (err) => {
            const ok = !err || fs.existsSync(localCliPath());
            if (ok) {
                if (!silent && vscode.window && typeof vscode.window.showInformationMessage === 'function') {
                    const p = vscode.window.showInformationMessage(
                        '✅ Coder Nexus CLI found. Next: run `coder-nexus setup huly` (optional) and `coder-nexus doctor` in the terminal.',
                        'Update CLI',
                        'Show Architecture'
                    );
                    if (p && typeof p.then === 'function') {
                        p.then(choice => {
                            if (choice === 'Update CLI') installCli(context);
                            else if (choice === 'Show Architecture') vscode.commands.executeCommand('coder-nexus.showArchitecture');
                        });
                    }
                }
                resolve(true);
            } else {
                if (!silent && vscode.window && typeof vscode.window.showWarningMessage === 'function') {
                    const p = vscode.window.showWarningMessage(
                        "⚠️ Coder Nexus CLI ('coder-nexus') is not installed. MCP tools, Huly and Flutter setup need it.",
                        'Install CLI',
                        'View Setup Guide'
                    );
                    if (p && typeof p.then === 'function') {
                        p.then(choice => {
                            if (choice === 'Install CLI') installCli(context);
                            else if (choice === 'View Setup Guide' && vscode.env && typeof vscode.env.openExternal === 'function') {
                                vscode.env.openExternal(vscode.Uri.parse(`${REPO_URL}#quickstart`));
                            }
                        });
                    }
                }
                resolve(false);
            }
        });
    });
}

/**
 * Prompt user to sync when opening a recognized workspace for the first time.
 */
function checkFirstTimeWorkspacePrompt(context) {
    if (!vscode.workspace || !Array.isArray(vscode.workspace.workspaceFolders) || vscode.workspace.workspaceFolders.length === 0) {
        return;
    }
    const wsPath = vscode.workspace.workspaceFolders[0].uri.fsPath;

    // Already synced: offer a re-sync when the projection is older (or uses the pre-2.8 layout)
    const current = path.join(wsPath, '.agents', 'plugins', 'coder-nexus');
    const legacy = ['coder-nexus-fe', 'coder-nexus-be'].map(name => path.join(wsPath, '.agents', 'plugins', name)).find(p => fs.existsSync(p));
    if (fs.existsSync(current) || legacy) {
        warnIfStaleSync(context, fs.existsSync(current) ? current : legacy);
        return;
    }

    if (!isRecognizedWorkspace(wsPath)) {
        return;
    }

    const state = context.workspaceState;
    if (state && typeof state.get === 'function' && state.get('coderNexusPromptDismissed')) {
        return;
    }

    const titles = Object.fromEntries(bundledPacks(context).map(pack => [pack.stack, pack.title]));
    const detected = detectPacks(wsPath);
    const roleLabel = Object.keys(detected).map(stack => titles[stack] || stack).join(' + ');

    if (vscode.window && typeof vscode.window.showInformationMessage === 'function') {
        const p = vscode.window.showInformationMessage(
            `🚀 Coder Nexus: Detected ${roleLabel} in this workspace. Sync AI delivery agents & skills?`,
            'Sync Now',
            'Show Architecture',
            "Don't Ask Again"
        );
        if (p && typeof p.then === 'function') {
            p.then(choice => {
                if (choice === 'Sync Now') {
                    vscode.commands.executeCommand('coder-nexus.installWorkspace');
                } else if (choice === 'Show Architecture') {
                    vscode.commands.executeCommand('coder-nexus.showArchitecture');
                } else if (choice === "Don't Ask Again") {
                    if (state && typeof state.update === 'function') {
                        state.update('coderNexusPromptDismissed', true);
                    }
                }
            });
        }
    }
}

/**
 * Offer a re-sync when the workspace projection is older than the bundled plugin.
 */
function warnIfStaleSync(context, pluginDir) {
    const pluginName = path.basename(pluginDir);
    const installed = installedPluginVersion(pluginDir);
    const bundled = bundledPluginVersion(context);
    if (!bundled || (installed === bundled && pluginName === 'coder-nexus')) return;
    if (!vscode.window || typeof vscode.window.showWarningMessage !== 'function') return;
    const p = vscode.window.showWarningMessage(
        `Coder Nexus: workspace has ${pluginName} ${installed || 'unknown'}, extension ships ${bundled}. Re-sync agents & skills?`,
        'Sync Now'
    );
    if (p && typeof p.then === 'function') {
        p.then(choice => {
            if (choice === 'Sync Now') vscode.commands.executeCommand('coder-nexus.installWorkspace');
        });
    }
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    const cmdGlobal = vscode.commands.registerCommand('coder-nexus.installGlobal', () => {
        installAntigravityPlugin(context, null, false, ['flutter']);
    });

    const currentWorkspace = () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showWarningMessage('No workspace open to sync Coder Nexus plugin.');
            return null;
        }
        return workspaceFolders[0].uri.fsPath;
    };

    const cmdWorkspace = vscode.commands.registerCommand('coder-nexus.installWorkspace', async () => {
        const wsPath = currentWorkspace();
        if (!wsPath) return;
        const detected = detectPacks(wsPath);
        const installed = installedPacks(wsPath);
        const items = bundledPacks(context).map(pack => {
            const found = detected[pack.stack];
            const notes = [];
            if (found) notes.push(`⭐ detected in ${found.join(', ')}`);
            if (installed.includes(pack.stack)) notes.push('installed');
            if (pack.status === 'preview') notes.push('preview');
            return {
                label: pack.title,
                description: notes.join(' · '),
                picked: Boolean(found) || installed.includes(pack.stack),
                stack: pack.stack,
            };
        });
        const choice = await vscode.window.showQuickPick(items, {
            canPickMany: true,
            placeHolder: 'Select the stacks this workspace contains (several for a monorepo)'
        });
        if (choice && choice.length) {
            installAntigravityPlugin(context, wsPath, false, choice.map(item => item.stack));
        }
    });

    // Force commands add one pack to the packs already installed in the workspace.
    const addPack = stack => () => {
        const wsPath = currentWorkspace();
        if (wsPath) installAntigravityPlugin(context, wsPath, false, [...installedPacks(wsPath), stack]);
    };
    const cmdWorkspaceFlutter = vscode.commands.registerCommand('coder-nexus.installWorkspaceFlutter', addPack('flutter'));
    const cmdWorkspaceFrappe = vscode.commands.registerCommand('coder-nexus.installWorkspaceFrappe', addPack('frappe'));
    const cmdWorkspaceBE = vscode.commands.registerCommand('coder-nexus.installWorkspaceBE', addPack('backend'));
    const cmdWorkspaceFE = vscode.commands.registerCommand('coder-nexus.installWorkspaceFE', addPack('flutter'));

    const cmdShowArch = vscode.commands.registerCommand('coder-nexus.showArchitecture', () => {
        const panel = vscode.window.createWebviewPanel(
            'coderNexusArchitecture',
            'Coder Nexus: Multi-Agent Architecture',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );
        const htmlPath = path.join(context.extensionPath, 'media', 'architecture.html');
        if (fs.existsSync(htmlPath)) {
            panel.webview.html = fs.readFileSync(htmlPath, 'utf8');
        } else {
            vscode.window.showErrorMessage('Coder Nexus: architecture.html not found in media folder.');
        }
    });

    const cmdQuickActions = vscode.commands.registerCommand('coder-nexus.quickActions', async () => {
        if (!vscode.window || typeof vscode.window.showQuickPick !== 'function') return;

        const items = [
            {
                label: '$(sync) Sync Stacks to Workspace (Auto-Detect)',
                description: 'Detects Flutter / Frappe / Backend folders (monorepo too) and installs agents & skills',
                action: () => vscode.commands.executeCommand('coder-nexus.installWorkspace')
            },
            {
                label: '$(device-mobile) Add Flutter Pack',
                description: 'Adds Flutter rules & skills to the stacks already installed',
                action: () => vscode.commands.executeCommand('coder-nexus.installWorkspaceFlutter')
            },
            {
                label: '$(server) Add Backend Pack',
                description: 'Adds Backend rules & skills to the stacks already installed (preview)',
                action: () => vscode.commands.executeCommand('coder-nexus.installWorkspaceBE')
            },
            {
                label: '$(graph) Show Architecture Dashboard',
                description: 'Interactive multi-agent delivery flow visualizer',
                action: () => vscode.commands.executeCommand('coder-nexus.showArchitecture')
            },
            {
                label: '$(cloud-download) Install / Update CLI',
                description: 'Installs uv (if missing) and coder-nexus pinned to this extension version',
                action: () => vscode.commands.executeCommand('coder-nexus.installCli')
            },
            {
                label: '$(pulse) Check Environment & CLI (Doctor)',
                description: 'Verify Python Hub and coder-nexus CLI status',
                action: () => vscode.commands.executeCommand('coder-nexus.checkHealth')
            },
            {
                label: '$(book) Open Documentation',
                description: 'View repository guides and setup instructions',
                action: () => {
                    if (vscode.env && typeof vscode.env.openExternal === 'function') {
                        vscode.env.openExternal(vscode.Uri.parse(REPO_URL));
                    }
                }
            }
        ];

        const choice = await vscode.window.showQuickPick(items, {
            placeHolder: 'Coder Nexus: Select an action'
        });
        if (choice && typeof choice.action === 'function') {
            choice.action();
        }
    });

    const cmdCheckHealth = vscode.commands.registerCommand('coder-nexus.checkHealth', () => {
        checkCliHealth(context, false);
    });

    const cmdInstallCli = vscode.commands.registerCommand('coder-nexus.installCli', () => installCli(context));

    context.subscriptions.push(
        cmdGlobal,
        cmdWorkspace,
        cmdWorkspaceFlutter,
        cmdWorkspaceFrappe,
        cmdWorkspaceBE,
        cmdWorkspaceFE,
        cmdShowArch,
        cmdQuickActions,
        cmdCheckHealth,
        cmdInstallCli    );

    // Status Bar Item for easy access
    if (vscode.window && typeof vscode.window.createStatusBarItem === 'function') {
        const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
        statusBarItem.text = '$(hubot) Coder Nexus';
        statusBarItem.tooltip = 'Coder Nexus: Click for Quick Actions & Status';
        statusBarItem.command = 'coder-nexus.quickActions';
        statusBarItem.show();
        context.subscriptions.push(statusBarItem);
    }

    // Prompt to sync when opening a recognized workspace for the first time
    checkFirstTimeWorkspacePrompt(context);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate,
    detectProjectRole,
    detectPacks
};
