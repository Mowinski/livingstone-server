from django.db import models
from django.db.models import Q


class Level(models.Model):
    GIRAFFE_BOX = 1
    ELEPHANT_BOX = 2
    LION_BOX = 3
    LIZARD_BOX = 4
    CAMEL_BOX = 5
    BOXES_CHOICES = (
        (GIRAFFE_BOX, 'Giraffe'),
        (ELEPHANT_BOX, 'Elephan'),
        (LION_BOX, 'Lion'),
        (LIZARD_BOX, 'Lizard'),
        (CAMEL_BOX, 'Camel'),
    )

    box_1 = models.IntegerField(choices=BOXES_CHOICES, verbose_name="First box")
    box_2 = models.IntegerField(choices=BOXES_CHOICES, verbose_name="Second box")
    box_3 = models.IntegerField(choices=BOXES_CHOICES, verbose_name="Third box")
    box_4 = models.IntegerField(choices=BOXES_CHOICES, verbose_name="Fourth box")
    box_5 = models.IntegerField(choices=BOXES_CHOICES, verbose_name="Fifth box")

    two_star_time = models.FloatField(verbose_name="Time to reach result with two star (2*)")
    three_star_time = models.FloatField(verbose_name="Time to reach result with three star (3*)")
    perfect_move_count = models.IntegerField(verbose_name="Maximum number of move to reach special star")
    order = models.IntegerField(verbose_name="Number of level in set")

    set = models.ForeignKey("Set", verbose_name="Pointer to set where level is located", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order} - {self.set.title}"

    class Meta:
        ordering = ['-set', 'order']


class Set(models.Model):
    title = models.CharField(max_length=250, verbose_name="Set title")
    history = models.ForeignKey("History", verbose_name="Which history unlock this set", on_delete=models.CASCADE)
    version = models.ForeignKey("Version", verbose_name="In which version this set is included", on_delete=models.CASCADE)

    def __str__(self):
        level_count = self.level_set.all().count()
        return f"{self.title}; levels count: {level_count}"


class History(models.Model):
    title = models.CharField(max_length=250, verbose_name="History title")
    image = models.ImageField(verbose_name="Image in background in history activity")
    description = models.TextField(verbose_name="Description of history")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Histories"


class Version(models.Model):
    version = models.CharField(max_length=20, verbose_name="Number/Name of version")
    next_version = models.ForeignKey("Version", verbose_name="Next version, leave empty if it is the latest one",
                                     related_name="next_available_version",
                                     null=True, blank=True, default=None, on_delete=models.SET_NULL)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        should_update_version = not bool(self.pk)
        super().save(force_insert, force_update, using, update_fields)

        if not should_update_version:
            return
        try:
            none_version = Version.objects.get(~Q(pk=self.pk), next_version__isnull=True)
            none_version.next_version = self
            none_version.save()
        except Version.DoesNotExist:
            pass

    def __str__(self):
        return f"Ver: {self.version}"

    def __repr__(self):
        return "<Version: {}>".format(self.version)

    class Meta:
        ordering = ['-id']
