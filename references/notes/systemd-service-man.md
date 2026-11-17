---
source: systemd-service-man
read_by: agent
date: 2026-11-17
sections_read: ["Description", "Options: Type=", "ExecStart=", "ExecStartPre=/ExecStartPost=", "ExecReload=", "ExecStop=", "ExecStopPost=", "RestartSec=", "TimeoutStartSec=", "TimeoutStopSec=", "Restart=", "RestartMode=", "SuccessExitStatus=", "RestartForceExitStatus=", "Sockets=", "FileDescriptorStoreMax=", "Examples (Example 3 Simple service, Example 4 Oneshot service)"]
---

# Notes: systemd.service, Service unit configuration

> Notes are in English and in your own words. Do not copy source sentences. Every point gives its location.
> Read on 2026-11-17 via `curl` on the raw HTML (the page is about 75 KB of text); directive names, defaults and behavior below were checked there. The page header shows "systemd 262". Not read in detail: ExitType=, PIDFile=, watchdog and notification-access options, credentials/OOM options, Examples 5 onward, and the companion man pages (systemd.unit, systemd.exec, systemd.kill), where the start-rate limit, Environment/EnvironmentFile and signal/kill details are defined.

## Key points

- (Description) A .service unit describes a process that systemd starts and supervises. Service-specific options are in the [Service] section; common options are in [Unit] and [Install] (defined in systemd.unit); execution environment is in systemd.exec; how processes are killed is in systemd.kill.
- (Type=) Type= says how systemd decides that start-up is finished. Types: simple, exec, forking, oneshot, dbus, notify, notify-reload, idle. The default is simple when ExecStart= is set and no Type= or BusName= is given.
- (Type=simple) The unit counts as started right after fork, before the binary is even executed. As a consequence, `systemctl start` reports success even if the binary is missing or the configured User= does not exist.
- (Type=exec) Counts as started after the binary has been executed successfully, so those errors are reported as failure. The page recommends exec for long-running services (it notes that it still cannot tell whether the program's own initialization worked).
- (Type=notify, notify-reload, dbus, forking) For when the program itself must signal readiness: notify (service sends a readiness message through sd_notify), dbus (a bus name is acquired), forking (traditional daemon where the parent exits when ready; use is discouraged by the page). These need support in the program, except forking. notify-reload also defines a reload protocol where systemd sends SIGHUP and waits for the service to report that reloading has finished.
- (Type=oneshot) For commands that run to completion (cleanup, migration-like jobs); the unit is considered up after the process exits and, without RemainAfterExit=, ends as "dead" rather than "active". It is the only type that can have several ExecStart= lines (Example 4). Restart=always and Restart=on-success are rejected for it.
- (ExecStart=) Exactly one command for non-oneshot units; the process is the main process unless Type=forking. If several commands exist (oneshot) they run in order and a failure stops the rest (a leading "-" on a command ignores its failure).
- (ExecStartPre=/ExecStartPost=) Extra commands before/after ExecStart=, run serially; if one fails (and has no "-"), the rest is skipped and the unit is failed. This is the place the page offers for pre-start steps (the page does not suggest database migration; that is our inference and must be labelled as design choice, not source fact).
- (ExecReload=) Optional command to ask the service to reload its configuration without a restart; $MAINPID is available. The page warns that "kill -HUP $MAINPID" is asynchronous (it returns before the reload is finished) and recommends either Type=notify-reload or a command that waits for completion. A reload that times out (TimeoutStartSec= also covers reloads) is a failed reload and the service keeps running with the old configuration.
- (ExecStop=, ExecStopPost=) ExecStop= runs commands that ask the service to stop cleanly; the page says the command should wait until the service has actually stopped, because the remaining processes are killed right after it exits (per KillMode=). ExecStop= runs only if the service started successfully; ExecStopPost= runs afterwards in all cases, including failed starts, and is for clean-up. If no ExecStop= is given, systemd sends the stop signal (SIGTERM by default, see systemd.kill; the Simple-service example confirms SIGTERM followed by SIGKILL after a timeout).
- (ExecStop=, last paragraph) A service restart is implemented as stop then start, and ExecStop=/ExecStopPost= run during it. This is the page's basis for "a restart has a gap in which the service is down."
- (TimeoutStopSec=) Time allowed for ExecStop= commands and for the service to exit after the stop signal; after that, SIGKILL. Default comes from the manager setting DefaultTimeoutStopSec= (value not stated on this page).
- (TimeoutStartSec=) Time allowed for start-up (and reloads); failing means the service is considered failed. Default from DefaultTimeoutStartSec=; disabled by default for oneshot.
- (Restart=) Values: no (default), on-success, on-failure, on-abnormal, on-watchdog, on-abort, always. A stop or restart requested through systemd never triggers an automatic restart, and the same goes for systemctl stop. The page recommends on-failure for long-running services so that crashes are retried automatically; always also restarts after a clean exit. The page includes a table of exit causes (clean exit, unclean exit code, unclean signal, timeout, watchdog, OOM) against each setting.
- (Restart=, RestartSec=) Restarts are subject to start rate limiting (StartLimitIntervalSec= and StartLimitBurst=, defined in systemd.unit); the delay before a restart is RestartSec=, default 100 ms.
- (SuccessExitStatus=, RestartForceExitStatus=) Lets you define extra exit codes that count as success or that force a restart; useful when an app exits with a special code on purpose.
- (RestartMode=) normal restarts through the failed/inactive state; direct goes straight to activating and skips failed state, which avoids dependent units reacting to a short failure (added in version 254).
- (Sockets=, ExecStart= notes on Type=simple) Systemd can create and hold the listening socket (socket activation) and hand it to the service; the page mentions socket activation as the way to have communication channels ready before the service starts (under Type=simple) and in Sockets=. It does not state that this removes downtime during deploys; that inference must be checked against systemd.socket docs or tested.
- (FileDescriptorStoreMax=) Lets a service park open file descriptors (for example sockets) with systemd so it can restart after a request or crash without losing them; the default is 0 (none). The service has to use the sd_notify FDSTORE protocol.
- (Examples 3) Minimal unit: [Unit] Description, [Service] ExecStart=/path, [Install] WantedBy=multi-user.target; with no ExecStop=, systemd sends SIGTERM and, after a timeout, SIGKILL.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Restart= default is no; recommended value for long-running services is on-failure | Restart= | Directive names and values confirmed on the raw page |
| RestartSec= default is 100 ms | RestartSec= | |
| Type= default is simple when ExecStart= is given without Type= or BusName= | Type= | Version-sensitive; check against the target distro's systemd |
| Type=simple reports start success right after fork, even if the binary is missing; Type=exec reports failure | Type=simple and Type=exec paragraphs | Good misconception material ("service started" does not mean "app is working") |
| Restart is stop followed by start | ExecStop= (last paragraph) | Short outage window for a naive restart |
| Reload timeout leaves the old configuration running | TimeoutStartSec= (note on reloads) | |
| Start-up and stop timeouts defaults come from DefaultTimeoutStartSec=/DefaultTimeoutStopSec= | TimeoutStartSec=, TimeoutStopSec= | Actual numbers are not on this page |
| FileDescriptorStoreMax= default is 0 | FileDescriptorStoreMax= | |
| Page version shown: systemd 262 | Page header | Options carry "Added in version N" notes, e.g. RestartMode= in 254, ExitType= in 250 |

## Relevant to concepts

- `simple-deploys` objective 1 (write the steps to deploy a new version, including database migration and rollback): NOT supported by this source beyond the "stop/start/reload the process" step. The page has no notion of releases, migrations, version switching or rollback. It supplies what a deploy script would call at the process level (systemctl restart/reload, ExecStartPre= for pre-start steps, Type=oneshot for run-to-completion jobs) and what can go wrong there (start reported successful for a missing binary under Type=simple). Migration and rollback steps must come from capistrano-docs-rollbacks, fowler-bluegreen-deployment and twelve-factor-app (and probably a migration source that is not currently mapped).
- `simple-deploys` objective 2 (explain why a direct deploy to one server causes brief downtime and how to reduce it): supported in part. The ExecStop= paragraph says a restart is stop then start (a gap), TimeoutStopSec= and Type= describe how long that gap can be, and ExecReload=/Type=notify-reload, Sockets= and FileDescriptorStoreMax= are the on-box mechanisms for reload or keeping sockets across a restart. The blue-green source is needed for the "second copy of the app" way. The page never uses the words "downtime" or "zero-downtime"; the link to deploys is our inference.
- `simple-deploys` objective 3 (separate configuration from code, twelve-factor): essentially not covered in the sections read. Environment variables in unit files appear only in the "Command lines" substitution examples (Environment=, not read in detail); the relevant directives (Environment=, EnvironmentFile=) are defined in systemd.exec, which was not opened. Use twelve-factor-app for this objective.
- `simple-deploys` (supervision aspect): supports "who restarts the app when it crashes" (Restart=on-failure with RestartSec=), process type choice, and a clean stop (SIGTERM, timeout, SIGKILL). Connects to the point in app-plus-database that process state is lost on restart.

## Warnings

- Reference manual, not a tutorial; NO-DATE and NO-AUTHOR; all-rights-reserved (see registry). Beginners need a guided path: Type= (simple vs exec), Restart=on-failure, ExecStart/ExecStop, TimeoutStopSec. Unit examples in a lesson must be written by us, not copied.
- Version-dependent: the page is systemd 262 and many options are marked "Added in version ...". RestartMode= (254), ExecReloadPost= (259) and ExitType= (250) carry such notes, so they may be missing on older systemd. Which version a given distribution ships was not checked. Check the target distribution version before putting such options in a lab.
- The signal sent by default on stop and the kill behavior (KillMode=, KillSignal=) are defined in systemd.kill, not on this page; only the Example 3 text says SIGTERM then SIGKILL after a timeout.
- Restart= has no effect when the stop is requested via systemd. Restarts are subject to a start rate limit (StartLimitIntervalSec=, StartLimitBurst=); what happens when it is hit and the limit values are in systemd.unit and were not read.
- Type=simple can mislead: success of `systemctl start` does not prove the app is up (see Type=simple/exec). Likewise "active" does not mean the app is ready or healthy; for readiness use notify or an external health check (see basic-monitoring).
- The Restart= effect table on the HTML page uses check-mark cells that were hard to read when converted to text; the prose above it was used instead, and a lesson should consult the page directly if a table claim is needed.
