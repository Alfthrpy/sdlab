---
source: mdn-http-overview
read_by: agent
date: 2026-11-17
sections_read: ["Introduction", "Components of HTTP-based systems (Client, Web server, Proxies)", "Basic aspects of HTTP", "What can be controlled by HTTP", "HTTP flow", "HTTP messages", "APIs based on HTTP (skimmed)"]
---

# Notes: Overview of HTTP (MDN Web Docs)

> Notes are in English and in your own words. Read in full via WebFetch and confirmed against the raw page with curl (page text, "last modified Oct 8, 2026"). Page footer license text was not re-read in this session (license is recorded in the registry from MDN's attribution page).

## Key points

- (Introduction) HTTP is a request/response protocol between a client and a server. The client starts every exchange. A single web page is normally assembled from many separate resources (HTML, CSS, scripts, images), each fetched by its own request.
- (Introduction) HTTP runs at the application layer, on top of TCP (or TCP with TLS). It only needs a reliable transport underneath.
- (Components: Client) The client ("user-agent") is usually a browser, but can also be a crawler or a debugging tool. The browser fetches the HTML first, then issues further requests for the resources the page refers to.
- (Components: Web server) What looks like "the server" to the client may be one machine, several machines behind a load balancer, or software such as caches and databases sitting behind the front. Several server programs can share one machine, and with the `Host` header they can even share one IP address.
- (Components: Proxies) Between client and server there can be intermediaries (proxies) that relay messages. They are listed as doing caching, filtering, load balancing, authentication, and logging. A transparent proxy forwards unchanged; a non-transparent one may modify the message.
- (Basic aspects) HTTP is text-based and readable, extensible through headers, and stateless: two requests on the same connection are not linked by the protocol itself. Cookies are the mechanism that adds sessions on top, using headers.
- (Basic aspects: connections) Opening a TCP connection takes several round trips, so opening one per request is wasteful. HTTP/1.1 added persistent connections (controlled by the `Connection` header) and pipelining (hard to deploy); HTTP/2 multiplexes many messages on one connection; QUIC (UDP-based) is mentioned as experimental.
- (HTTP flow) Four steps: open (or reuse) a TCP connection, send the request message, read the response, then close or reuse the connection.
- (HTTP messages) A request has a method, a path, a version, optional headers, and an optional body. A response has a version, a status code, a status message, headers, and an optional body. In HTTP/2 these are carried in binary frames, but the meaning is unchanged.
- (What can be controlled) Caching, relaxing the same-origin restriction, authentication, proxying/tunneling, and sessions are all negotiated through headers.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| HTTP flow has 4 steps (connect, send request, read response, close/reuse) | HTTP flow | Useful skeleton for the HTTP part of a request timeline |
| A request message has 5 parts; a response message has 5 parts | HTTP messages | Method, path, version, headers, body / version, status code, status message, headers, body |
| Setting up a TCP connection needs several round trips (no exact number given) | Basic aspects: HTTP and connections | Exact round-trip counts are not on this page; see mdn-tcp-handshake-glossary and mdn-http-connection-management-1x for Unit 2 |
| HTTP/1.0 used one TCP connection per request/response pair; HTTP/1.1 added persistent connections and pipelining; HTTP/2 multiplexes | Basic aspects: HTTP and connections | Version history only, no performance numbers |
| Proxy functions listed: caching, filtering, load balancing, authentication, logging | Components: Proxies | |
| Page last modified Oct 8, 2026 | page footer | Matches registry `published` |

## Relevant to concepts

- `request-lifecycle` (unit 0), objective 1 (draw the order of stages from browser to database and back): partly supported. The page supports the client -> (proxy) -> web server -> response part, the 4-step HTTP flow, and the point that one page load means many requests. It does NOT cover DNS, TLS, the application code, or the database, so the lesson needs other sources for the "to the database and back" half.
- `request-lifecycle`, objective 2 (decide which stage is likely slowest from per-stage timing data): NOT supported. There are no timings or latency guidance on this page. The only hint is that new TCP connections cost several round trips.
- `dns-networking-basics` (unit 2, mapped in concepts.yaml but outside this ticket): supports the keep-alive/persistent-connection explanation (objective 3) qualitatively; it gives no round-trip numbers for objective 2.
- `stateless-services-sessions` (unit 2, not mapped to this source): the "stateless but not sessionless" section is a handy definition if the writer wants one.

## Warnings

- This is a vocabulary and orientation page. The HTTP/3 transport is not described; QUIC is called "experimental", which is dated wording for 2026. Do not cite it for current HTTP/3 status.
- The sample response uses 2009/2010 dates; they are only examples, not facts.
- The page describes only the HTTP part of a request's life, as the registry note also says.
- Proxy functions are listed without detail; for reverse proxy behavior (buffering, header rewriting) use nginx-reverse-proxy-admin-guide.
