[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$repo = 'lojandemas36-crypto/NEXUS'
$description = 'A Python workflow orchestrator that makes uncertain outcomes visible, supports explicit human decisions, and provides a read-only local dashboard.'
$website = 'https://lojandemas36-crypto.github.io/NEXUS/'
$topics = @('workflow-orchestration','python','sqlite','llm','ollama','automation','uncertain-resume','decision-api','dashboard','stdlib-only')
function Show-ManualValues {
    Write-Host 'GitHub Settings → General → About (copy-ready values):'
    Write-Host "Description: $description"
    Write-Host "Website: $website"
    Write-Host "Topics: $($topics -join ', ')"
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { Write-Warning 'GitHub CLI (gh) is not installed. No repository settings were changed.'; Show-ManualValues; exit 0 }
& gh auth status *> $null
if ($LASTEXITCODE -ne 0) { Write-Error 'GitHub CLI is not authenticated. Run "gh auth login", then rerun this script.'; exit 1 }
& gh repo edit $repo --description $description --homepage $website --add-topic workflow-orchestration --add-topic python --add-topic sqlite --add-topic llm --add-topic ollama --add-topic automation --add-topic uncertain-resume --add-topic decision-api --add-topic dashboard --add-topic stdlib-only
if ($LASTEXITCODE -ne 0) { throw 'gh repo edit failed; repository About metadata was not fully updated.' }
& gh api -X PUT repos/lojandemas36-crypto/NEXUS -F has_issues=true -F has_discussions=true
if ($LASTEXITCODE -ne 0) { throw 'GitHub API settings update failed after metadata edit.' }
Write-Host 'About updated: description, website, ten topics, Issues enabled, Discussions enabled.'
