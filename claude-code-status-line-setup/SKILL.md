---
name: claude-code-status-line-setup
description: Set up a custom multi-line Claude Code status bar footer showing context window usage, 5-hour and 7-day plan limits with reset times, git branch, and current model. Also triggers on /claude-code-status-line-setup.
---

# Claude Code Status Line Setup

Installs a custom 4-line footer in Claude Code that shows:
- **Line 1:** Current folder · git branch (+ dirty file count) · active model
- **Line 2:** Context window usage bar (%)
- **Line 3:** 5-hour plan usage bar + reset time
- **Line 4:** 7-day plan usage bar + reset time

The 5h/7d bars pull live data from Anthropic's usage API, authenticated via your local Claude Code session token. Data is cached for 60 seconds to avoid API hammering.

## Step 1 — Detect the OS

Check which OS the user is on:

```bash
uname -s 2>/dev/null || echo "Windows"
```

- `Darwin` → macOS path (bash script + Keychain auth)
- `Linux` → Linux path (bash script, no Keychain — 5h/7d bars show `—`)
- Anything else or command fails → Windows path (PowerShell script)

## Step 2 — Write the script

### macOS and Linux

Write the following to `~/.claude/statusline-command.sh`:

```bash
#!/bin/sh
input=$(cat)

raw_dir=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // empty')
model=$(echo "$input" | jq -r '.model.display_name // empty')
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')

folder_name=$(basename "$raw_dir")

RESET="\033[0m"
GRAY="\033[38;5;232m"
GRAY_FILLED="\033[38;5;232m"
GRAY_EMPTY="\033[38;5;248m"
SEP="\033[38;5;232m | "

bar=""
if [ -n "$used" ]; then
  used_int=$(printf "%.0f" "$used")
  total=15
  filled=$(( used_int * total / 100 ))
  [ "$filled" -gt "$total" ] && filled=$total
  empty=$(( total - filled ))

  i=0
  while [ "$i" -lt "$filled" ]; do
    bar="${bar}${GRAY_FILLED}█"
    i=$(( i + 1 ))
  done
  i=0
  while [ "$i" -lt "$empty" ]; do
    bar="${bar}${GRAY_EMPTY}░"
    i=$(( i + 1 ))
  done
  bar="${bar}${GRAY} ${used_int}%"
  ctx_segment="Context: ${bar}"
else
  ctx_segment=""
fi

CACHE_FILE="/tmp/claude_usage_cache.json"
CACHE_TIME_FILE="/tmp/claude_usage_cache_time"

_fetch_usage() {
  token=$(security find-generic-password -s 'Claude Code-credentials' -w 2>/dev/null | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('claudeAiOauth',{}).get('accessToken',''))" 2>/dev/null)
  if [ -z "$token" ]; then
    return 1
  fi
  curl -sf --max-time 4 \
    -H "Authorization: Bearer ${token}" \
    -H "anthropic-beta: oauth-2025-04-20" \
    -H "Content-Type: application/json" \
    "https://api.anthropic.com/api/oauth/usage" \
    -o "$CACHE_FILE" 2>/dev/null
}

_needs_refresh=1
if [ -f "$CACHE_TIME_FILE" ] && [ -f "$CACHE_FILE" ]; then
  last_time=$(cat "$CACHE_TIME_FILE" 2>/dev/null)
  now=$(date +%s)
  if [ -n "$last_time" ]; then
    age=$(( now - last_time ))
    [ "$age" -lt 60 ] && _needs_refresh=0
  fi
fi

if [ "$_needs_refresh" -eq 1 ]; then
  if _fetch_usage; then
    date +%s > "$CACHE_TIME_FILE"
  fi
fi

five_hour_pct=""
five_hour_resets=""
seven_day_pct=""
seven_day_resets=""
if [ -f "$CACHE_FILE" ]; then
  five_hour_pct=$(python3 -c "
import json,sys
try:
  d=json.load(open('$CACHE_FILE'))
  v=d.get('five_hour',{}).get('utilization')
  if v is not None: print(int(round(float(v))))
except: pass
" 2>/dev/null)
  seven_day_pct=$(python3 -c "
import json,sys
try:
  d=json.load(open('$CACHE_FILE'))
  v=d.get('seven_day',{}).get('utilization')
  if v is not None: print(int(round(float(v))))
except: pass
" 2>/dev/null)
  five_hour_resets=$(python3 -c "
import json,sys
try:
  d=json.load(open('$CACHE_FILE'))
  ts=d.get('five_hour',{}).get('resets_at')
  if ts:
    from datetime import datetime
    dt=datetime.fromisoformat(ts).astimezone()
    print(dt.strftime('%I:%M %p').lstrip('0').lower())
except: pass
" 2>/dev/null)
  seven_day_resets=$(python3 -c "
import json,sys
try:
  d=json.load(open('$CACHE_FILE'))
  ts=d.get('seven_day',{}).get('resets_at')
  if ts:
    from datetime import datetime
    dt=datetime.fromisoformat(ts).astimezone()
    print(dt.strftime('%b %-d, %I:%M %p').lower())
except: pass
" 2>/dev/null)
fi

_usage_bar() {
  _pct="$1"
  _total=10
  _filled=$(( _pct * _total / 100 ))
  [ "$_filled" -gt "$_total" ] && _filled=$_total
  _empty=$(( _total - _filled ))

  _BAR_FILLED="\033[38;5;232m"
  _BAR_EMPTY="\033[38;5;248m"
  _BAR_TEXT="\033[38;5;232m"

  _bar=""
  _i=0
  while [ "$_i" -lt "$_filled" ]; do
    _bar="${_bar}${_BAR_FILLED}█"
    _i=$(( _i + 1 ))
  done
  _i=0
  while [ "$_i" -lt "$_empty" ]; do
    _bar="${_bar}${_BAR_EMPTY}░"
    _i=$(( _i + 1 ))
  done
  printf "%b" "${_bar}${_BAR_TEXT} ${_pct}%${GRAY}"
}

five_hour_segment=""
if [ -n "$five_hour_pct" ]; then
  _bar_part=$(_usage_bar "$five_hour_pct")
  if [ -n "$five_hour_resets" ]; then
    five_hour_segment="5h: ${_bar_part}${GRAY}  resets ${five_hour_resets}"
  else
    five_hour_segment="5h: ${_bar_part}"
  fi
else
  five_hour_segment="5h: ${GRAY}—"
fi

seven_day_segment=""
if [ -n "$seven_day_pct" ]; then
  _bar_part=$(_usage_bar "$seven_day_pct")
  if [ -n "$seven_day_resets" ]; then
    seven_day_segment="7d: ${_bar_part}${GRAY}  resets ${seven_day_resets}"
  else
    seven_day_segment="7d: ${_bar_part}"
  fi
else
  seven_day_segment="7d: ${GRAY}—"
fi

git_segment=""
if [ -n "$raw_dir" ]; then
  git_branch=$(git -C "$raw_dir" rev-parse --abbrev-ref HEAD 2>/dev/null)
  if [ -n "$git_branch" ]; then
    git_dirty=$(git -C "$raw_dir" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    if [ "$git_dirty" -gt 0 ] 2>/dev/null; then
      git_segment="🌿 Branch: ${git_branch} (${git_dirty})"
    else
      git_segment="🌿 Branch: ${git_branch}"
    fi
  fi
fi

line1="${GRAY}📂 ${folder_name}"
if [ -n "$git_segment" ]; then
  line1="${line1}${SEP}${GRAY}${git_segment}"
fi
if [ -n "$model" ]; then
  line1="${line1}${SEP}${GRAY}★ ${model}"
fi

line2=""
if [ -n "$ctx_segment" ]; then
  line2="${GRAY}${ctx_segment}"
fi

line3="${GRAY}${five_hour_segment}"
line4="${GRAY}${seven_day_segment}"

printf "%b" "${line1}"
printf "%b" "\n${line2}"
printf "%b" "\n${line3}"
printf "%b" "\n${line4}"
printf "%b" "${RESET}"
```

Then make it executable:

```bash
chmod +x ~/.claude/statusline-command.sh
```

**Note for Linux users:** The `security find-generic-password` call is macOS-only. On Linux, the token fetch will silently fail and the 5h/7d bars will show `—`. Everything else (folder, branch, model, context %) works normally.

### Windows

Write the following to `~/.claude/statusline-command.ps1`:

```powershell
# Read JSON input from stdin
$input_data = $input | ConvertFrom-Json -ErrorAction SilentlyContinue

$raw_dir = $input_data.workspace.current_dir
if (-not $raw_dir) { $raw_dir = $input_data.cwd }
$model = $input_data.model.display_name
$used = $input_data.context_window.used_percentage

$folder_name = if ($raw_dir) { Split-Path $raw_dir -Leaf } else { "" }

# ANSI escape
$ESC = [char]27
$RESET = "$ESC[0m"
$GRAY = "$ESC[38;5;232m"
$GRAY_EMPTY = "$ESC[38;5;248m"
$SEP = "$ESC[38;5;232m | "

# Context bar (15 blocks)
$ctx_segment = ""
if ($used -ne $null) {
    $used_int = [int][math]::Round($used)
    $total = 15
    $filled = [math]::Min([int]($used_int * $total / 100), $total)
    $empty = $total - $filled
    $bar = ($GRAY + ("$ESC[38;5;232m█" * $filled)) + ("$ESC[38;5;248m░" * $empty) + "$GRAY $used_int%"
    $ctx_segment = "Context: $bar"
}

# Usage bar helper (10 blocks)
function Get-UsageBar($pct) {
    $total = 10
    $filled = [math]::Min([int]($pct * $total / 100), $total)
    $empty = $total - $filled
    return ($GRAY + ("$ESC[38;5;232m█" * $filled)) + ("$ESC[38;5;248m░" * $empty) + "$GRAY $pct%"
}

# Fetch usage from Anthropic API (cached 60s in $env:TEMP)
$cache_file = "$env:TEMP\claude_usage_cache.json"
$cache_time_file = "$env:TEMP\claude_usage_cache_time"
$five_hour_pct = $null
$five_hour_resets = ""
$seven_day_pct = $null
$seven_day_resets = ""

$needs_refresh = $true
if ((Test-Path $cache_time_file) -and (Test-Path $cache_file)) {
    $last_time = [long](Get-Content $cache_time_file -Raw).Trim()
    $now = [long](Get-Date -UFormat %s)
    if (($now - $last_time) -lt 60) { $needs_refresh = $false }
}

if ($needs_refresh) {
    # Try reading token from AppData credentials file
    $cred_path = "$env:APPDATA\Claude\credentials"
    $token = ""
    if (Test-Path $cred_path) {
        try {
            $cred = Get-Content $cred_path -Raw | ConvertFrom-Json
            $token = $cred.claudeAiOauth.accessToken
        } catch {}
    }
    if ($token) {
        try {
            $headers = @{
                "Authorization" = "Bearer $token"
                "anthropic-beta" = "oauth-2025-04-20"
                "Content-Type" = "application/json"
            }
            Invoke-RestMethod -Uri "https://api.anthropic.com/api/oauth/usage" `
                -Headers $headers -TimeoutSec 4 | ConvertTo-Json | Set-Content $cache_file
            [long](Get-Date -UFormat %s) | Set-Content $cache_time_file
        } catch {}
    }
}

if (Test-Path $cache_file) {
    try {
        $usage = Get-Content $cache_file -Raw | ConvertFrom-Json
        if ($usage.five_hour.utilization -ne $null) {
            $five_hour_pct = [int][math]::Round($usage.five_hour.utilization)
        }
        if ($usage.seven_day.utilization -ne $null) {
            $seven_day_pct = [int][math]::Round($usage.seven_day.utilization)
        }
        if ($usage.five_hour.resets_at) {
            $five_hour_resets = ([datetime]$usage.five_hour.resets_at).ToLocalTime().ToString("h:mm tt").ToLower()
        }
        if ($usage.seven_day.resets_at) {
            $seven_day_resets = ([datetime]$usage.seven_day.resets_at).ToLocalTime().ToString("MMM d, h:mm tt").ToLower()
        }
    } catch {}
}

# Git branch
$git_segment = ""
if ($raw_dir -and (Test-Path "$raw_dir\.git")) {
    try {
        $branch = git -C $raw_dir rev-parse --abbrev-ref HEAD 2>$null
        if ($branch) {
            $dirty = (git -C $raw_dir status --porcelain 2>$null | Measure-Object -Line).Lines
            $git_segment = if ($dirty -gt 0) { "Branch: $branch ($dirty)" } else { "Branch: $branch" }
        }
    } catch {}
}

# Assemble lines
$line1 = "${GRAY}$folder_name"
if ($git_segment) { $line1 += "${SEP}${GRAY}$git_segment" }
if ($model)       { $line1 += "${SEP}${GRAY}* $model" }

$line2 = if ($ctx_segment) { "${GRAY}$ctx_segment" } else { "" }

$five_hour_segment = if ($five_hour_pct -ne $null) {
    $bar = Get-UsageBar $five_hour_pct
    if ($five_hour_resets) { "5h: $bar${GRAY}  resets $five_hour_resets" } else { "5h: $bar" }
} else { "5h: ${GRAY}-" }

$seven_day_segment = if ($seven_day_pct -ne $null) {
    $bar = Get-UsageBar $seven_day_pct
    if ($seven_day_resets) { "7d: $bar${GRAY}  resets $seven_day_resets" } else { "7d: $bar" }
} else { "7d: ${GRAY}-" }

Write-Host -NoNewline "${line1}`n${line2}`n${GRAY}${five_hour_segment}`n${GRAY}${seven_day_segment}${RESET}"
```

**Note for Windows users:** The script looks for your Claude token at `%APPDATA%\Claude\credentials`. If the 5h/7d bars show `—`, the credentials file may be at a different path — check `%APPDATA%\Claude\` and adjust `$cred_path` in the script accordingly.

## Step 3 — Update settings.json

Read `~/.claude/settings.json` (create it as `{}` if it doesn't exist). Merge in the `statusLine` key without touching any existing keys:

**macOS / Linux:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline-command.sh"
  }
}
```

**Windows:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "powershell.exe -NoProfile -File \"%USERPROFILE%\\.claude\\statusline-command.ps1\""
  }
}
```

Write the merged result back to `~/.claude/settings.json`.

## Step 4 — Confirm and instruct

Tell the user:

> Done. Restart Claude Code and you'll see the 4-line footer. The 5h/7d usage bars update every 60 seconds from Anthropic's usage API.
> 
> [macOS only] The usage bars read your Claude session token from macOS Keychain — no extra auth needed.
> [Linux] The usage bars will show `—` since Linux doesn't use the macOS Keychain. Everything else works.
> [Windows] The usage bars look for your token at `%APPDATA%\Claude\credentials`. If they show `—`, check that path and update `$cred_path` in `~/.claude/statusline-command.ps1`.
