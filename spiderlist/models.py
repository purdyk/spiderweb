from django.db import models
from django.conf import settings

# Create your models here.


class SearchGroup(models.Model):
    name = models.CharField(max_length=200)
    search_string = models.CharField(max_length=200)
    additional_parameters = models.CharField(max_length=200, blank=True)

    def valid_results(self):
        return self.searchresult_set.filter(ignored=False, invalid=False, file__isnull=True)

    def update_invalidity(self):
        for result in self.searchresult_set.filter(ignored=False).all():
            if result.valid_reports().count() == 0:
                result.invalid = True
            else:
                result.invalid = False

            result.save()

    def __str__(self):
        return self.name


class MatchedFile(models.Model):
    path = models.CharField(max_length=4000, db_index=True)
    date_key = models.CharField(max_length=20, db_index=True)
    group = models.ForeignKey(SearchGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.path


class SearchResult(models.Model):
    group = models.ForeignKey(SearchGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    date_key = models.CharField(max_length=20, db_index=True)
    ignored = models.BooleanField(default=False)
    invalid = models.BooleanField(default=False)
    file = models.ForeignKey(
        MatchedFile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    def valid_reports(self):
        return self.report_set.filter(size__gte=settings.MINSIZE)


class Report(models.Model):
    result = models.ForeignKey(SearchResult, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    size = models.IntegerField(default=0)
    guid = models.CharField(max_length=100, db_index=True)
    raw = models.TextField

    def __str__(self):
        return self.name

    def enq_url(self):
        return "%s/api?t=get&id=%s&apikey=%s" % (settings.NEWZNAB_URL, self.guid, settings.NEWZNAB_KEY)

