from __future__ import absolute_import

from celery import shared_task

@shared_task
def refresh_group(gid):
    group = SearchGroup.get(gid)
    group.refresh()
