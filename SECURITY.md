# Security policy

EnoTech repositories are private by default. Do not disclose suspected
vulnerabilities, secrets, customer details, coordinates, mesh identifiers, or
deployment data in public issues, public pull requests, or public discussions.

## Reporting

Use the existing private founder/operator channel for security reports. There
is no public disclosure mailbox, bounty program, or public SLA yet.

If you are a Cloud Agent and you encounter a possible secret or live operational
detail:

1. Stop expanding the exposure.
2. Remove the value from any pending diff.
3. Record the file/path and a redacted description in the private handoff.
4. Ask the founder/operator to rotate the affected credential or confirm the
   data is synthetic before continuing.

## Scope

This policy applies to this repository and all of its branches. Report a suspected
leak of credentials or customer data through a private security advisory on this
repository; if that channel is unavailable, contact a maintainer listed in
[`GOVERNANCE.md`](./GOVERNANCE.md). Do not open a public issue for a suspected leak.

