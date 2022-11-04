# Evaluation
The initial application was badly structure. A badly structured project can increase the possibility of bugs which in turn can have impacts on the security of the application.

## Application design, implementation and run instructions
To improve security we decided on restructuring the project. We wanted a clear separation of concerns to increase readability and maintainability of the code.

### Features of our application
- <code>app.py</code> - contains methods for initializing the application and database
- <code>config.py</code> - application configuration
- <code>data_handling.py</code> - contains all methods for accessing the database
- <code>database.py</code> - exposes the database for use in different parts of the application
- <code>manage.py</code> - initializes the application
- <code>models.py</code> - contains the data transfer objects
- <code>web_models.py</code> - contains objects used for when data is being exposed to the client

### Technical details


### How to run
- Run <code>python manage.py</code> to ensure databases are set up and updated to most recent migration
- Start the application with https <code>flask run --cert=adhoc</code>
- Start the application with http(testing) <code>flask run</code>
- The application is now available at <code>localhost:5000</code>

Test the application by using one of the test users:
1. Alice
    - Username: <code>alice</code>
    - Password: <code>testtest</code>
2. Bob
    - Username: <code>bob</code>
    - Password: <code>12345678</code>

or register a new user.

To run multiple instances of the application clear the browser cache or open a new browser. Start the application with <code>flask run --port 5001</code>. Any port can be used except from port 5000.


## Questions
### Threat Model

- Secret key is not random and stored directly in code. This makes it easier for an attacker to find session cookies and hijack a session.
- User data was stored directly in the source code. This increases the risk of an attacker obtaining sensitive information.
- Data was stored in the database using string concatenation which exposes the application to SQLi.
- Messages is unencrypted in the database, meaning anyone with access could read all messages.
- When messages are shown to the user, data is added to the DOM using <code>innerHtml</code>. <code>innerHtml</code> is unsafe and if the data is not escaped it exposes the application to XSS attacks.
- Most routes are not protected meaning login is not required to access these pages. This allows attackers to obtain information they should not have access to.
- Using URL parameter to redirect and post data
    - Enables option for CSRF attacks
    - Vunreble to XSS, tricking logged in users to click on urls with malicious payloads
- Private messages are not private, making the confidentiality of the application low
- No authentication is in place. Password is not checked on login. A user can send a message as anyone.
- Input is not validated.
- Data is sent over http, sending messages over the network unencrypted, making network sniffing possible to read private messages.

### What can an attacker do?
- Access information they are not authorized to see
    - There was initially no authorization or access control in place
    - An attacker could access any information they would want
    - An attacker could send any information they would want as anyone

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
    - Lack of protection against CSRF.

### What damage could be done?
Firstly, in terms of confidentiality there were two main issues:
- Reading of private messages
- Accessing user passwords

Secondly, in terms of integrity there were also two issues:
- Possibility of session hijacking as secret was not secured
- CSRF

Lastly, in terms of availability there were three issues:
- Deleting or manipulating data, either through SQLi or XSS
- DDOS attacks

## Attack Vectors
The application had many attack vectors. Though some could be debated we formed this list for the application:

- Session Hijacking
- Security Misconfiguration
- Cryptographic Failures
- Injection
    - Cross Site Scripting
    - SQL Injection
- Broken Access Control
- Identification and Authentication Failures
- Security Logging and Monitoring Failures
- Insecure Design

## Control measures
- To prevent session hijacking the secret key is now stored in an environment variable that is accessed through the configuration file. For testing purposes there has been made one configuration file for development and another for production. An alternative could also be to store it directly in the configuration file and keep this file stored securely or inject the secrets into the config file on deployment.
- Sensitive information has been protected by hashing and salting passwords aswell as storing them in the database. Ideally this information would be stored in a separate database.
- SQL injection attacks have been mitigated by using SQLAlchemys functionality. All user input is escaped before queries are made.
- XSS attacks have been mitigated by replacing <code>innerHtml</code> with <code>setHTML</code> (or <code>setText</code> if browser doesn't support <code>setHTML</code>). <code>setHTML</code> sanitizes the data before adding it to the DOM.
- To handle access control most methods have been made unavailable unless a user is logged in. Additionally, a user can no longer set who has sent a message. Also, a user can no longer access messages where they are not the sender nor on the recipient list.
- Authentication is now done by checking the provided password against the hashed password in the database. If the hash of the provided password doesn't match the user is denied access.
- CSRF attacks have been mitigated by applying a CSRF token to all forms. Further, all forms are now validated by applying custom validators for each field. This includes minimum lengths for passwords, required inputs, checks for unwanted characters and more. If a form is invalid, the user will be redirected to page and no data is sent to the server.
- Flask default <code>next</code>-parameter on redirect has been made obsolete. This is to prevent the user trying to redirect to unwanted URLs. Further the cookie settings has been set to require same-site origin for requests.
- In addition to same-site, cookies have been set to be secure meaning they can only be transferred by HTTPS. To avoid being read by JavaScript they have also been given HttpOnly attribute.
- To help with traceability in the case of an attack we have added logging to the application. Most logged events are either debug or info. We have tried to mark logged events with warning in places where we think the application could be exploited.

## Access Control Model
The access control implemented in the application is Relationship Based Access Control. User have access to protected resources based on what other users set. If a users A sets user B as recipient of a message, user B will get access to that resource while an arbitrary user does not have access.

## Discussion
There are still some things that have not been adressed.
- Messages in the database are not encrypted potentially making sensitive information available to an attacker. This was not implemented due to time restrictions. An implementation of this would be similar to the implementation of password hashing.