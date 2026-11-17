---
source: mysql-84-optimization-indexes
read_by: agent
date: 2026-11-17
sections_read: ["10.3 Optimization and Indexes (landing page: intro text and subsection list)", "10.3.1 How MySQL Uses Indexes (extra page, not the registry URL)", "10.3.7 Verifying Index Usage (extra page, not the registry URL)"]
---

# Notes: MySQL 8.4 Reference Manual, 10.3 Optimization and Indexes

> Notes are in English and in your own words. The registry URL is the 10.3 landing page, which is only one short paragraph plus a table of subsections. Because that is too thin to teach from, two subsection pages (10.3.1 and 10.3.7) were also opened on 2026-11-17 and are marked "(10.3.1)" / "(10.3.7)" below. All three were read as raw HTML via `curl` and via text extraction. The other subsections (10.3.2 to 10.3.6, 10.3.8 to 10.3.14) were NOT read; only their titles were seen.

## Key points

- (10.3, intro) The main way to speed up SELECTs is to create indexes on the columns that the query tests. Index entries work like pointers to table rows, so the server can find matching rows for the WHERE clause without scanning.
- (10.3, intro) Any MySQL data type can be indexed.
- (10.3, intro) Indexing every column that appears in some query is tempting but wasteful: unnecessary indexes use space and make the optimizer spend time choosing among them.
- (10.3, intro) Indexes also add cost to INSERT, UPDATE, and DELETE because every index has to be updated; the job is to find a balanced set that makes queries fast without excess.
- (10.3.1) Without an index MySQL starts at the first row and reads the whole table, so the cost grows with table size; with an index it can jump to the right position in the data.
- (10.3.1) Most index kinds (PRIMARY KEY, UNIQUE, INDEX, FULLTEXT) are stored as B-trees. Exceptions: spatial indexes use R-trees; MEMORY tables can use hash indexes; InnoDB FULLTEXT uses inverted lists.
- (10.3.1) Uses of indexes listed: find rows for a WHERE clause; discard rows from consideration (when several indexes could apply, the optimizer normally picks the most selective one, i.e. the one that leaves the fewest rows); fetch rows from other tables in joins; get MIN/MAX of an indexed column; sort or group on a leftmost prefix of an index.
- (10.3.1) A multiple-column index can be used for any leftmost prefix: an index on (col1, col2, col3) can serve lookups on col1, on col1+col2, or on all three.
- (10.3.1) Comparing columns of different type, size, or character set can stop an index from being used (example given: utf8mb4 vs latin1 column, or comparing a string column to a number, since one number can equal many different strings).
- (10.3.1) A covering index (the index holds every column the query needs) lets MySQL answer from the index tree without reading the table rows.
- (10.3.1) Indexes matter less for small tables, and for large tables where a report reads most rows; in that case sequential reading beats following an index.
- (10.3.7) The manual's whole advice here is: check that your queries really use the indexes you created, using EXPLAIN (the details are in section 10.8.1, not read).

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Index on (col1, col2, col3) is usable for (col1), (col1, col2), (col1, col2, col3) | 10.3.1 | Leftmost-prefix rule; matches use-the-index-luke concatenated keys |
| Each index must be updated on insert, update, delete | 10.3 intro | Qualitative only: no measurements or numbers given |
| Most MySQL indexes are B-trees (spatial = R-tree, MEMORY = hash allowed, InnoDB FULLTEXT = inverted list) | 10.3.1 | |
| Optimizer normally picks the most selective index when several apply | 10.3.1 | "Selective" = finds fewest rows |
| Page version label: MySQL 8.4; legal footer (c) 2026 Oracle | page header/footer | Version selector on the page also lists 9.7 as current |

## Relevant to concepts

- `indexes-query-basics`, per objective:
  - Obj. 1 (read EXPLAIN output and decide index vs full scan): only weakly supported. 10.3.7 just tells the reader to use EXPLAIN; it does not show or explain any output columns. The MySQL EXPLAIN output format (10.8.x) is a separate section that was not read. Pair with use-the-index-luke (which shows MySQL `type` values such as const and ref next to other databases) and pg-docs-using-explain.
  - Obj. 2 (choose which column deserves an index for a slow query): partly supported. 10.3.1 gives selection principles (index the columns the query tests, selective index preferred, leftmost-prefix rule, type/charset must match, small tables and large scans gain little). It gives no worked example of picking a column for a given slow query.
  - Obj. 3 (explain the cost of an index on write operations): supported only at the one-sentence level (10.3 intro). There is no explanation of why (tree maintenance) and no numbers; use use-the-index-luke "Modifying Data" for the why.
- This is the MySQL counterpart to pg-docs-indexes-intro; use it where the lesson needs to say "MySQL behaves the same / differently".

## Warnings

- The registry URL is only the landing page of the section; most useful content lives in subsections that were not read. Do not cite "10.3" for details that are actually in 10.3.5 to 10.3.14.
- Manual text for 8.4 only. The version selector shows 9.7 as the current series, so details can differ in newer or older versions.
- Product-specific: the storage-engine remarks (MyISAM, MEMORY, InnoDB clustered primary key) are MySQL details and should not be generalized to PostgreSQL.
- No author or date on the page (corporate documentation, versioned manual).
