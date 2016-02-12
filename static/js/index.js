var res_load = function() {
  debugger;
  var resId = this.attributes['data'].value;
  var target = $('#result-' + resId);
  if (target.children().length == 0) {
    target.collapse('show');
    target.load('results/' + resId);
  } else {
    target.toggle();
  }
  return false;
};

var group_load = function () {
  var id = this.attributes['data'].value;
  var target = $('#group-' + id);
  if (target.children().length == 0) {
    target.collapse('show');
    target.load("groups/" + id, function() {
      $('#group-' + id + ' .result-link').click(res_load);
    });
  } else {
    target.toggle();
  }
  return false;
}

$('.group-link').click(group_load);