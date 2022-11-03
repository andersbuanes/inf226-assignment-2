# Evaluation
The initial application was badly structure. A badly structured project can increase the possibility of bugs which in turn can have impacts on the security of the application.

## Application design, implementation and run instructions
To improve security we decided on restructuring the project. We wanted a clear separation of concerns to increase readability and maintainability of the code.

### Features of our application
- <code>app.py</code> - contains methods for initializing the application and database
- <code>config.py</code> - application configuration
- <code>data_handling.py</code> - contains all methods for accessing the database
- <code>database.py</code> - exposes the database for use in different parts of the application
- <code>manage.py</code> - runs the application
- <code>models.py</code> - contains the data transfer objects
- <code>web_models.py</code> - contains objects used for when data is being exposed to the client

### Technical details


### How to run
- Run <code>python manage.py</code> to ensure databases are set up and updated to most recent migration
- Start the application with <code>flask run</code>

Test the application by using one of the test users:
1. Alice
    - Username: <code>alice</code>
    - Password: <code>testtest</code>
2. Bob
    - Username: <code>bob</code>
    - Password: <code>password123</code>

or register a new user.



## Questions
### Threat Model

- Secret key is not random and stored directly in code
    - Easier to find session cookies which enables session hijacking
+ User data was stored directly in the source code. This increases the risk of an attacker obtaining sensitive information.
- Data was stored in the database using string concatenation. This makes SQLi very likely.
+ When searching for messages, data is added to the DOM using <code>innerHtml</code>. <code>innerHtml</code> is unsafe and if the data is not escaped it exposes the application to XSS attacks.
- Most routes are not protected meaning login is not required to access pages. This allows attackers to obtain information they should not have access to.
+ Using URL parameter to redirect
    - Enables option for CSRF attacks
- private messages are not private -> access control / authorization (?)
+ No authentication
- Input is not validated

### What can an attacker do?
- Access information they are not authorized to see
    - There was initially no authorization or access control in place
    - An attacker could access any information they would want
    - An attacker could send any information they would want

+ Obtain sensitive information
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
Firstly, in terms of confidationality there were two main issues:
- Reading of private messages
- Accessing user passwords

Secondly, in terms of integrity there were also two issues:
- Spoofing
- CSRF

Lastly, in terms of availability there were three issues:
    - Deleting or manipulating data, either through SQLi or XSS
    - DDOS attacks

## Attack Vectors
- Cryptographic Failures
- Injection
    - Cross Site Scripting
    - SQL Injection
- Security Misconfiguration
- Session Hijacking
- Broken Access Control
- Identification and Authentication Failures
- Security Logging and Monitoring Failures
- Insecure Design

## Control measures
TODO

## Access Control Model
TODO

## Traceability
TODO