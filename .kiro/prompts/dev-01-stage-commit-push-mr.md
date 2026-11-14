# dev-01-stage-commit-push-mr

Walk the developer through the full workflow of staging, committing, pushing, and raising a merge request for their current code changes. Follow each step in order. Each step must pass before moving to the next.

---

## Step 1 — Feature branch (blocking)

Check the current branch.

- If the developer is on `main`, **stop**. Do not proceed with any git operations.
  - Explain that commits to `main` are not allowed.
  - Ask whether to create a new feature branch or checkout an existing one.
  - Help them create or checkout the appropriate branch (e.g. `git checkout -b feature/<name>` or `git checkout <existing-branch>`).
  - Once they are on a non-main branch, continue to Step 2.
- If already on a feature branch, continue.

---

## Step 2 — Rebase on main

Bring the feature branch up to date with the latest `main` before committing.

1. Stash any unstaged or uncommitted changes: `git stash`.
2. Switch to `main` and pull the latest: `git checkout main && git pull`.
3. Switch back to the feature branch: `git checkout <feature-branch>`.
4. Rebase onto main: `git rebase main`.
5. Restore stashed changes: `git stash pop`.

If there are rebase conflicts, surface them to the developer and wait for resolution before continuing.

---

## Step 3 — Stage changes

Show the developer the current diff (`git status` and `git diff`).

Ask which files to stage, or confirm staging everything:
- Stage all: `git add .`
- Or stage specific files as directed.

Confirm the staged changes with `git diff --cached`.

---

## Step 4 — Generate a commit message

Infer a commit message from the staged diff and the nature of the changes.

Format:
```
<type>: <short-description>
```

Where `<type>` is one of: `feature`, `fix`, `docs`, `kiro`, `config`.

Rules:
- `<short-description>` must be lowercase, imperative mood, under 72 characters.
- Do not include a body or footer unless the developer asks.

Present the generated message to the developer and ask them to confirm or edit it before proceeding.

---

## Step 5 — Generate a MR description

Based on the staged diff and commit message, generate a merge request description using the following structure:

```
## Changes description
<A concise summary of what this MR contains.>

## Why change
<The reason or motivation behind these changes.>

## What is changing
<A specific breakdown of the files or logic being changed.>

## Testing
<How the changes were tested or how a reviewer can verify them.>

## Possible next steps (optional)
<Any follow-up work, known gaps, or future improvements.>
```

Present the generated description to the developer and ask them to confirm or edit it before proceeding.

---

## Step 6 — Commit

Commit the staged changes using the confirmed message:

```
git commit -m "<confirmed-commit-message>"
```

Confirm the commit was created successfully.

---

## Step 7 — Push to remote

Push the feature branch to the remote:

```
git push origin <feature-branch>
```

If the branch does not exist on the remote yet, use:

```
git push --set-upstream origin <feature-branch>
```

Confirm the push was successful.

---

## Step 8 — Raise a MR

Using the confirmed MR description from Step 5, raise a merge request targeting `main`.

- If the `gh` CLI is available: use `gh pr create --base main --title "<commit-message>" --body "<mr-description>"`.
- If the `glab` CLI is available: use `glab mr create --target-branch main --title "<commit-message>" --description "<mr-description>"`.
- If neither is available, output the MR title and description in full so the developer can paste it into their git hosting platform manually.

Confirm the MR was raised and provide the URL if returned by the CLI.
