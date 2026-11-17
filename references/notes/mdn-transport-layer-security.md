---
source: mdn-transport-layer-security
read_by: agent
date: 2026-11-17
sections_read: ["Intro", "TLS handshake", "Configuring TLS", "Server authentication", "Mixed content (skimmed)", "Upgrading HTTP connections (skimmed)"]
---

# Notes: Transport Layer Security (TLS) (MDN Web Docs)

> Notes are in English and in your own words. Page fetched with curl on 2026-11-17 (raw HTML, main text extracted). Registry already records date (last modified 2026-02-28) and the MDN license; not re-derived here.

## Key points

- (Intro) TLS lets a client talk to a server safely over an untrusted network; HTTPS is HTTP over TLS. It gives three things: encryption (outsiders cannot read the traffic), integrity (changes in transit are detected), and authentication (each side can prove who it is; on the web mainly the server proves itself to the client).
- (Intro) HTTPS defends against a man-in-the-middle who sits between browser and server and could read and alter traffic. Browsers treat HTTPS pages as a "secure context", and many powerful web APIs only work there. The page's stance is that all sites should serve everything over HTTPS.
- (TLS handshake) Before application data flows, client and server run a handshake to set the security parameters: agree on the TLS version (1.3 is current and most used; 1.2 still seen; 1.1 and 1.0 should not be used), agree on a cipher suite (the algorithms for key agreement, authentication, encryption and message checks), optionally authenticate each other (client authentication is rare on the web, server authentication is fundamental), and agree on a secret key. After that, everything, including HTTP headers and bodies, is encrypted with that key.
- (Server authentication) A site needs a digital certificate: a signed copy of the public key tied to the domain name, so the browser knows it really reached that domain. Let's Encrypt is named as a widely used nonprofit certificate authority that issues free certificates. Many hosting services manage certificates for you.
- (Configuring TLS) Server TLS settings strongly affect security; Mozilla's recommended configurations and generator are pointed to.
- (Upgrading HTTP connections) A site served only over HTTPS should still redirect plain HTTP requests with a 301; this first request can be intercepted, so servers should also send a header (HSTS) so browsers use HTTPS from the start.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| TLS 1.3 (RFC 8446) is the current and most used version; TLS 1.0 and 1.1 should not be used | TLS handshake | |
| The handshake happens after the connection exists and before HTTP data; it settles version, cipher suite, authentication and a shared secret key | TLS handshake | The page does not say how many round trips this takes |

## Relevant to concepts

- `request-lifecycle` (unit 0), objective 1: SUPPORTS the TLS box in the stage diagram: what happens (agree on parameters, prove server identity with a certificate, derive a key) and where (after TCP, before the HTTP request). The order relative to TCP and DNS comes from `mdn-tcp-handshake-glossary`.
- `request-lifecycle`, objective 2: does not give any time for the handshake and does not mention round trips; use `web-dev-ttfb` and `mdn-navigation-resource-timings` for "TLS is a timed stage", and treat the number of round trips as outside the sources (or the author's own scenario).
- Unit 2 (load balancer, TLS termination): the base explanation.

## Warnings

- Beginner-level overview; it does not explain the key exchange and does not give timing. Do not claim "one round trip" or "two round trips" from this page.
- "Handshake happens after TCP" is stated on the TCP handshake glossary page, not here.
