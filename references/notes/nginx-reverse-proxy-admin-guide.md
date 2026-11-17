---
source: nginx-reverse-proxy-admin-guide
read_by: agent
date: 2026-11-17
sections_read: ["Introduction", "Passing a Request to a Proxied Server", "Passing Request Headers", "Configuring Buffers", "Choosing an Outgoing IP Address"]
---

# Notes: NGINX Reverse Proxy (NGINX Documentation, Admin Guide)

> Notes are in English and in your own words. The whole page was read via WebFetch and re-checked against the raw HTML with curl (directive names and values below are from the raw page). The page shows a banner saying the NGINX docs are moving to docs.f5.com, and has no version or date; footer is "(c) 2026 F5, Inc.".

## Key points

- (Introduction) Proxying is used to spread load over several servers, to show content from different sites under one address, and to hand requests to application servers over non-HTTP protocols.
- (Passing a Request) When NGINX proxies, it does three things: forwards the request to the proxied server, fetches the response, sends it back to the client. This is the middle of the request path: client -> NGINX -> application -> (database) -> back.
- (Passing a Request) For an HTTP backend, `proxy_pass` goes inside a `location` block. The backend can be a domain, an IP, or IP with port, for example an app listening on `127.0.0.1:8000` on the same machine.
- (Passing a Request) If the `proxy_pass` address carries a URI, that URI replaces the part of the request path that matched the `location`; without a URI the full request path is passed on.
- (Passing a Request) For non-HTTP backends, there are matching directives: `fastcgi_pass`, `uwsgi_pass`, `scgi_pass`, `memcached_pass`. `proxy_pass` can also point to a named group of servers, in which case requests are distributed among them (load balancing, covered on a separate page).
- (Passing Request Headers) By default NGINX rewrites two headers on the way to the backend: `Host` becomes the proxy-host value and `Connection` becomes `close`; headers with empty values are dropped. `proxy_set_header` changes this; typical use is passing the original host (`$host`) and client address (`$remote_addr`, e.g. as `X-Real-IP`) so the application is not blind to who the client is. Setting a header to an empty string stops it from being forwarded.
- (Configuring Buffers) Response buffering is on by default: NGINX holds the complete response from the backend before sending it to the client. The benefit is that a slow client does not keep a backend worker busy; the backend hands the response off quickly. `proxy_buffering off` sends data to the client as it arrives, which suits fast interactive clients.
- (Configuring Buffers) `proxy_buffers` sets number and size of buffers; `proxy_buffer_size` sets the buffer for the first part of the response (the headers), which can be smaller.
- (Choosing an Outgoing IP Address) `proxy_bind` selects the source IP on a multi-interface host. Marginal for this course.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Default: `proxy_buffering` is on | Configuring Buffers | Whole backend response is buffered before it goes to the client |
| Default header changes: `Host` set to `$proxy_host`, `Connection` set to `close` | Passing Request Headers | Example of what a proxy changes in the message |
| Supported non-HTTP backend protocols: FastCGI, uwsgi, SCGI, memcached | Passing a Request to a Proxied Server | |
| Example buffer settings `proxy_buffers 16 4k;` and `proxy_buffer_size 2k;` | Configuring Buffers | Docs example values, not recommendations |

## Relevant to concepts

- `request-lifecycle` (unit 0), objective 1 (draw the stages): supports the reverse-proxy stage (client -> proxy -> app on a local port -> response back through the proxy) and the idea that a proxy can change headers and buffer responses. It does not cover DNS, TLS, or the database stage, so it supports one box in the diagram only.
- `request-lifecycle`, objective 2 (find the slowest stage from timing data): only indirectly supported. The buffering explanation gives a reason why a slow client does not slow the application, which helps interpret "time at proxy vs time at app", but the page has no timings, log variables, or diagnosis steps.
- `load-balancer-reverse-proxy` (unit 2, outside this ticket): supports the reverse-proxy-function half of objective 1 (routing, buffering). TLS termination is NOT on this page (it is a separate NGINX page, "NGINX SSL Termination", listed in the sidebar but not opened). The load-balancing algorithms of objective 2 and health checks of objective 3 are on other pages.

## Warnings

- Vendor documentation of NGINX Plus/Open Source; some sidebar items are NGINX Plus-only. Only the directives on this page are described here, and they exist in open source NGINX.
- No version or date on the page, and a notice that the docs are moving to docs.f5.com, so the URL may change.
- `Connection: close` as the default to the backend means no keep-alive to the upstream unless configured otherwise (a related setting is on the NGINX HTTP load balancing / upstream pages, not read here). Do not claim keep-alive behavior from this page.
- The page does not mention `X-Forwarded-For`; only `X-Real-IP` appears in the example. Do not attribute `X-Forwarded-For` advice to it.
- Beginner's guide at nginx.org remains unverified (not opened here).
