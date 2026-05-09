param(
  [string]$Python = "python"
)

# Create a venv in backend/.venv
$venvPath = Join-Path $PSScriptRoot '.venv'
if (-Not (Test-Path $venvPath)) {
  & $Python -m venv $venvPath
}

# Activate for current session
$activate = Join-Path $venvPath 'Scripts\Activate.ps1'
if (Test-Path $activate) {
  Write-Host "Activating venv: $venvPath"
  . $activate
  pip install --upgrade pip
  pip install -r (Join-Path $PSScriptRoot 'requirements.txt')
  Write-Host "Setup complete. Run: uvicorn app.main:app --reload"
} else {
  Write-Error "Activation script not found. Ensure Python is installed and venv created."
}
