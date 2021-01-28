$(document).ready(function () {
  var socket = io.connect("http://" + document.domain + ":" + location.port);

  console.log("Page has been refreshed");

  function getStatus() {
    var topic = [];
    var data = [];

    topic.push("cmnd/light/POWER");
    topic.push("cmnd/heater/POWER");

    for (var i = 0; i < topic.length; i++) {
      data.push(
        '{"topic": "' +
        topic[i] +
        '", "message": "' +
        "" +
        '", "qos": ' +
        "0" +
        "}"
      );
      //   console.log(data[i]);
      socket.emit("publish", (datas = data[i]));
    }
  }

  getStatus();

  $(".dropdown-toggle").dropdown();

  $("#deskLamp").click(function (event) {
    console.log("click");
    var topic = "cmnd/light/POWER";
    var message = "";
    var qos = 0;
    var state = $("#deskLampState").text();

    if (state == "Actif") {
      message = "off";
    } else {
      message = "on";
    }

    var data =
      '{"topic": "' +
      topic +
      '", "message": "' +
      message +
      '", "qos": ' +
      qos +
      "}";
    socket.emit("publish", (data = data));
  });

  socket.on("mqtt_message", function (data) {
    console.log(data);
    if (data["topic"] == "stat/light/RESULT") {
      console.log("*** LAMP ***");
      var img = document.getElementById("deskLampImg");
      var imgAttribute = img.getAttribute("src");

      if (data["payload"] == "ON") {
        $("#deskLampState").text("Actif");
        imgAttribute = "../static/img/led-light_on.png";

        $("#deskLamp").removeClass("accessorie");
        $("#deskLamp").addClass("accessorieActive");
        $("#deskLampState").removeClass("accessorieStatusOff");
        $("#deskLampState").addClass("accessorieStatusOn");
        $("#deskLampName").removeClass("accessorieNameOff");
        $("#deskLampName").addClass("accessorieNameOn");
      } else {
        $("#deskLampState").text("Éteint");
        imgAttribute = "../static/img/led-light_off.png";

        $("#deskLamp").removeClass("accessorieActive");
        $("#deskLamp").addClass("accessorie");
        $("#deskLampState").removeClass("accessorieStatusOn");
        $("#deskLampState").addClass("accessorieStatusOff");
        $("#deskLampName").removeClass("accessorieNameOn");
        $("#deskLampName").addClass("accessorieNameOff");
      }
      img.setAttribute("src", imgAttribute);
    }
  });
});
