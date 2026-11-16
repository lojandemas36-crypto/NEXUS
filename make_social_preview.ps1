[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$clone = 'C:\Users\Admin\Documents\ChatGPT\nexus\nexus_repo'
if (-not (Test-Path -LiteralPath $clone -PathType Container)) { throw "Local clone not found: $clone" }
$png = Join-Path $clone 'social-preview.png'
$svg = Join-Path $clone 'social-preview.svg'
try {
    Add-Type -AssemblyName System.Drawing -ErrorAction Stop
    $bitmap = New-Object System.Drawing.Bitmap 1200,630
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
        $graphics.Clear([System.Drawing.ColorTranslator]::FromHtml('#1a202c'))
        $green = [System.Drawing.ColorTranslator]::FromHtml('#0a6e0a')
        $white = [System.Drawing.Color]::White
        $muted = [System.Drawing.ColorTranslator]::FromHtml('#cbd5e0')
        $bar = New-Object System.Drawing.SolidBrush $green
        $titleBrush = New-Object System.Drawing.SolidBrush $white
        $subtitleBrush = New-Object System.Drawing.SolidBrush $muted
        $chipTextBrush = New-Object System.Drawing.SolidBrush $white
        $fontTitle = New-Object System.Drawing.Font('Segoe UI',76,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
        $fontSubtitle = New-Object System.Drawing.Font('Segoe UI',30,[System.Drawing.FontStyle]::Regular,[System.Drawing.GraphicsUnit]::Pixel)
        $fontChip = New-Object System.Drawing.Font('Segoe UI',20,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
        $fontFooter = New-Object System.Drawing.Font('Segoe UI',20,[System.Drawing.FontStyle]::Regular,[System.Drawing.GraphicsUnit]::Pixel)
        $graphics.FillRectangle($bar,0,0,18,630)
        $graphics.DrawString('NEXUS',$fontTitle,$titleBrush,72,96)
        $graphics.DrawString('Workflow orchestrator with uncertain-resume',$fontSubtitle,$subtitleBrush,78,220)
        $chipSpecs = @(@{Text='Completed';X=78;Color='#0a6e0a';Width=190},@{Text='Needs review';X=286;Color='#b7791f';Width=230},@{Text='Failed';X=534;Color='#c53030';Width=150})
        foreach($chip in $chipSpecs){$brush=New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml($chip.Color));$graphics.FillRectangle($brush,$chip.X,350,$chip.Width,52);$graphics.DrawString($chip.Text,$fontChip,$chipTextBrush,($chip.X+16),359);$brush.Dispose()}
        $graphics.DrawString('v1.1  ·  Lojan Demas  ·  2026',$fontFooter,$muted,78,548)
        $bitmap.Save($png,[System.Drawing.Imaging.ImageFormat]::Png)
        $bar.Dispose();$titleBrush.Dispose();$subtitleBrush.Dispose();$chipTextBrush.Dispose();$fontTitle.Dispose();$fontSubtitle.Dispose();$fontChip.Dispose();$fontFooter.Dispose()
    } finally {$graphics.Dispose();$bitmap.Dispose()}
    $hash=(Get-FileHash -LiteralPath $png -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-Host "Social preview PNG: $png"
    Write-Host "SHA-256: $hash"
} catch {
    if(Test-Path -LiteralPath $png){Remove-Item -LiteralPath $png -Force}
    $svgLines=@(
'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">',
'<rect width="1200" height="630" fill="#1a202c"/><rect width="18" height="630" fill="#0a6e0a"/>',
'<text x="78" y="190" fill="#ffffff" font-family="Segoe UI,Arial,sans-serif" font-size="100" font-weight="700">NEXUS</text>',
'<text x="82" y="275" fill="#cbd5e0" font-family="Segoe UI,Arial,sans-serif" font-size="30">Workflow orchestrator with uncertain-resume</text>',
'<rect x="78" y="350" width="190" height="52" fill="#0a6e0a"/><text x="94" y="385" fill="white" font-family="Arial,sans-serif" font-size="20" font-weight="700">Completed</text>',
'<rect x="286" y="350" width="230" height="52" fill="#b7791f"/><text x="302" y="385" fill="white" font-family="Arial,sans-serif" font-size="20" font-weight="700">Needs review</text>',
'<rect x="534" y="350" width="150" height="52" fill="#c53030"/><text x="550" y="385" fill="white" font-family="Arial,sans-serif" font-size="20" font-weight="700">Failed</text>',
'<text x="78" y="570" fill="#cbd5e0" font-family="Segoe UI,Arial,sans-serif" font-size="20">v1.1 · Lojan Demas · 2026</text></svg>'
    )
    Set-Content -LiteralPath $svg -Value ($svgLines -join "`n") -Encoding UTF8
    $svgHash=(Get-FileHash -LiteralPath $svg -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-Warning 'System.Drawing is unavailable. SVG fallback created; export it as a 1200x630 PNG before upload.'
    Write-Host "Social preview SVG: $svg"
    Write-Host "SHA-256: $svgHash"
}
