# Evaluation
The initial application was badly structure. A badly structured project can increase the possibility of bugs which in turn can have impacts on the security of the application.

## Design
To improve security we decided on restructuring the project.

## Security issues

- Secret key is not random and stored directly in code -> easier to find session cookies, session hijacking

- Users stored directly in source code

- String concatenation for SQL statements -> SQLi

- Some routes are not protected (send, search) -> access control / authorization (?)

- *next* parameter -> csrf

- private messages are not private -> access control / authorization (?)

- No authentication

- Input is not validated

- innerHtml is sketchy

- No application logger -> traceability

## Questions
## Threat Model
### Who might attack the application?

### What can an attacker do?
- Access information they are not authorized to see
    - There was initially no authorization or access control in place
    - An attacker could access any information they would want
    - An attacker could send any information they would want

+ Obtain user information
    - Passwords were stored in the source code
    - SQLi to access passwords

- Crash the application
    - No protection against DDOS
    - No protection against SQLi
    - No protection against XSS

+ Spoofing
    - The secret key was not secured, nor random. Easy for an attacker to hijack session.
    - There was no validation of passwords. As long as an attacker knew a username they could "log in".
    - Lack of protection against Cross-site Request Forgery.

### What damage could be done?
CIA-triad
- Confidentiality
    - asd

+ Integrity
    - asd

- Availability
    -   sd

## Attack Vectors

## Protection

## Access Control Model

## Traceability