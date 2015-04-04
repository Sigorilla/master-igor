$(document).ready(function () {

  var FIT = (function () {

    var $settings,
        $fitTable,
        $addDay,
        csrftoken;

    var _init = function (argument) {
      console.log('Init FIT.');

      $fitTable = $('#fitTable');
      $settings = $('#settings');
      $addDay = $('#addDay');

      csrftoken = getCookie('csrftoken');

      FIT.addListners();
    };

    var _addListners = function (argument) {
      $fitTable.find('td').on('click', _showSettings);
      $settings.on('hidden.bs.modal', _clearSettings);
      $settings.find('#saveSettings').on('click', _saveSettings);
      $('#btnAddDay').on('click', _showAddDay);
    };

    var getCookie = function (name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    };

    var csrfSafeMethod = function (method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    var JSON_stringify = function(s, emit_unicode) {
       var json = JSON.stringify(s);
       return emit_unicode ? json : json.replace(/[\u007f-\uffff]/g,
          function(c) { 
            return '\\u'+('0000'+c.charCodeAt(0).toString(16)).slice(-4);
          }
       );
    };

    var _showSettings = function(event) {
      console.log("Show form for settings.");
      // console.log($(this));
      if (!$settings.hasClass('no_auth')) {
        var $td = $(this),
            $tr = $td.parent('tr');
        var h4 = $tr.find('th').text(),
            h4_small = $fitTable.find('thead th').eq($td.index()).text(),
            count = parseInt($td.data('count'));
        var exerciseID = $tr.find('th').data('exercise-id'),
            dayID = $fitTable.find('thead th').eq($td.index()).data('day-id');

        $settings.find('.modal-title')
          .html(h4 + ' <small>' + h4_small + '</small>');

        $td.find('.approach').each(function (index, element) {
          $settings.find('.modal-body > .row').eq(index)
            .find('.input-weight').val($(element).find('.weight').text());
          $settings.find('.modal-body > .row').eq(index)
            .find('.input-times').val($(element).find('.times').text());
        });

        for (var i = $td.find('.approach').length; 
          i <= $settings.find('.modal-body > .row').length; 
          i++) {
          $settings.find('.modal-body > .row').eq(i)
            .find('.input-weight').val('');
          $settings.find('.modal-body > .row').eq(i)
            .find('.input-times').val('');
        }

        $settings.find('input[name=training]').val($td.data('training-id'));
        $settings.find('input[name=exercise]').val(exerciseID);
        $settings.find('input[name=day]').val(dayID);
      }

      $settings.modal();
    };

    var _clearSettings = function(event) {
      console.log("Clear form for settings.");
      $settings.find('.modal-title').html('');
      $settings.find('.modal-body > .row .input-weight').val('');
      $settings.find('.modal-body > .row .input-times').val('');
    };

    var _saveSettings = function (event) {
      console.log("Save settings.");

      var currSettings = {
        count: 0,
        items: []
      };

      $settings.find('.modal-body > .row').each( function (index, element) {
        var currApproach = {
          weight: 0,
          times: 0
        };
        currApproach.weight = $(element).find('.input-weight').val();
        currApproach.times = $(element).find('.input-times').val();
        currSettings.items.push(currApproach);
        currSettings.count++;
      });

      var dataOut = {
        trainingID: $settings.find('input[name=training]').val(),
        exerciseID: parseInt($settings.find('input[name=exercise]').val()),
        dayID: parseInt($settings.find('input[name=day]').val()),
        results: JSON_stringify(currSettings, false), //encodeURIComponent(JSON.stringify(currSettings)),
      };
      console.log('Settings: ' + dataOut);

      $.ajax({
        type: 'POST',
        url: '/fitness/save_results/',
        data: dataOut,
        success: function (data) {
          console.log(data);
        }
      });

    };

    var _showAddDay = function (event) {
        $addDay.modal();
    };

    return {
      init: _init,
      addListners: _addListners,
    }
  }());

  FIT.init();

});
