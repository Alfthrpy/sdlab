---
source: aws-route53-how-dns-routes-traffic
read_by: agent
date: 2026-11-17
sections_read: ["intro", "Overview of how you configure Route 53 (records: name, type, value)", "How Amazon Route 53 routes traffic for your domain (the step list)"]
---

# Notes: How internet traffic is routed to your website or web application (Amazon Route 53 Developer Guide)

> Notes are in English and in your own words. Page fetched with curl on 2026-11-17 (static HTML text). The footer is not part of the static HTML (the page is rendered by script), so the license could not be seen there; the registry treats it as all-rights-reserved. No date on the page.

## Key points

- (intro) Computers talk using IP addresses (IPv4 like 192.0.2.44, IPv6 like 2001:0db8:...); a DNS service maps a human-friendly domain name to the address.
- (configuration overview) You register a domain, which creates a hosted zone; then you add records. A record has a name (the domain or subdomain), a type (A for an IPv4 web server, MX for mail servers, among others) and a value (the IP address or server names). Alias records point to some AWS resources.
- (How Route 53 routes traffic: the nine steps, "in a few milliseconds") The browser gets a typed name; the request goes to a DNS resolver, usually run by the ISP or a company network; the resolver asks a root name server, then a name server for the top-level domain (.com), which answers with the names of the name servers responsible for the domain; the resolver caches those name server names (typically two days, per the page); it asks one of them for the record and gets the IP address; it returns the address to the browser, and caches the address for the record's time to live (TTL). Only then does the browser send its HTTP request to that IP, and the web server returns the page.
- (note box) The cache means a later lookup skips the walk through root and TLD servers, and for repeats within the TTL it skips the whole lookup. This is what makes DNS cheap on most requests and slow on the first one.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| DNS resolution is a chain: resolver, root server, TLD server, the domain's own name server, then the answer returned to the browser | step list | Vendor wording (Route 53 name servers), generic process |
| Name server delegation is cached by the resolver, typically two days; the final IP answer is cached for the record's TTL | step 5 and note after step 8 | |
| The page describes the whole process as happening "in a few milliseconds" | lead-in to the step list | A loose claim, no measurement; do not cite as a timing figure |
| The browser sends the HTTP request only after it has the IP | step 9 | Gives the order DNS before TCP/TLS/HTTP |

## Relevant to concepts

- `request-lifecycle` (unit 0), objective 1: SUPPORTS the DNS stage in the diagram (what is looked up, who answers, why it is cached). 
- `request-lifecycle`, objective 2: PARTLY: it says DNS is quick and cached but gives no numbers; a DNS stage in a timing scenario is the author's own (or a measured value from `mdn-navigation-resource-timings` style data).
- Unit 2 (DNS, load balancing by DNS): base explanation.

## Warnings

- Vendor documentation; uses Route 53 terms (hosted zone, alias record) not needed for Unit 0.
- The "TTL" section the page links to was not opened.
- The two-day cache claim is the page's, for the delegation to name servers; the TTL of the final record is set by the domain owner ("an amount of time that you specify"), and the page gives no typical value.
