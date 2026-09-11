# Evals — design-sandbox-setup

Two side-by-side evals used to check that runs *with* this skill reliably produce the
`COMPONENTS.md` / `CLAUDE.md` guardrail files that runs *without* it skip.

## Placeholders

| Placeholder | Meaning |
|---|---|
| `{{TARGET_DIR}}` | The empty folder the sandbox gets built in. Supplied by the eval runner. |
| `{{MONOREPO_DIR}}` | A local monorepo that vendors a design system as a workspace package, plus an app that consumes it. **You must supply this yourself.** |

## Which one you can run

- **`fresh-shadcn-no-source-app` (id 1)** — self-contained. Needs only `{{TARGET_DIR}}`; it
  installs shadcn/ui from the internet and builds a screen from a written description, so it
  runs anywhere.

- **`untitledui-real-repo` (id 0)** — needs `{{MONOREPO_DIR}}` pointed at a real monorepo on
  your machine. It was written against a private Untitled UI React repo, so substitute one of
  your own with the same shape: a design system package (e.g. `@repo/ui`) plus an app with a
  screen worth recreating. Update the package name, the app path, and the screen name in the
  prompt and assertions to match whatever you point it at.

Eval 0's last assertion (`git_clean`) checks that the skill treated your real repo as
read-only and wrote nothing outside `{{TARGET_DIR}}` — worth keeping whatever repo you swap in,
since "don't touch production" is the property most worth verifying.
