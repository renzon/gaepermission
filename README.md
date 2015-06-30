gaepermission
=============

Tekton app to handle user login and permissions based on groups and roles

It can be installed from pypi:

```
pip install gaepermission
```

It supports logins with Google, Facebook and Passwordless

### Decotators

```python
@login_not_required
```
You can declare that login is not required on your routes. That way, you won't get a 403 Forbidden response.

```python
@login_required
```
To use on sensitive requests. This is default convention on Tekton.
