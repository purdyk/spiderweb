from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from .models import SearchGroup
from .models import Report
from .models import SearchResult
from .models import MatchedFile

from .apis import NabAPI
from .apis import FCSpider
from .apis import SabAPI

import re
import json
import logging


@login_required
def index(request):

    groups = SearchGroup.objects.order_by('name')

    context = {
        'groups': groups,
        'title': "Group List"
    }
    return render(request, 'spiderlist/index.html', context)


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(SearchGroup, pk=group_id)

    results = group.valid_results()

    context = {
        'group': group,
        'results': results,
        'title': group.name.title()
    }

    return render(request, 'spiderlist/group_detail.html', context)


@login_required
def result_detail(request, result_id):
    result = get_object_or_404(SearchResult, pk=result_id)

    reports = result.valid_reports().order_by('-size')

    context = {
        'result': result,
        'reports': reports,
        'title': "%s - %s" % (result.group.name.title(), result.date_key)
    }

    return render(request, 'spiderlist/result_detail.html', context)

@login_required
def result_ignore(request, result_id):
    result = get_object_or_404(SearchResult, pk=result_id)
    result.ignored = True
    result.save()

    return redirect('group_detail', group_id=result.group.id)

@login_required
def group_refresh(request, group_id):
    group = get_object_or_404(SearchGroup, pk=group_id)

    dateMatcher = re.compile("(\d\d)?(\d\d)[^\d]?(\d\d)[^\d]?(\d\d)")

    nabapi = NabAPI.NabAPI(dateMatcher)
    spider = FCSpider.FileSpider(dateMatcher)

    complete = False
    found = []
    new_files = []
    offset = 0

    query = group.search_string

    have = spider.build_file_list(query)

    for date in have:
        path = have[date][0]
        name = have[date][1]
        files = MatchedFile.objects.filter(path=path)
        if files.count() == 0:
            file = MatchedFile(
                group=group,
                path=path,
                date_key=date
            )
            file.save()
            new_files.append(file)

            results = SearchResult.objects.filter(date_key=date)
            if len(results) == 0:
                result = SearchResult(
                    group=group,
                    name=name,
                    date_key=date,
                    file=file
                )
            else:
                result = results[0]
                result.file = file

            result.save()

    query = [query]

    if len(group.additional_parameters) > 0:
        for each in group.additional_parameters.split(' '):
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
        results = SearchResult.objects.filter(date_key=each.date_key())

        if len(results) == 0:
            result = SearchResult(
                group=group,
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

    context = {
        'group': group,
        'reports': new_reports,
        'results': new_results,
        'files': new_files
    }

    return render(request, 'spiderlist/group_refresh.html', context)


@login_required
def report_fetch(request, report_id):
    report = get_object_or_404(Report, pk=report_id)

    sabapi = SabAPI.SabAPI()
    res = sabapi.enqueue(report.enq_url(), report.name)

    context = {
        'report': report,
        'res': res
    }

    return render(request, 'spiderlist/report_fetch.html', context)
