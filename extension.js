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

function rewriteFlattenedLinks(directory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
        const file = path.join(directory, entry.name);
        if (entry.isDirectory()) {
            rewriteFlattenedLinks(file);
        } else if (entry.name.endsWith('.md')) {
            const text = fs.readFileSync(file, 'utf8');
            const rewritten = text.replaceAll('(../../flutter/', '(../').replaceAll('(../skills/flutter/', '(../skills/');
            if (rewritten !== text) fs.writeFileSync(file, rewritten, 'utf8');
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

function bundledPluginVersion(context, pluginName) {
    try {
        const manifest = path.join(context.extensionPath, 'plugins', pluginName, 'bundle_manifest.json');
        return JSON.parse(fs.readFileSync(manifest, 'utf8')).plugin_version || null;
    } catch (_) {
        return null;
    }
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

/**
 * Detect project role ('flutter', 'frappe', or 'be') based on workspace root signatures.
 */
function detectProjectRole(workspacePath) {
    if (fs.existsSync(path.join(workspacePath, 'pubspec.yaml'))) {
        return 'flutter';
    }
    const pkgPath = path.join(workspacePath, 'package.json');
    if (fs.existsSync(pkgPath)) {
        try {
            const content = fs.readFileSync(pkgPath, 'utf8');
            if (content.includes('frappe-ui')) {
                return 'frappe';
            }
        } catch (_) {}
    }
    if (fs.existsSync(path.join(workspacePath, 'hooks.py'))) {
        return 'frappe';
    }
    const beSignatures = [
        'go.mod', 'pom.xml', 'build.gradle', 'build.gradle.kts',
        'requirements.txt', 'pyproject.toml', 'Cargo.toml',
        'Dockerfile', 'docker-compose.yml'
    ];
    for (const sig of beSignatures) {
        if (fs.existsSync(path.join(workspacePath, sig))) {
            return 'be';
        }
    }
    return 'flutter';
}

/**
 * Check if the workspace contains recognized project signatures (Flutter, Frappe, or Backend).
 */
function isRecognizedWorkspace(workspacePath) {
    if (fs.existsSync(path.join(workspacePath, 'pubspec.yaml'))) return true;
    const pkgPath = path.join(workspacePath, 'package.json');
    if (fs.existsSync(pkgPath)) {
        try {
            const content = fs.readFileSync(pkgPath, 'utf8');
            if (content.includes('frappe-ui')) return true;
        } catch (_) {}
    }
    if (fs.existsSync(path.join(workspacePath, 'hooks.py'))) return true;
    const beSignatures = [
        'go.mod', 'pom.xml', 'build.gradle', 'build.gradle.kts',
        'requirements.txt', 'pyproject.toml', 'Cargo.toml',
        'Dockerfile', 'docker-compose.yml'
    ];
    return beSignatures.some(sig => fs.existsSync(path.join(workspacePath, sig)));
}

/**
 * Install or update Coder Nexus Antigravity plugin with flattened skills.
 */
function installAntigravityPlugin(context, targetWorkspace = null, silent = false, pluginName = 'coder-nexus-fe', framework = 'flutter') {
    const pluginSource = path.join(context.extensionPath, 'plugins', pluginName);
    const sharedContracts = path.join(context.extensionPath, 'plugins', 'shared_contracts');
    if (!fs.existsSync(pluginSource) || !fs.existsSync(path.join(sharedContracts, 'api_handshake_protocol.md'))) {
        if (!silent) {
            vscode.window.showErrorMessage(`Coder Nexus plugin assets (${pluginName}) or shared handshake protocol not found inside extension path.`);
        }
        return false;
    }

    try {
        let destPath;
        if (targetWorkspace) {
            destPath = path.join(targetWorkspace, '.agents', 'plugins', pluginName);
        } else {
            const home = os.homedir();
            destPath = path.join(home, '.gemini', 'config', 'plugins', pluginName);
        }

        if (fs.existsSync(destPath)) {
            fs.rmSync(destPath, { recursive: true, force: true });
        }
        fs.mkdirSync(destPath, { recursive: true });

        if (pluginName === 'coder-nexus-fe') {
            const entries = fs.readdirSync(pluginSource, { withFileTypes: true });
            for (const entry of entries) {
                if (entry.name === 'skills' || entry.name === 'rules') {
                    continue;
                }
                // Workspace agents live only in .agents/agents (single copy the host reads).
                if (entry.name === 'agents' && targetWorkspace) {
                    continue;
                }
                const src = path.join(pluginSource, entry.name);
                const dest = path.join(destPath, entry.name);
                if (entry.isDirectory()) {
                    copyFolderSync(src, dest);
                } else {
                    fs.copyFileSync(src, dest);
                }
            }

            const rulesDest = path.join(destPath, 'rules');
            fs.mkdirSync(rulesDest, { recursive: true });
            const rulesSource = path.join(pluginSource, 'rules');
            if (framework === 'frappe') {
                const frappeRule = path.join(rulesSource, 'frappe_specific_rules.md');
                if (fs.existsSync(frappeRule)) {
                    fs.copyFileSync(frappeRule, path.join(rulesDest, 'frappe_specific_rules.md'));
                }
            } else {
                const flutterRule = path.join(rulesSource, 'clean_architecture_rules.md');
                if (fs.existsSync(flutterRule)) {
                    fs.copyFileSync(flutterRule, path.join(rulesDest, 'clean_architecture_rules.md'));
                }
            }

            const skillsDest = path.join(destPath, 'skills');
            fs.mkdirSync(skillsDest, { recursive: true });
            const skillsSource = path.join(pluginSource, 'skills');

            // Shared skills
            const sharedDir = path.join(skillsSource, 'shared');
            if (fs.existsSync(sharedDir)) {
                for (const item of fs.readdirSync(sharedDir, { withFileTypes: true })) {
                    if (item.isDirectory() && fs.existsSync(path.join(sharedDir, item.name, 'SKILL.md'))) {
                        copyFolderSync(path.join(sharedDir, item.name), path.join(skillsDest, item.name));
                    }
                }
            }

            // Framework skills (flutter or frappe)
            const fwDir = path.join(skillsSource, framework);
            if (fs.existsSync(fwDir)) {
                for (const item of fs.readdirSync(fwDir, { withFileTypes: true })) {
                    if (item.isDirectory() && fs.existsSync(path.join(fwDir, item.name, 'SKILL.md'))) {
                        copyFolderSync(path.join(fwDir, item.name), path.join(skillsDest, item.name));
                    }
                }
            }

            // Rewrite manifest to reflect flattened skills
            const manifestPath = path.join(destPath, 'bundle_manifest.json');
            if (fs.existsSync(manifestPath)) {
                try {
                    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
                    const installedSkills = fs.readdirSync(skillsDest, { withFileTypes: true })
                        .filter(e => e.isDirectory() && fs.existsSync(path.join(skillsDest, e.name, 'SKILL.md')))
                        .map(e => e.name)
                        .sort();
                    manifest.public_skills = installedSkills;

                    if (Array.isArray(manifest.required_resources)) {
                        const excludedFramework = framework === 'frappe' ? 'flutter' : 'frappe';
                        const excludedRule = framework === 'frappe' ? 'clean_architecture_rules.md' : 'frappe_specific_rules.md';
                        manifest.required_resources = manifest.required_resources.filter(res =>
                            !res.startsWith(`skills/${excludedFramework}/`) && res !== `rules/${excludedRule}`
                        ).map(res => {
                            for (const prefix of ['skills/shared/', 'skills/flutter/', 'skills/frappe/']) {
                                if (res.startsWith(prefix)) {
                                    return 'skills/' + res.slice(prefix.length);
                                }
                            }
                            return res;
                        });
                    }
                    fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
                } catch (e) {
                    console.error('Failed to update bundle_manifest.json:', e);
                }
            }
        } else {
            // Backend plugin is already flat; workspace agents live only in .agents/agents.
            for (const entry of fs.readdirSync(pluginSource, { withFileTypes: true })) {
                if (entry.name === 'agents' && targetWorkspace) continue;
                const src = path.join(pluginSource, entry.name);
                const dest = path.join(destPath, entry.name);
                if (entry.isDirectory()) copyFolderSync(src, dest); else fs.copyFileSync(src, dest);
            }
        }

        copyFolderSync(sharedContracts, path.join(destPath, 'shared_contracts'));
        // GUI-launched IDEs may not have ~/.local/bin in PATH; point MCP at the absolute CLI when present.
        const mcpConfigPath = path.join(destPath, 'mcp_config.json');
        if (fs.existsSync(mcpConfigPath) && fs.existsSync(localCliPath())) {
            const mcp = JSON.parse(fs.readFileSync(mcpConfigPath, 'utf8'));
            if (mcp.mcpServers && mcp.mcpServers['coder-nexus']) {
                mcp.mcpServers['coder-nexus'].command = localCliPath();
                fs.writeFileSync(mcpConfigPath, JSON.stringify(mcp, null, 2) + '\n', 'utf8');
            }
        }
        if (pluginName === 'coder-nexus-fe') rewriteFlattenedLinks(destPath);
        const projectedManifestPath = path.join(destPath, 'bundle_manifest.json');
        const projectedManifest = JSON.parse(fs.readFileSync(projectedManifestPath, 'utf8'));
        projectedManifest.required_resources = (projectedManifest.required_resources || []).map(res => {
            if (res.startsWith('../shared_contracts/')) return res.slice(3);
            if (targetWorkspace && res.startsWith('agents/')) return `../../${res}`;
            return res;
        });
        fs.writeFileSync(projectedManifestPath, JSON.stringify(projectedManifest, null, 2) + '\n', 'utf8');
        fs.writeFileSync(path.join(destPath, 'installed_version.json'), JSON.stringify({
            plugin_version: projectedManifest.plugin_version || 'UNKNOWN',
            extension_version: extensionVersion(context),
            framework: pluginName === 'coder-nexus-fe' ? framework : null,
            synced_at: new Date().toISOString(),
        }, null, 2) + '\n', 'utf8');

        if (targetWorkspace) {
            // Sync corresponding agents to .agents/agents
            const agentsSource = path.join(pluginSource, 'agents');
            const agentsDest = path.join(targetWorkspace, '.agents', 'agents');
            if (fs.existsSync(agentsSource)) {
                copyFolderSync(agentsSource, agentsDest);
            }

            // Remove a stale agents/ copy left inside the plugin by older syncs.
            fs.rmSync(path.join(destPath, 'agents'), { recursive: true, force: true });

            // Clean up the alternative plugin directory if present to avoid role confusion
            const otherPlugin = pluginName === 'coder-nexus-fe' ? 'coder-nexus-be' : 'coder-nexus-fe';
            const otherDest = path.join(targetWorkspace, '.agents', 'plugins', otherPlugin);
            if (fs.existsSync(otherDest)) {
                fs.rmSync(otherDest, { recursive: true, force: true });
            }
        }

        // Ensure bundled Ponytail plugin is installed if not already present on host/workspace
        ensurePonytailPlugin(context, targetWorkspace, silent);

        const frameworkLabel = pluginName === 'coder-nexus-fe' ? (framework === 'frappe' ? 'Frappe UI' : 'Flutter') : 'Backend (BE)';
        if (!silent) {
            const msg = `✅ ${frameworkLabel} plugin synced to Antigravity (${destPath})`;
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
            vscode.window.showErrorMessage(`❌ Failed to sync ${pluginName} plugin: ${err.message}`);
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

    // Do nothing if already synced
    const fePath = path.join(wsPath, '.agents', 'plugins', 'coder-nexus-fe');
    const bePath = path.join(wsPath, '.agents', 'plugins', 'coder-nexus-be');
    if (fs.existsSync(fePath) || fs.existsSync(bePath)) {
        warnIfStaleSync(context, fs.existsSync(fePath) ? fePath : bePath);
        return;
    }

    if (!isRecognizedWorkspace(wsPath)) {
        return;
    }

    const state = context.workspaceState;
    if (state && typeof state.get === 'function' && state.get('coderNexusPromptDismissed')) {
        return;
    }

    const role = detectProjectRole(wsPath);
    const roleLabel = role === 'flutter' ? 'Flutter' : role === 'be' ? 'Backend' : 'Frappe UI';

    if (vscode.window && typeof vscode.window.showInformationMessage === 'function') {
        const p = vscode.window.showInformationMessage(
            `🚀 Coder Nexus: Detected a ${roleLabel} project. Sync AI delivery agents & skills into this workspace?`,
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
    const bundled = bundledPluginVersion(context, pluginName);
    if (!bundled || installed === bundled) return;
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
        installAntigravityPlugin(context, null, false, 'coder-nexus-fe', 'flutter');
    });

    const cmdWorkspace = vscode.commands.registerCommand('coder-nexus.installWorkspace', async () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showWarningMessage('No workspace open to sync Coder Nexus plugin.');
            return;
        }
        const wsPath = workspaceFolders[0].uri.fsPath;
        const detected = detectProjectRole(wsPath);

        const items = [
            {
                label: '📱 Flutter (Frontend Client)',
                description: detected === 'flutter' ? '⭐ Recommended (Detected pubspec.yaml)' : '',
                pluginName: 'coder-nexus-fe',
                framework: 'flutter'
            },
            {
                label: '🌐 Frappe UI (Frontend Desk)',
                description: detected === 'frappe' ? '⭐ Recommended (Detected Frappe)' : '',
                pluginName: 'coder-nexus-fe',
                framework: 'frappe'
            },
            {
                label: '🖥️ Backend (API / Service)',
                description: detected === 'be' ? '⭐ Recommended (Detected backend files)' : '',
                pluginName: 'coder-nexus-be',
                framework: null
            }
        ];

        const recommendedIdx = items.findIndex(item => item.description.includes('Recommended'));
        if (recommendedIdx > 0) {
            const [recItem] = items.splice(recommendedIdx, 1);
            items.unshift(recItem);
        }

        const choice = await vscode.window.showQuickPick(items, {
            placeHolder: 'Select Coder Nexus plugin to sync into this workspace'
        });

        if (choice) {
            installAntigravityPlugin(context, wsPath, false, choice.pluginName, choice.framework || 'flutter');
        }
    });

    const cmdWorkspaceFlutter = vscode.commands.registerCommand('coder-nexus.installWorkspaceFlutter', () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showWarningMessage('No workspace open to sync Coder Nexus plugin.');
            return;
        }
        installAntigravityPlugin(context, workspaceFolders[0].uri.fsPath, false, 'coder-nexus-fe', 'flutter');
    });

    const cmdWorkspaceFrappe = vscode.commands.registerCommand('coder-nexus.installWorkspaceFrappe', () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showWarningMessage('No workspace open to sync Coder Nexus plugin.');
            return;
        }
        installAntigravityPlugin(context, workspaceFolders[0].uri.fsPath, false, 'coder-nexus-fe', 'frappe');
    });

    const cmdWorkspaceBE = vscode.commands.registerCommand('coder-nexus.installWorkspaceBE', () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showWarningMessage('No workspace open to sync Coder Nexus plugin.');
            return;
        }
        installAntigravityPlugin(context, workspaceFolders[0].uri.fsPath, false, 'coder-nexus-be', null);
    });

    const cmdWorkspaceFE = vscode.commands.registerCommand('coder-nexus.installWorkspaceFE', () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showWarningMessage('No workspace open to sync Coder Nexus plugin.');
            return;
        }
        installAntigravityPlugin(context, workspaceFolders[0].uri.fsPath, false, 'coder-nexus-fe', 'flutter');
    });

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
                label: '$(sync) Sync Plugin to Workspace (Auto-Detect)',
                description: 'Detects project stack and installs AI agents & skills',
                action: () => vscode.commands.executeCommand('coder-nexus.installWorkspace')
            },
            {
                label: '$(device-mobile) Force Sync Flutter Bundle',
                description: 'Installs Flutter roles, clean architecture rules & skills',
                action: () => vscode.commands.executeCommand('coder-nexus.installWorkspaceFlutter')
            },
            {
                label: '$(server) Force Sync Backend (BE) Bundle',
                description: 'Installs Backend roles & handshake contracts',
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
    detectProjectRole
};
