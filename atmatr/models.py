from django.db import models

# CUSTOM MANAGERS


class ucManager(models.Manager):

    """
    Adds an update_or_create method.
    This can go away once we upgrade to Django 1.7

    """

    def update_or_create(self, **kwargs):
        assert kwargs, \
            'update_or_create() must be passed at least one keyword argument'
        obj, created = self.get_or_create(**kwargs)
        defaults = kwargs.pop('defaults', {})
        if created:
            return obj, True, False
        else:
            try:
                params = dict([(k, v) for k, v in kwargs.items() if '__' not in k])
                params.update(defaults)
                for attr, val in params.items():
                    if hasattr(obj, attr):
                        setattr(obj, attr, val)
                sid = transaction.savepoint()
                obj.save(force_update=True)
                transaction.savepoint_commit(sid)
                return obj, False, True
            except IntegrityError, e:
                transaction.savepoint_rollback(sid)
                try:
                    return self.get(**kwargs), False, False
                except self.model.DoesNotExist:
                    raise e


# ABSTRACT MODELS

class ucModel(models.Model):

    """
    Abstract model with an update_or_create manager.
    This can go away once we upgrade to Django 1.7

    """
    class Meta:
        abstract = True

    objects = ucManager()


class TimestampModel(models.Model):

    """
    Abstract model with timestamp fields

    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NamedModel(models.Model):

    """
    Abstract model with a name.
    CAUTION: NAMES ARE REQUIRED for NamedModel models.

    """
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        abstract = True


class DateRangeModel(models.Model):

    """
    Abstract model with date range fields.

    """
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class ExtendedModel(ucModel, TimestampModel, NamedModel):

    """
    Abstract model to combine common extended functionality.
    Provided for utility only.
    """

    class Meta:
        abstract = True
