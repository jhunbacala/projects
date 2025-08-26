# Repository Guidelines

## Project Structure & Module Organization
- Root: `Vagrantfile` defines the CentOS VM (box, CPUs, memory, networking, synced folders).
- `provision/`: provisioning scripts (e.g., `provision/bootstrap.sh`, `provision/verify.sh`).
- `scripts/`: local helper commands (e.g., `scripts/reload.sh`, `scripts/cleanup.sh`).
- `docs/`: usage notes and architecture snippets.
- `shared/` (optional): files synced into the VM via `/vagrant`.

## Build, Test, and Development Commands
- `vagrant up`: boots and provisions the VM from the `Vagrantfile`.
- `vagrant ssh`: opens an interactive shell inside the VM.
- `vagrant reload --provision`: restarts and re-runs provisioning.
- `vagrant halt`: stops the VM cleanly.
- `vagrant destroy -f`: removes the VM (data loss inside the VM).
- `shellcheck provision/*.sh`: lint provisioning shell scripts locally.

## Coding Style & Naming Conventions
- Shell scripts: 2-space indent; `bash` with `set -euo pipefail`; functions/use lower_snake_case; files use kebab-case (e.g., `install-packages.sh`).
- Ruby `Vagrantfile`: 2-space indent; single quotes unless interpolation; keep provider-specific settings grouped.
- File layout: group provisioning by concern (e.g., `provision/docker.sh`, `provision/users.sh`).

## Testing Guidelines
- Smoke: `vagrant up` finishes without errors, SSH works.
- Idempotency: `vagrant provision` twice yields no unexpected changes.
- Add `provision/verify.sh` with basic checks (examples):
  - `command -v docker` returns 0
  - services enabled and running (`systemctl status <name>`)
- Run verification non-interactively: `vagrant ssh -c 'bash /vagrant/provision/verify.sh'`.

## Commit & Pull Request Guidelines
- Commits: imperative mood with scope, e.g., `provision: install Docker CE`, `scripts: add cleanup`.
- PRs: include what/why, linked issues, repro/verification steps (commands), and relevant logs (`vagrant up --debug` if provisioning changed).

## Security & Configuration Tips
- Do not commit secrets; keep `.env` out of VCS and provide `.env.example`.
- Pin base box and versions in `Vagrantfile` (e.g., `bento/centos-7`, specific version).
- Prefer non-interactive package installs; avoid `sudo` when running as root during provisioning.

