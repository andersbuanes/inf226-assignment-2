# Evaluation

## Design
### Application Factory
Moving the creation of our application object lets us create multiple instances of the app later. There are multiple benefits to this, for example:

- Testing the application with different settings
- Run different versions of the application

### User model
UserMixin exposes methods such as *is_authenticated()*, *is_active()* and *get_id()*, making our life easier :)

### Protect pages
*Send*- and *Search*-route is not protected. We should require login to query for data. Solution: Add *@login_required* to these paths. Protecting pages ensures that only people with access are allowed to make requests.

### Prepared Statements
The application is vulnerable to SQL injection.

### 




- Session protection = "strong" secures 