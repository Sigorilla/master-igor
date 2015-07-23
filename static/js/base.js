$(document).ready(function () {

  // Highlight link to current page
  $("a[href='" + location.pathname + "']:not(.noselect)")
    .addClass("selected").removeAttr("href");

  // Replace h5, h6 to h4 and h1 to h2 from article
  $("article.post h5, article.post h6").each(function (index, element) {
    $(element).replaceWith("<h4>" + $(element).text() + "</h4>");
  });
  $("article.post h1").each(function (index, element) {
    $(element).replaceWith("<h2>" + $(element).text() + "</h2>");
  });

  // Create titling
  // TODO:: add a check for the existence of ID
  var headings = {
    "H2": 0,
    "H3": 0,
    "H4": 0
  };
  var $prev, $h2, $h3, $h4;
  var $root1, $root2, $root3;
  $(".detail h2, .detail h3, .detail h4").each(function (index, element) {
    var name = $(element).prop("tagName"),
        curr = $(element).text(),
        link = curr.toLowerCase().replace(/([ \W])/g, '-').replace(/-+$/gm, ''),
        text = "";
    $(element).attr("id", link);
    link = "#" + link;
    if (name == "H2") {
      headings[name] += 1;
      text += headings[name] + ". " + curr;
      if (headings[name] == 1) {
        $root1 = $("<ol class='titling'></ol>").insertAfter($("article.post.detail .intro"));
      }
      if ($root1) {
        $h2 = $("<li><a href='" + link + "'>" + curr + "</a></li>").appendTo($root1);
      }
      headings["H3"] = 0;
    }
    if (name == "H3") {
      headings[name] += 1;
      text += headings["H2"] + "." + headings[name] + ". " + curr;
      if (headings[name] == 1) {
        $root2 = $("<ol></ol>").insertAfter($h2);
      }
      if ($root2) {
        $h3 = $("<li><a href='" + link + "'>" + curr + "</a></li>").appendTo($root2);
      }
      headings["H4"] = 0;
    }
    if (name == "H4") {
      headings[name] += 1;
      text += headings["H2"] + "." + headings["H3"] + "." + headings[name] + ". " + curr;
      if (headings[name] == 1) {
        $root3 = $("<ol></ol>").insertAfter($h3);
      }
      if ($root3) {
        $h4 = $("<li><a href='" + link + "'>" + curr + "</a></li>").appendTo($root3);
      }
    }

    $(element).text(text);
    // console.log(headings);
    $prev = $(element);
  });

  // Replace double normal dashes to one long dash
  $("main :contains('--'), #main :contains('--')").each(function () {
    $(this).html($(this).html().replace(new RegExp('--','g'), "&mdash;"));
  });

  // Fire some events
  $('[data-fire]').click(function () {
    var fire = $(this).data('fire');
    if (fire == 'totop') {
      $('html, body').animate({scrollTop: 0});
    }
    if (fire == 'print') {
      window.print();
    }
    if (fire == 'search') {
      open_search();
    }
  });

  $('#searchModal').on('shown.bs.modal', function () {
    $(this).find('input#search').focus();
  });

  $('#search').on('keyup', function () {
    var q = $(this).val();
    if (q != '') {
      $(this).parents('.modal-content').find('.modal-body').remove();
      $(this).parents('.modal-content').append('<div class="modal-body"><div id="searchResults"></div></div>');
      $('#searchResults').html('&nbsp;').load( $(this).parents('form').attr('action') + '?q=' + q );
    }
  });

  // $("body").css("margin-bottom", $("footer").outerHeight());
});

$(window).resize(function () {
  // $("body").css("margin-bottom", $("footer").outerHeight());
});