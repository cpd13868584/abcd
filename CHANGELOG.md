# Changelog

## 0.1.0 — unreleased

- Scaffold: repo structure, portable `setup` (symlinks `abcd-*` into the host skills dir), MIT license, README.
- Shared references (`shared/references/`): `package-spec.md` (design-package contract + manifest schema), `method-abcd.md` (the ABCD method encoded — constitution, business-sequence rules, use-case spec template, analysis stripping, class-diagram linter, forward/reverse boundary), `diagram-syntax.md`, `conventions.md`.
- `/abcd-recover` + `/abcd-trace`: reverse flows implemented, codified from a real dogfood (recovered the KOL-campaign email-outreach flow into design-level sequences + class diagram + a stripped analysis-level domain model).
- `/abcd-model`, `/abcd-sync`, `/abcd-handoff`: WIP stubs.
- Grounded in 潘加宇《软件方法》ABCD workflow.
