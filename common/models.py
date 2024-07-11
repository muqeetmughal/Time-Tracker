
from django.db import models
from django.utils import timezone

class SoftDeleteQuerySet(models.QuerySet):
    def archive(self):
        return super().update(archived_at=timezone.now())

    def delete(self):
        return super().delete()

    def restore(self):
        return self.update(archived_at=None)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(
            archived_at__isnull=True
        )


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def archive(self, using=None, keep_parents=False):
        self.archived_at = timezone.now()
        self.save()

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)

    def restore(self):
        self.archived_at = None
        self.save()

    @property
    def is_archived(self):
        return self.archived_at is not None


