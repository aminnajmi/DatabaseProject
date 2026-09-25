# Graph Report - VPSHostingSystem  (2026-09-25)

## Corpus Check
- Corpus is ~2,628 words - fits in a single context window. You may not need a graph.

## Summary
- 82 nodes · 184 edges · 19 communities (8 shown, 11 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Database Authentication Helpers
- Application Database Integration
- Domain Management Operations
- VPS Server Operations
- Administration and Configuration
- Customer Billing and Support
- Route Access Control
- Flask Application Startup
- Hosting Dashboard Metrics
- Flask Dependency Setup
- Domain Assignment Workflow
- SQL Reporting
- MySQL Connectivity
- Route Blueprint Registration
- Additional Route Handlers
- Additional Route Handlers
- Record Status Actions
- Record Deletion Actions

## God Nodes (most connected - your core abstractions)
1. `login_required()` - 26 edges
2. `execute_query()` - 22 edges
3. `fetch_all()` - 17 edges
4. `fetch_one()` - 11 edges
5. `VPS Hosting Management System` - 10 edges
6. `edit()` - 7 edges
7. `index()` - 6 edges
8. `edit()` - 6 edges
9. `index()` - 6 edges
10. `get_connection()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Raw SQL CRUD` --conceptually_related_to--> `Invoice Management`  [INFERRED]
  README.md → templates/invoices.html
- `Raw SQL CRUD` --conceptually_related_to--> `Support Ticket Workflow`  [INFERRED]
  README.md → templates/tickets.html
- `Raw SQL CRUD` --conceptually_related_to--> `User Management`  [INFERRED]
  README.md → templates/users.html
- `Raw SQL CRUD` --conceptually_related_to--> `VPS Lifecycle Management`  [INFERRED]
  README.md → templates/vps.html
- `create_app()` --calls--> `ensure_default_admin()`  [EXTRACTED]
  app.py → database.py

## Import Cycles
- None detected.

## Communities (19 total, 11 thin omitted)

### Community 0 - "Database Authentication Helpers"
Cohesion: 0.18
Nodes (12): fetch_one(), get_connection(), Return a new MySQL connection using environment-based configuration., login(), logout(), route, index(), count() (+4 more)

### Community 1 - "Application Database Integration"
Cohesion: 0.38
Nodes (5): flask, functools, mysql_connector, missing_fields(), index()

### Community 2 - "Domain Management Operations"
Cohesion: 0.54
Nodes (7): execute_query(), add(), assign(), delete(), index(), route, unassign()

### Community 3 - "VPS Server Operations"
Cohesion: 0.46
Nodes (7): fetch_all(), index(), route, edit(), index(), options(), route

### Community 4 - "Administration and Configuration"
Cohesion: 0.33
Nodes (6): Administrator Authentication, Environment Configuration, Parameterized SQL Queries, VPS Hosting Management System, Shared Admin Shell, Administrator Login

### Community 5 - "Customer Billing and Support"
Cohesion: 0.40
Nodes (5): Raw SQL CRUD, Invoice Management, Support Ticket Workflow, User Management, VPS Lifecycle Management

### Community 6 - "Route Access Control"
Cohesion: 0.50
Nodes (4): login_required(), delete(), post, status()

### Community 7 - "Flask Application Startup"
Cohesion: 0.67
Nodes (3): create_app(), ensure_default_admin(), os

## Knowledge Gaps
- **13 isolated node(s):** `Parameterized SQL Queries`, `Environment Configuration`, `Flask Dependency`, `MySQL Connector Dependency`, `Shared Admin Shell` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 26 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `login_required()` connect `Route Access Control` to `Database Authentication Helpers`, `Application Database Integration`, `Domain Management Operations`, `VPS Server Operations`, `Additional Route Handlers`, `Additional Route Handlers`, `Record Status Actions`, `Record Deletion Actions`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `execute_query()` connect `Domain Management Operations` to `Database Authentication Helpers`, `Application Database Integration`, `VPS Server Operations`, `Route Access Control`, `Flask Application Startup`, `Additional Route Handlers`, `Additional Route Handlers`, `Record Status Actions`, `Record Deletion Actions`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Why does `VPS Hosting Management System` connect `Administration and Configuration` to `Customer Billing and Support`, `Hosting Dashboard Metrics`, `Flask Dependency Setup`, `Domain Assignment Workflow`, `SQL Reporting`, `MySQL Connectivity`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **What connects `Parameterized SQL Queries`, `Environment Configuration`, `Flask Dependency` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._