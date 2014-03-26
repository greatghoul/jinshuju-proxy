(function($) {
  log('Listening push request for', form);

  function pullEntry(form, callback) {
    log('Pulling the latest entry ...')
    $.get(url('/entry'), form, callback, 'json');
  }

  function cleanEntry(entry) {
    $.ajax({
      url: url('/entry'),
      type: 'DELETE',
      data: {
        entry_key: entry.key
      },
      success: function() {
        setTimeout(processProxy, 5000);
      }
    });
  }

  function pushEntry(entry) {
    if (entry) {
      log('  Pushing entry:', entry);
      $.ajax({
        type: 'POST',
        url: localStorage['PUSH_URL'],
        processData: false,
        data: entry.data,
        success: function(data) {
          log('  Response:', data);
          cleanEntry(entry);
        }
      });
    } else {
      log('  No entry found at this time.');
      setTimeout(processProxy, 5000);
    }
  }

  function processProxy() {
    pullEntry(form, pushEntry);
  }

  $(function() {
    processProxy();
  }); 
})(jQuery);
