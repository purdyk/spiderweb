from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import SearchGroup
from .models import Report
from .models import SearchResult

from .apis import SabAPI

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

    results = group.valid_results().order_by('-date_key')

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

    context = group.refresh()

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
