---
source: mdn-tcp-handshake-glossary
read_by: agent
date: 2026-11-17
sections_read: ["whole glossary entry (about 250 words)"]
---

# Notes: TCP handshake (MDN Web Docs Glossary)

> Notes are in English and in your own words. Page fetched with curl on 2026-11-17 (raw HTML, main text extracted). Very short page.

## Key points

- (intro) TCP sets up a connection with a three-message exchange (SYN, SYN-ACK, ACK) and ends it with a four-message exchange (FIN and ACK in each direction).
- (setup steps) The initiator (usually the browser) sends a SYN; the server answers with SYN-ACK; the initiator sends an ACK; then the connection is established. The purpose is to let both machines agree on connection parameters before any data, such as an HTTP request, is sent.
- (placement) The page states where it sits in a secure web request: after the DNS lookup and before the TLS handshake.
- (teardown) Each side can close its half independently with FIN and ACK; the connection can be half-closed while the other side still sends data.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Order for a secure web request: DNS lookup, then TCP handshake, then TLS handshake | "after a DNS lookup and before the TLS handshake" paragraph | The one sentence that fixes the order of the three early stages; there is no timing |
| TCP setup is three messages (SYN, SYN-ACK, ACK); teardown is four | intro, steps | The page does not say how many round trips this costs; see `mdn-http-connection-management-1x` for the cost of setting up a connection per request |

## Relevant to concepts

- `request-lifecycle` (unit 0), objective 1: SUPPORTS the order DNS then TCP then TLS before the HTTP request. Combined with `aws-route53-how-dns-routes-traffic` (DNS) and `mdn-transport-layer-security` (TLS) and `mdn-http-overview` (HTTP), the pre-server stages are covered.
- `connection-pooling` (unit 0), objective 1: indirect, it names the setup steps a new connection needs (the database connection setup itself is a different protocol; see the pooling notes).

## Warnings

- Generic networking glossary; it says nothing about databases. Do not use it to claim that a database connection costs a TCP handshake plus authentication; that needs a database source.
- Very short. One sentence is the main use.
