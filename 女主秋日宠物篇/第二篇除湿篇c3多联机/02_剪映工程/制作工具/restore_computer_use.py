from pathlib import Path
import shutil
import tomllib

config = Path('/Users/weipeilong/.codex/config.toml')
backup = Path(__file__).parent / 'config_before_computer_use_restore.toml'
text = config.read_text()
current = tomllib.loads(text).get('mcp_servers', {}).get('cua_repl', {})
if current.get('command') != '/Applications/ChatGPT.app/Contents/MacOS/ChatGPT':
    raise SystemExit('Unexpected Computer Use launcher; no changes made.')
if current.get('enabled') is True:
    print('Computer Use configuration already enabled.')
    raise SystemExit(0)
if current.get('enabled') is not False:
    raise SystemExit('Unexpected Computer Use enabled state; no changes made.')
lines = text.splitlines(keepends=True)
in_section = False
changed = 0
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('['):
        in_section = stripped == '[mcp_servers.cua_repl]'
    if in_section and stripped == 'enabled = false':
        lines[i] = line.replace('enabled = false', 'enabled = true')
        changed += 1
if changed != 1:
    raise SystemExit('Expected exactly one switch; no changes made.')
updated = ''.join(lines)
assert tomllib.loads(updated)['mcp_servers']['cua_repl']['enabled'] is True
if not backup.exists():
    shutil.copy2(config, backup)
config.write_text(updated)
assert tomllib.loads(config.read_text())['mcp_servers']['cua_repl']['enabled'] is True
print('Enabled existing Computer Use server. Original configuration backed up locally.')
