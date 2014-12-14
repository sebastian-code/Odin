'use strict';

$(function(){
  $('select').on('change', function (event) {
      var url = $(this).val();
      if (url) {
          window.location = url;
      }
      return false;
  });
});
