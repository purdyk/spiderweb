var res_load = function() {
  var resId = this.attributes['data-target'].value;
  var target = $('#result-' + resId);
  if (target.children().length == 0) {
    target.collapse('show');
    target.load('results/' + resId, function() {
      $('#result-' +resId + ' .report-fetch-link').click(report_fetch);
    });
  } else {
    target.toggle();
  }
  return false;
};

var res_ignore = function() {
  var resId = this.attributes['data-target'].value;
  var groupId = this.attributes['data-toggle'].value;
  var target = $('#group-' + groupId);
  var targetL = $('#group-refresh-' + groupId);

  jQuery.ajax('results/' + resId + '/ignore').done(function(data) {
    target.children().remove();
    targetL.click();
  });

  return false;
}

var group_load = function () {
  var id = this.attributes['data-target'].value;
  var target = $('#group-' + id);
  if (target.children().length == 0) {
    target.collapse('show');
    target.load("groups/" + id, function() {
      $('#group-' + id + ' .result-link').click(res_load);
      $('#group-' + id + ' .result-ignore').click(res_ignore);
    });
  } else {
    target.toggle();
  }
  return false;
}

var group_refresh = function () {
  var id = this.attributes['data-target'].value;
  var title = $('#dialog-title');
  var content = $('#dialog-content');
  var name = this.attributes['name'].value;

  title.text("Refreshing: " + name);
  content.text("")
  show_dialog();
  disable_close();
  content.load("groups/" + id + "/refresh", function() {
    enable_close();
    title.text("Refresh Complete: " + name);
  });

  return false;
}

var report_fetch = function () {
  var id = this.attributes['data-target'].value;
  var title = $('#dialog-title');
  var content = $('#dialog-content');
  var name = this.attributes['name'].value;

  title.text("Enqueuing: " + name);
  content.text("")
  disable_close();
  show_dialog();
  content.load("reports/" + id + "/fetch", function() {
    enable_close();
    title.text("Enqueued: " + name);
  });

  return false;
}

var show_dialog = function() {
  $('#dialog').modal()
}

var disable_close = function() {
  $('#dialog-dismiss').prop('disabled', true)
}

var enable_close = function() {
  $('#dialog-dismiss').prop('disabled', false)
}

$('.group-link').click(group_load);
$('.group-refresh-link').click(group_refresh);
