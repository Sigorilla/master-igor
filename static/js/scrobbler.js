var nick = "Sigorilla", prev_nick, date,
  default_img = "http://screenshots.en.sftcdn.net/blog/en/2012/10/10-15-2012-2-22-52-PM-300x300.png";

$(document).ready(function () {

  var get_now = function () {
    // TODO:: add error of network or something else...
    var url = "https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&limit=1&user=" + nick + "&api_key=cb7c92d1840e42c12214eb470e5281e0&format=json";
    $.getJSON(url)
    .success(function (data) {
      // console.log(data);
      var track, user;
      try {
        track = data.recenttracks.track;
        user = data.recenttracks["@attr"]["user"];
      } catch (e) {
        var er;
        try {
          er = (data.error) ? data.message : "Rly?!";
          if (data.error)
            nick = prev_nick;
        } catch (err) {
          er = "Something happends wrong.";
        }
        console.warn(er);
      }
      if (track) {
        track = track[0] || track;
        // TODO:: not update if same track

        // console.log(track);
        // var curr_date = track["@attr"]["nowplaying"] || track.date["uts"];
        // if (date !== curr_date || curr_date !== "true") {
          // console.info("New scrobble.");
          $("#nick").text(user);
          $("#name").text(track.name);
          $("#name").attr("href", track.url);
          $("#artist").text(track.artist["#text"]);
          $("#img").attr("src", track.image[3]["#text"] || default_img);
          // date = curr_date;
        // }
      }
    });
  };

  setTimeout(get_now, 1000);

  setInterval(get_now, 10000);

  $("#change_name").on("submit", function (event) {
    event.preventDefault();
    yaCounter25920671.reachGoal('SCROB');
    prev_nick = nick;
    nick = $(this).find("input#new_nick").val();
    if (nick) {
      get_now();
    } else {
      nick = prev_nick;
    }
  });

});
