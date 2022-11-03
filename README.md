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

### Protect pages
*Send*- and *Search*-route is not protected. We should require login to access or modify data. Solution: Add *@login_required* to these paths. Protecting pages ensures that only people with access are allowed to make requests.

### Prepared Statements
The application is vulnerable to SQL injection. Using prepared statements ...


- Session protection = "strong" secures ...