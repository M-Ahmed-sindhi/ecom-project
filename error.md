# Migration Error Analysis

## Error Description
**Error**: `TypeError: Model instances without primary key value are unhashable`

## Context
This error occurs when running `python manage.py migrate`. It specifically happens during the `post_migrate` signal, where Django attempts to create permissions for installed apps.

## Root Cause Analysis
The issue is fundamentally a compatibility problem between **Django's ContentType framework** and the **Djongo** MongoDB connector.

1.  **Unhashable Instances**: The error message indicates that a Django model instance is being hashed (likely put into a set or dict key), but it lacks a Primary Key (PK).
2.  **Debug Findings**:
    - Our debug script (`debug_migration_loop.py`) revealed that for models like `LogEntry`, `Permission`, and `User`, `ContentType.objects.get_for_model(klass)` returns a `ContentType` instance where `id` is `None`.
    - `ContentType ID: None` cannot be hashed, leading to the crash.
3.  **Specific Triggers**:
    - `django.contrib.auth` tries to create permissions for all models after migration.
    - To do this, it requests `ContentType` objects for every model.
    - Djongo fails to return a saved instance (with an `_id` populated) for these specific models, causing the crash downstream in `django.db.models.base.Model.__hash__`.

## Traceback Sceenshot
```
  File "/.../django/contrib/auth/management/__init__.py", line 65, in create_permissions
    ctypes.add(ctype)
  File "/.../django/db/models/base.py", line 536, in __hash__
    raise TypeError("Model instances without primary key value are unhashable")
TypeError: Model instances without primary key value are unhashable
```

## Conclusion
The `django_content_type` collection in MongoDB seems to be in an inconsistent state or Djongo is failing to auto-generate ObjectIDs correctly for these system models. Dropping the collection was a good first step, but the issue persists because the *re-creation* process is returning incomplete objects.
