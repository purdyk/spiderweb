from django.db import models
from django.conf import settings

from .apis import NabAPI
from .apis import FCSpider

import re
import json


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

    def refresh_files(self):
        date_matcher = re.compile("(\d\d)?(\d\d)[^\d]?(\d\d)[^\d]?(\d\d)")
        spider = FCSpider.FileSpider(date_matcher)
        new_files = []
        query = self.search_string

        have = spider.build_file_list(query)

        for date in have:
            path = have[date][0]
            name = have[date][1]
            files = MatchedFile.objects.filter(path=path)
            if files.count() == 0:
                file = MatchedFile(
                    group=self,
                    path=path,
                    date_key=date
                )
                file.save()
                new_files.append(file)

                results = SearchResult.objects.filter(date_key=date)
                if len(results) == 0:
                    result = SearchResult(
                        group=self,
                        name=name,
                        date_key=date,
                        file=file
                    )
                else:
                    result = results[0]
                    result.file = file

                result.save()

        return new_files

    def refresh_nab(self):
        date_matcher = re.compile("(\d\d)?(\d\d)[^\d]?(\d\d)[^\d]?(\d\d)")
        query = [self.search_string]
        nabapi = NabAPI.NabAPI(date_matcher)

        complete = False
        found = []
        offset = 0

        if len(self.additional_parameters) > 0:
            for each in self.additional_parameters.split(' '):
                query.append(each)

        while not complete:
            print("Doing Search ", offset)
            incoming = nabapi.do_search(query, offset)

            if len(incoming) == 0:
                complete = True

            for each in incoming:
                print("Processing raw result guid: ", each.guid())
                reports = Report.objects.filter(guid=each.guid())

                if len(reports) == 0:
                    found.append(each)
                else:
                    complete = True
                    break

            offset += 100

        new_reports = []
        new_results = []

        for each in found:
            results = self.searchresult_set.filter(date_key=each.date_key())

            if len(results) == 0:
                result = SearchResult(
                    group=self,
                    name=each.title(),
                    date_key=each.date_key(),
                )
                result.save()
                new_results.append(result)
            else:
                result = results[0]

            report = Report(
                result=result,
                name=each.title(),
                size=each.size(),
                guid=each.guid(),
            )
            report.raw = json.dumps(each.attrs)
            report.save()
            new_reports.append(report)

        return dict(reports=new_reports, results=new_results)

    def refresh(self):
        new_files = self.refresh_files()
        result = self.refresh_nab()
        result['group'] = self
        result['files'] = new_files
        return result


class MatchedFile(models.Model):
    path = models.CharField(max_length=4000, db_index=True)
    date_key = models.CharField(max_length=20, db_index=True)
    group = models.ForeignKey(SearchGroup, on_delete=models.CASCADE)
    missing = models.BooleanField(default=False)

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

    def clean_name(self):
        start = self.name.find(self.date_key)
        end = self.name.lower().find("xxx")

        if start > 0:
            start += len(self.date_key)

        if start > 0 and end > 0:
            stripped = self.name[start:end]
        elif start > 0:
            stripped = self.name[start]
        else:
            stripped = self.name

        stripped = stripped.replace(".", " ")
        if start > 0:
            return self.date_key + " " + stripped
        else:
            return stripped


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
