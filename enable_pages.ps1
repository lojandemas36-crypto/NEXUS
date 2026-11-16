[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$repo = 'lojandemas36-crypto/NEXUS'
$expected = 'https://lojandemas36-crypto.github.io/NEXUS/'
function Show-ManualSteps {
    Write-Host 'GitHub Pages manual setup: repository Settings → Pages → Build and deployment.'
    Write-Host 'Choose Deploy from a branch, branch main, folder /(root), then Save.'
    Write-Host "Expected site URL: $expected"
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { Write-Warning 'GitHub CLI (gh) is not installed. Pages was not configured.'; Show-ManualSteps; exit 0 }
& gh auth status *> $null
if ($LASTEXITCODE -ne 0) { Write-Error 'GitHub CLI is not authenticated. Run "gh auth login", then rerun this script.'; exit 1 }
$createOutput = & gh api -X POST "repos/$repo/pages" -f 'source[branch]=main' -f 'source[path]=/' 2>&1
$createCode = $LASTEXITCODE
if ($createCode -ne 0) {
    $createText = $createOutput -join "`n"
    if ($createText -match '(?i)already exists|already configured|already enabled') { Write-Host 'Pages configuration already exists; continuing with URL verification.' }
    else { Write-Error "Could not configure Pages: $createText"; Show-ManualSteps; exit 1 }
}
$timer = [Diagnostics.Stopwatch]::StartNew()
$url = ''
while ($timer.Elapsed.TotalSeconds -lt 120) {
    $urlOutput = & gh api "repos/$repo/pages" --jq .html_url 2>$null
    if ($LASTEXITCODE -eq 0) { $url = (($urlOutput | Out-String).Trim()) }
    if ($url.TrimEnd('/') -ieq $expected.TrimEnd('/')) { Write-Host "Pages is live: $url"; exit 0 }
    Write-Host ("Waiting for Pages URL... {0}s" -f [int]$timer.Elapsed.TotalSeconds)
    Start-Sleep -Seconds 5
}
Write-Error "Pages URL was not confirmed within 120 seconds. Last API URL: '$url'."
Show-ManualSteps
exit 1
