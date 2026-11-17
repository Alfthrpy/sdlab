---
source: twelve-factor-app
read_by: agent
date: 2026-11-17
sections_read: ["Introduction", "Background", "The Twelve Factors (index page)", "III. Config", "IV. Backing services", "V. Build, release, run", "VI. Processes", "IX. Disposability", "X. Dev/prod parity", "XII. Admin processes"]
---

# Notes: The Twelve-Factor App

> Notes are in English and in your own words. Pages read via curl on the raw HTML (the site is static and short). Not read: I Codebase, II Dependencies, VII Port binding, VIII Concurrency, XI Logs, and the Background-only "Who should read" detail beyond the index. Footer on every page: "Written by Adam Wiggins, Last updated 2017" and "(c) Copyright 2026 Salesforce, Inc. All rights reserved."

## Key points

- (Introduction) It is a methodology for web apps delivered as a service, aimed at portability between environments, minimal gap between development and production, and the ability to scale without re-architecting. The authors draw on the Heroku platform experience (Background).
- (III Config) "Config" means anything that differs between deploys: database and cache addresses, third-party credentials, per-deploy values like hostname. It must be strictly separate from code and is stored in environment variables. Litmus test given: could the repository be made public at any time without leaking credentials?
- (III Config) Internal config that does not change between deploys (for example routing tables) is fine in code. Untracked config files are an improvement over constants in code but are easy to commit by mistake and get scattered in different formats. Named "environment" groups (development, staging, ...) do not scale; each variable is managed independently per deploy.
- (IV Backing services) Database, queue, cache, mail service: all are attached resources reached by a URL or credentials from config. Swapping a local database for a managed one, or attaching a database restored from backup to replace a failing one, should need only a config change.
- (V Build, release, run) A deploy goes through three stages: build (code to an executable bundle), release (build plus the deploy's config), run (processes launched from a release). Releases get unique ids and cannot be changed after creation, so a rollback means running a previous release. Capistrano's `releases` directory with a symlink to the current one is given as an example. The run stage should be as simple as possible because it can start automatically (reboot, crash restart) with no developer present.
- (VI Processes) Processes are stateless and share nothing; anything that must persist goes to a backing service such as a database. Memory or local disk can serve as a short cache within one request or job, but nothing may be assumed to be there for the next request, and a restart (deploy, config change, relocation) wipes local state even with a single process. Sticky sessions violate this; session data belongs in a datastore with expiry such as Memcached or Redis.
- (IX Disposability) Processes should start fast (a few seconds) and shut down gracefully on SIGTERM: a web process stops accepting new connections, finishes current requests, then exits. Worker processes return the current job to the queue, which requires jobs to be safe to repeat. Processes should also survive sudden death.
- (X Dev/prod parity) Keep time gap (deploy within hours), personnel gap (authors take part in deploying) and tools gap (same database type and version in every environment) small. The page specifically argues against SQLite locally and PostgreSQL in production, even behind an adapter layer, because small incompatibilities only show up in production.
- (XII Admin processes) One-off tasks such as database migrations, a console, or one-time scripts run as separate processes against the same release, code, and config as the app, not from a separate copy of the code.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| The methodology has 12 factors (Codebase ... Admin processes) | The Twelve Factors index | |
| Startup should ideally take "a few seconds" | IX Disposability | Guidance, not a measured number |
| Web process graceful shutdown: stop listening, finish in-flight requests, exit; triggered by SIGTERM | IX Disposability | Assumes requests are short (a few seconds at most) |
| Release ids: timestamp or incrementing number (examples given), releases are append-only | V Build, release, run | Basis for a rollback step in a deploy runbook |
| Traditional vs twelve-factor table: deploy interval weeks vs hours; authors and deployers different vs same people | X Dev/prod parity | Opinionated claim of the authors, not data |
| Migrations (`manage.py migrate`, `rake db:migrate`) given as admin-process examples | XII Admin processes | |

## Relevant to concepts

- `simple-deploys` (unit 0), objective 3 (separate config from code per twelve-factor): directly supported by III Config (definition, env vars, litmus test) and IV (config as the place for resource handles).
- `simple-deploys`, objective 1 (compose the deploy steps including migration and rollback): partly supported. V gives build/release/run and rollback by switching releases; XII says migrations run as a one-off process from the same release. The page does not describe the order of migration vs code switch, or backward-compatible migrations; those need another source (e.g. fowler-bluegreen-deployment, capistrano-docs-rollbacks).
- `simple-deploys`, objective 2 (explain why deploying directly to one server causes short downtime and how to reduce it): weakly supported. IX gives fast startup and graceful shutdown as ingredients, but the page never discusses single-server deploy downtime or zero-downtime techniques; use fowler-bluegreen-deployment and systemd-service-man.
- `app-plus-database` (unit 0), objective 2 (distinguish state in the database from state lost on app restart): directly supported by VI Processes (what is lost on restart, what must live in a backing service) and IV.
- `app-plus-database`, objective 1 (calculate that one app plus one database suffices): not supported (no numbers).
- `stateless-services-sessions` (unit 2, outside this ticket): VI (stateless processes, sticky sessions "should never be used") supports objective 1 and the sticky-session part of objective 2. It does not compare signed-cookie sessions with shared stores.

## Warnings

- Licensing is unresolved (see registry note): the site shows only a Salesforce copyright while the GitHub repo is MIT. Paraphrase only.
- Written around 2011-2012 for Heroku-style PaaS (last updated 2017). Tools named (Capistrano, Chef, Puppet, Vagrant, Beanstalkd, Jammit) are dated. On a plain VPS, "environment variables" is typically done through the process manager (for example systemd unit environment files); that translation is not on this page.
- The authors' claims about dev/prod parity and "stateless" are strong prescriptions. For example, a single-server app with a local SQLite file contradicts factor X; present it as one guideline, not as law.
- Factor VI says local disk may only be a short per-request cache. Many real apps store uploads on local disk; the guidance then is to move them to a backing service, but this page does not discuss object storage.
- The registry note says only the factor list page was read; this note records that the subpages listed above were also read in this session (a registry note update may be wanted).
