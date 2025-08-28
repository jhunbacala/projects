# Puppet Project (Docker-only): 1 Server + 2 Agents

This project runs a single Puppet Server and two Puppet Agents using Docker Compose. It persists server data via named volumes and includes optional autosigning for fast, hands-free development.

## Prerequisites

- Docker Engine 20.10+ and Docker Compose v2 plugin
- ~2 GB free RAM for the Puppet Server container

## Project Structure

```
puppet-project/
├─ docker-compose.yml
├─ code/
│  └─ environments/
│     └─ production/
│        └─ manifests/
│           └─ site.pp
└─ puppet/
   └─ autosign.conf   (dev-only; optional)
```

## What’s Included

- Puppet Server container exposed on port `8140` with limited JVM memory.
- Two Puppet Agent containers (`agent1` and `agent2`) that connect to the server and request certs.
- Example manifest to prove convergence by creating a file on each agent.
- Optional autosign for easy development: automatically signs agents matching `*.example.test`.

## Quick Start

1) Start the Puppet Server first (initial CA/cert setup takes ~1–2 minutes):

```
cd puppet-project
docker compose up -d puppet
docker logs -f puppet
```

2) Once the server log shows it is ready, start the agents:

```
docker compose up -d agent1 agent2
```

3) Verify the example resource was applied:

```
docker exec -it puppet-agent1 cat /tmp/hello_from_puppet
docker exec -it puppet-agent2 cat /tmp/hello_from_puppet
```

You should see "Hello from Puppet" on both.

## Manual Certificate Signing (if not using autosign)

By default, `docker-compose.yml` mounts `puppet/autosign.conf` to enable automatic signing in development. For manual signing, comment out that bind mount in `docker-compose.yml` under the `puppet` service and restart the server. Then:

```
docker exec -it puppet puppetserver ca list --all
docker exec -it puppet puppetserver ca sign --all
```

Trigger an agent run to apply the catalog immediately:

```
docker exec -it puppet-agent1 puppet agent -t
docker exec -it puppet-agent2 puppet agent -t
```

## Editing Puppet Code

- Update `code/environments/production/manifests/site.pp` or add modules/classes under `code`.
- Re-run an agent to apply changes:

```
docker exec -it puppet-agent1 puppet agent -t
docker exec -it puppet-agent2 puppet agent -t
```

## Common Operations

- Show server logs: `docker logs -f puppet`
- Show agent logs: `docker logs -f puppet-agent1` (or `puppet-agent2`)
- Force agent run: `docker exec -it puppet-agent1 puppet agent -t`
- Inspect last run: `docker exec -it puppet-agent1 puppet last run`
- Bring all up: `docker compose up -d`
- Stop all: `docker compose down`
- Reset everything (includes volumes): `docker compose down -v`

## Networking & Hostnames

- The server’s hostname is `puppet`, which agents use via `puppet config set server puppet`.
- Agents use FQDN certnames (`agent1.example.test`, `agent2.example.test`) to match `autosign.conf`.

## Image Versions

This project uses `:latest` tags for simplicity. For stability, pin versions:

```
image: puppet/puppetserver:8
image: puppet/puppet-agent:8
```

## Troubleshooting

- Server not ready: Give it 1–2 minutes on first boot, watch `docker logs -f puppet`.
- Cert wait timeouts: If autosign is disabled, sign certs manually (see above).
- Permission issues on code bind mount: Ensure the repo is readable by Docker on your host.
- Low memory: Increase `PUPPETSERVER_JAVA_ARGS` (e.g., `-Xmx1g`) if you see OOM or GC pressure.

## Security Notes

- Do not use autosign in production. Prefer manual signing and RBAC.
- Use proper DNS/FQDNs, pin image versions, and consider PuppetDB for real environments.

---

Happy Puppeting!
