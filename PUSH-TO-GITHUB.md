# PUSH TO GITHUB - Run these commands

## Step 1: Create the repo on GitHub
1. Go to https://github.com/new
2. Repository name: `home-platform`
3. Description: `H.O.M.E. Platform - Housing Opportunity Management Engine for Long Beach`
4. Public repository
5. DO NOT initialize with README (we already have files)
6. Click "Create repository"

## Step 2: Push your code
Run these commands in PowerShell:

```powershell
cd C:\Users\james\Projects\Active\home-platform

git remote add origin https://github.com/EinInnSol/home-platform.git

git branch -M main

git push -u origin main
```

## Step 3: Get the URL for Opus
Once pushed, the repo URL will be:
https://github.com/EinInnSol/home-platform

Give Opus this URL and tell it to:
"Read all the documentation in this repo, especially OPUS-BUILD-REQUEST.md, and generate all the components listed."

---

## OR - Quick Alternative

If you want me to try one more thing, give me a GitHub Personal Access Token with repo permissions and I'll push it via API.

To create a token:
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Check "repo" scope
4. Copy the token
5. Give it to me

Then I can push everything in one command.
