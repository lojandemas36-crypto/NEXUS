[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$clone = 'C:\Users\Admin\Documents\ChatGPT\nexus\nexus_repo'
$source = $PSScriptRoot
$repo = 'https://github.com/lojandemas36-crypto/NEXUS'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Write-Error 'Git was not found on PATH. Install Git for Windows, then rerun this script.'; exit 1 }
if (-not (Test-Path -LiteralPath $clone -PathType Container)) { Write-Error "Local clone not found: $clone"; exit 1 }
Push-Location -LiteralPath $clone
try {
    & git rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -ne 0) { throw "The configured clone is not a Git working tree: $clone" }
    Write-Host 'Updating local main from origin/main with rebase...'
    & git pull --rebase origin main
    if ($LASTEXITCODE -ne 0) { throw 'git pull --rebase failed. Resolve the reported Git/authentication issue, then rerun.' }
    foreach ($name in @('REPO_METADATA.md','CONTRIBUTING.md','RELEASE_NOTES_v1.1.0.md','SOCIAL_ANNOUNCEMENT.md')) {
        $from = Join-Path $source $name
        if (-not (Test-Path -LiteralPath $from -PathType Leaf)) { throw "Required publication file is missing: $from" }
        Copy-Item -LiteralPath $from -Destination (Join-Path $clone $name) -Force
    }
    $templates = Join-Path $source '.github'
    if (Test-Path -LiteralPath $templates -PathType Container) { Copy-Item -LiteralPath $templates -Destination (Join-Path $clone '.github') -Recurse -Force }
    $shotsSource = Join-Path $env:USERPROFILE 'Desktop'
    $shotsDest = Join-Path $clone 'screenshots'
    New-Item -ItemType Directory -Path $shotsDest -Force | Out-Null
    foreach ($name in @('dashboard_overview.png','dashboard_workflows.png','dashboard_capabilities.png','dashboard_darkmode.png','nexus_console.png')) {
        $from = Join-Path $shotsSource $name
        if (Test-Path -LiteralPath $from -PathType Leaf) { Copy-Item -LiteralPath $from -Destination (Join-Path $shotsDest $name) -Force; Write-Host "Copied screenshot: $name" }
        else { Write-Warning "Screenshot is missing and was skipped: $from" }
    }
    & git add -A
    if ($LASTEXITCODE -ne 0) { throw 'git add -A failed.' }
    & git diff --cached --quiet
    $diffCode = $LASTEXITCODE
    if ($diffCode -eq 1) { & git commit -m 'Add community docs (metadata, contributing, release notes, social kit) and dashboard screenshots.'; if ($LASTEXITCODE -ne 0) { throw 'git commit failed. Review Git output and rerun after resolving the issue.' } }
    elseif ($diffCode -eq 0) { Write-Host 'No staged changes; commit skipped (idempotent rerun).' }
    else { throw "git diff --cached failed with exit code $diffCode." }
    & git push origin main
    if ($LASTEXITCODE -ne 0) { throw 'Push failed or was rejected. Check Git authentication and remote branch status; no force-push was attempted.' }
    $commit = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Could not read the resulting commit hash.' }
    $tracked = @(& git ls-tree -r --name-only origin/main)
    if ($LASTEXITCODE -ne 0) { throw 'Could not count tracked files on origin/main.' }
    Write-Host "Pushed to $repo"
    Write-Host "Commit: $commit"
    Write-Host "Tracked files on origin/main: $($tracked.Count)"
} catch { Write-Error $_; exit 1 }
finally { Pop-Location }
