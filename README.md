# LAB EX19: Continuous Deployment with GitHub Actions

Small Flask app, containerized, with a GitHub Actions pipeline that:

1. Runs unit tests.
2. Builds the Docker image and pushes it to **GitHub Container Registry (GHCR)**.
3. Deploys automatically to a **self-hosted runner** (your own PC) by pulling the
   new image and restarting the container -- this stands in for "deploy to a
   cloud platform" without needing an AWS/GCP/Azure account for the lab.

Repo: https://github.com/JoanathanPS/Exp19
Workflow file: `.github/workflows/exp19-deploy.yml` (must live at the repo
root for GitHub Actions to pick it up).

## One-time setup

### 1. Turn this folder into the repo and push it

This folder currently lives inside your bigger `CSA1016_Joanathan` repo's
working tree, but it's meant to be its own independent repo. Open PowerShell
in this folder (`Experiments\Exp\Exp19`) and run:

```powershell
git init
git branch -M main
git remote add origin https://github.com/JoanathanPS/Exp19.git
git add .
git commit -m "EX19: Dockerized app + GitHub Actions CD pipeline"
```

If you created the GitHub repo with a README/license/gitignore already in
it (GitHub does this by default unless you unchecked those boxes), the
remote has commits your local repo doesn't -- pull and merge them first:

```powershell
git pull origin main --allow-unrelated-histories
```

(If a merge editor opens, just save and close it to accept the default
merge commit message.) Then push:

```powershell
git push -u origin main
```

If the repo was created completely empty, skip the `pull` and just run
`git push -u origin main` directly.

### 2. Register your PC as a self-hosted runner

In your browser: open the **Exp19** repo -> **Settings -> Actions ->
Runners -> New self-hosted runner** -> pick **Windows** -> copy the exact
commands GitHub shows you (they include a unique token, so don't reuse the
ones below verbatim). It looks like this:

```powershell
mkdir actions-runner ; cd actions-runner
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/vX.X.X/actions-runner-win-x64-X.X.X.zip -OutFile actions-runner.zip
Expand-Archive -Path actions-runner.zip -DestinationPath .
./config.cmd --url https://github.com/JoanathanPS/Exp19 --token <TOKEN_FROM_GITHUB>
```

When `config.cmd` asks for runner name/labels, defaults are fine (just make
sure it's not labeled anything unusual -- the workflow targets `self-hosted`).

Then start it (keep this terminal open while you test the pipeline):

```powershell
./run.cmd
```

You should see `Listening for Jobs` once it's connected.

### 3. Make sure Docker Desktop is running

The `deploy` job runs `docker pull` / `docker run` on this same machine, so
Docker Desktop needs to be open (same as EX18).

## Testing the pipeline

Change something small in `app/app.py` (e.g. tweak the message string),
then, from `Experiments\Exp\Exp19`:

```powershell
git add app/app.py
git commit -m "test: trigger EX19 pipeline"
git push
```

Watch it run under the **Exp19** repo's **Actions** tab. Once the `deploy`
job goes green, check the running container:

```powershell
curl http://localhost:5001/
```

You should see the updated message plus a `version` field matching the git
commit SHA that triggered the build -- that's your proof the deployment is
actually the new code, not a stale container.

## Screenshots to grab for submission

1. Actions tab showing the 3 jobs (`test` -> `build-and-push` -> `deploy`)
   all green.
2. The `build-and-push` job's logs showing the image pushed to
   `ghcr.io/.../exp19-app`.
3. The repo's **Packages** tab showing the published container image.
4. Terminal output of `curl http://localhost:5001/` after a push, showing
   the updated `version`.

## Going further (optional)

Swap the self-hosted `deploy` job for a real cloud target once you're
comfortable with the pipeline shape:

- **AWS ECS**: use `aws-actions/amazon-ecs-deploy-task-definition` after
  pushing to ECR instead of GHCR.
- **Azure AKS** / **Google GKE**: use `azure/k8s-deploy` or
  `google-github-actions/deploy-cloudrun`, authenticating via OIDC (no
  long-lived cloud keys needed in repo secrets).

The `test` and `build-and-push` jobs stay identical either way -- only the
last job's target changes.
