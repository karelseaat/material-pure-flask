(function() {
  'use strict';
  var snackbarContainer = document.querySelector('#demo-toast-example');
  window.addEventListener('load', function() {
    'use strict';
    var data = {message: snackbarContainer.childNodes[1].innerHTML, timeout: 3000,};
    snackbarContainer.MaterialSnackbar.showSnackbar(data);
  });
}());
