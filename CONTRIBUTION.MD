# Contributing to Tomcat Event Ticketing

This guide walks you through how we work as a team on this repo: setting up your machine, picking up a task, and getting your code merged. Follow it closely. It exists specifically to avoid merge conflict headaches.

---

## Table of Contents

- [1. Initial Setup](#1-initial-setup)
- [2. Project Structure, Who Owns What](#2-project-structure-who-owns-what)
- [3. Branching Strategy](#3-branching-strategy)
- [4. Daily Workflow](#4-daily-workflow)
- [5. Commit Message Format](#5-commit-message-format)
- [6. Opening a Pull Request](#6-opening-a-pull-request)
- [7. Code Review](#7-code-review)
- [8. Merging](#8-merging)
- [9. Avoiding and Resolving Conflicts](#9-avoiding-and-resolving-conflicts)
- [10. Quick Reference Cheat Sheet](#10-quick-reference-cheat-sheet)

---

## 1. Initial Setup

Do this once, on your own machine.

### 1.1 Install tools

| Tool | Purpose | Link |
|------|---------|------|
| **Git** | Version control | https://git-scm.com/downloads |
| **VS Code** | Editor | https://code.visualstudio.com |
| **GitHub Pull Requests and Issues** (VS Code extension) | Create and review PRs without leaving VS Code | Search "GitHub Pull Requests" in the VS Code Extensions tab |
| **AWS SAM CLI** | Run and deploy the serverless stack | https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html |
| **Python 3.12+** | Runtime for Lambda handlers | https://www.python.org/downloads/ |

### 1.2 Sign in to GitHub inside VS Code

1. Open VS Code.
2. Click the **Accounts** icon (bottom left corner).
3. Choose **Sign in with GitHub** and follow the browser prompt.
4. Once signed in, open the **Source Control** tab (left sidebar, branch icon). You should see your name and avatar.

### 1.3 Clone the repository

1. In VS Code, press `Ctrl/Cmd + Shift + P` and type `git clone https://github.com/EAkatse/tomcat-event-ticketing.git`.

2. Choose a folder on your machine, then **Open** the cloned repo when prompted.

### 1.4 Set up your local environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

You're set up. Do not skip signing in via the Accounts icon. The GitHub Pull Requests extension needs this to create and view PRs.

---

## 2. Project Structure, Who Owns What

Matching the `CODEOWNERS` file, each folder has a primary owner. If you're touching a folder that isn't yours, tag that person as a reviewer.

| Folder | Owns | Primary Owner |
|--------|------|----------------|
| `src/handlers/register/`, `src/handlers/cancel_registration/` | Registration and cancellation Lambdas | Backend Engineer |
| `src/handlers/list_events/`, `src/handlers/get_registrations/` | Events and registrations Lambdas, DynamoDB design | Database Admin |
| `infra/monitoring.yaml`, `infra/budgets.yaml` | CloudWatch, IAM, SNS, Budgets | Monitoring Lead |
| `.github/workflows/` | CI/CD pipeline | CI/CD Manager |
| `docs/`, `README.md`, `tests/` | Documentation, OpenAPI spec, testing | QA Lead |
| Overall architecture and coordination | Cross cutting decisions, domain and DNS | Team Coordinator |

---

## 3. Branching Strategy

We use a lightweight trunk based model. `main` is always deployable, and all work happens in short lived feature branches.

### 3.1 Branch naming

```
<type>/<short_description>
```

Use underscores to separate words in the description, not spaces or hyphens.

| Type | Use for |
|------|---------|
| `feature/` | New functionality (e.g. `feature/cancel_registration_endpoint`) |
| `fix/` | Bug fixes (e.g. `fix/dynamodb_throttle_alarm`) |
| `docs/` | Documentation only changes (e.g. `docs/update_api_endpoints_table`) |
| `chore/` | Tooling, CI/CD, dependency bumps (e.g. `chore/bump_sam_cli`) |

Keep names short and lowercase. Avoid personal names in branch names (e.g. not `feature/pipeline_by_sam`). Name the work, not the person, so anyone can tell what a branch does from its name alone, and so two people never end up with overlapping branches on the same topic.

### 3.2 Branch rules

- `main` is protected. No direct pushes. All changes come in through a Pull Request.
- One branch equals one task. Don't bundle unrelated changes (e.g. don't fix a Lambda bug and update the README in the same branch).

---

## 4. Daily Workflow

This is the sequence that prevents the nested conflict mess we hit before.

### Step 1: Start from an up to date `main`

Every single time you start new work:

```bash
git checkout main
git pull origin main
```

In VS Code, click **Source Control**, then the sync icon (circular arrows) while on `main`, or use `Ctrl/Cmd+Shift+P` and select **Git: Pull**.

### Step 2: Create your branch

```bash
git checkout -b feature/your_branch_name
```

Or in VS Code, click the branch name in the bottom left status bar, then **Create new branch**.

### Step 3: Work, commit often

Commit in small logical chunks rather than one giant commit at the end. Use the **Source Control** tab: stage files with the plus icon, write a message, and press `Ctrl/Cmd+Enter` to commit.

### Step 4: Pull `main` into your branch daily, even mid task

This is the single most important habit to prevent conflicts:

```bash
git checkout main
git pull origin main
git checkout feature/your_branch_name
git merge main
```

Do this every time you're working on a branch, and again right before opening your PR.

### Step 5: Push your branch

```bash
git push origin feature/your_branch_name
```

Or click **Publish Branch** in VS Code's Source Control tab.

---

## 5. Commit Message Format

Use Conventional Commits (see conventionalcommits.org): short, structured, and it makes the project history readable.

```
<type>: <short summary>
```

| Type | Example |
|------|---------|
| `feat` | `feat: add DELETE /registration endpoint` |
| `fix` | `fix: correct GSI1PK format in registrations query` |
| `docs` | `docs: update API endpoints table` |
| `chore` | `chore: update samconfig for prod deploy` |
| `test` | `test: add unit tests for cancel_registration handler` |

Avoid vague messages like `update stuff` or `fixes`.

---

## 6. Opening a Pull Request

All done inside VS Code with the GitHub Pull Requests extension.

1. Push your branch (see Step 5 above).
2. Open the **GitHub Pull Requests** icon in the VS Code sidebar (a branching icon labeled "PR").
3. Click **Create Pull Request**.
4. Base branch: `main`. Compare branch: your feature branch.
5. Fill in the PR template that appears (from `.github/PULL_REQUEST_TEMPLATE.md`). Describe what changed and why.
6. Assign the relevant code owner (see Section 2) as a reviewer.
7. Submit.

---

## 7. Code Review

- Reviewers should aim to respond within the shortest possible time.
- If you're the reviewer, use the GitHub Pull Requests extension's inline commenting (click the plus icon next to a line in the PR's "Files Changed" view) rather than a giant comment at the end.

---

## 8. Merging

- Use **Squash and Merge** (select this from the dropdown on the merge button). It keeps `main`'s history as one clean commit per feature, rather than a pile of "wip" commits.
- After merging, delete the branch (VS Code and GitHub will prompt you). Don't keep merged branches around, they cause confusion about what's still live work.
- Pull `main` locally again afterward so your next branch starts fresh:
  ```bash
  git checkout main
  git pull origin main
  ```

---

## 9. Avoiding and Resolving Conflicts

**Prevention (do this and you'll rarely see a real conflict):**

- Pull `main` into your branch daily (Section 4, Step 4).
- Keep branches small and short lived.
- Don't copy content, such as whole README sections, between branches manually. That's what caused the nested conflict markers we ran into. If two branches need the same content, merge through `main`, don't copy it across by hand.
- Treat shared files (`README.md`, `docs/ARCHITECTURE.md`) as a high risk for conflicts. Coordinate in Trello or chat before editing them if you know someone else is also touching docs.

**If you do hit a conflict:**

1. The GitHub Pull Requests extension, or VS Code's built in merge editor, will show conflicting files with **Accept Current**, **Accept Incoming**, or **Accept Both** buttons. Use the built in merge editor rather than editing `<<<<<<<` markers by hand where possible.
2. Read both sides before choosing. Don't blindly click "Accept Incoming" for everything.
3. After resolving, check the file for leftover `<<<<<<<`, `=======`, `>>>>>>>` markers before committing. VS Code highlights unresolved markers in red. Don't commit until they're gone.
4. If a conflict looks confusing or nested, with multiple marker blocks, stop and ask in the team channel rather than guessing. It's much faster to sort out together than to untangle a bad resolution later.
5. Once resolved, stage the files, commit, and continue.

If a merge attempt goes badly wrong, it's fine to abort and start over:

```bash
git merge --abort
```

---

## 10. Quick Reference Cheat Sheet

```bash
# Start new work
git checkout main
git pull origin main
git checkout -b feature/my_task

# Stay in sync while working
git checkout main && git pull origin main
git checkout feature/my_task && git merge main

# Push and open PR
git push origin feature/my_task
# then use the GitHub Pull Requests extension in VS Code to open the PR

# After merge
git checkout main
git pull origin main
```

---

Questions about this process go to the Team Coordinator. Questions about a specific folder's code go to that folder's owner.