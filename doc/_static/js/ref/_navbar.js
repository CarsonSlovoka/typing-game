/*
This script is a reference for you.
js.ref
*/

function show_nav_bar(){
    // nav section
    // $("section.wy-nav-content-wrap").replaceWith("margin-left: 0;")
    // $(".wy-nav-content").css({margin: ""})
    $("nav.wy-nav-side").css("display", "block")
    $("section.wy-nav-content-wrap").css("margin-left", "300px")
    $("div.wy-nav-content").css({margin:"initial"})
}

function hide_nav_bar(){
    $("nav.wy-nav-side").css("display", "none")
    $("section.wy-nav-content-wrap").css("margin-left", "0")
    $("div.wy-nav-content").css("margin-left", "300px")

    /*var isMobile = window.matchMedia("only screen and (min-width: 1100px)");
    if(window.matchMedia('only screen and (min-width: 1100px)').matches) {
     $("div.wy-nav-content").css("margin-left", "300px")
    }
    */
}

function setCookie(cname, cvalue, exdays) {
  // python3 -m http.server
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}


function getCookie(cname) {

  if (typeof document.cookie === "undefined") {
    return "";
  }

  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  // console.log(decodedCookie)

  var ca = decodedCookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

$(document).ready(function(){
  // $(".label_show_env_bar").hide()
  var hide_nav_bar_flag = getCookie("hide_nav_bar_flag")
  // console.log(hide_nav_bar_flag)
  hide_nav_bar_flag === "true"? hide_nav_bar() : show_nav_bar()

  $("button#ShowNav").click(function(){
    setCookie("hide_nav_bar_flag", "false", 1)
    show_nav_bar()
  });

  $("button#HideNav").click(function(){
    setCookie("hide_nav_bar_flag", "true", 1)
    hide_nav_bar()
  });
});
