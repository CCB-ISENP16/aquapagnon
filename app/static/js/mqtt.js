$(document).ready(function () {
  var socket = io.connect("http://" + document.domain + ":" + location.port);

  console.log("Page has been refreshed");

  function getStatus() {
    var topic = [];
    var data = [];

    topic.push("cmnd/SmartSurgeDesk/POWER1");
    topic.push("cmnd/SmartSurgeDesk/POWER2");
    topic.push("cmnd/SmartSurgeDesk/POWER3");
    topic.push("cmnd/SmartSurgeDesk/POWER4");

    topic.push("cmnd/columnLED/power");
    topic.push("cmnd/treeLED/power");

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
    var topic = "cmnd/SmartSurgeDesk/POWER1";
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

  $("#usbPorts").click(function (event) {
    var topic = "cmnd/SmartSurgeDesk/power";
    var message = "";
    var qos = 0;
    var state = $("#usbPortsState").text();

    if (state == "Allumé") {
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

  $("#screenMonitor").click(function (event) {
    var topic = "cmnd/SmartSurgeDesk/power";
    var message = "";
    var qos = 0;
    var state = $("#screenMonitorState").text();

    if (state == "Allumé") {
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

  $("#solderingIron").click(function (event) {
    var topic = "cmnd/SmartSurgeDesk/power";
    var message = "";
    var qos = 0;
    var state = $("#solderingIronState").text();

    if (state == "Allumé") {
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

  // Salon

  $("#treeLED").click(function (event) {
    var topic = "cmnd/treeLED/power";
    var message = "";
    var qos = 0;
    var state = $("#treeLEDState").text();

    if (state == "Allumé") {
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

  $("#columnLED").click(function (event) {
    var topic = "cmnd/columnLED/power";
    var message = "";
    var qos = 0;
    var state = $("#columnLEDState").text();

    if (state == "Allumé") {
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
    if (data["topic"] == "stat/SmartSurgeDesk/POWER1") {
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

    if (data["topic"] == "stat/SmartSurgeDesk/POWER") {
      var img = document.getElementById("usbPortsImg");
      var imgAttribute = img.getAttribute("src");
      if (data["payload"] == "ON") {
        $("#usbPortsState").text("Allumé");
        imgAttribute = "../static/png/powerOutlet.png";

        $("#usbPorts").removeClass("accessorie");
        $("#usbPorts").addClass("accessorieActive");
        $("#usbPortsState").removeClass("accessorieStatusOff");
        $("#usbPortsState").addClass("accessorieStatusOn");
        $("#usbPortsName").removeClass("accessorieNameOff");
        $("#usbPortsName").addClass("accessorieNameOn");
      } else {
        $("#usbPortsState").text("Éteint");
        imgAttribute = "../static/png/powerOutletOff.png";

        $("#usbPorts").removeClass("accessorieActive");
        $("#usbPorts").addClass("accessorie");
        $("#usbPortsState").removeClass("accessorieStatusOn");
        $("#usbPortsState").addClass("accessorieStatusOff");
        $("#usbPortsName").removeClass("accessorieNameOn");
        $("#usbPortsName").addClass("accessorieNameOff");
      }
      img.setAttribute("src", imgAttribute);
    }

    if (data["topic"] == "stat/SmartSurgeDesk/POWER") {
      var img = document.getElementById("screenMonitorImg");
      var imgAttribute = img.getAttribute("src");
      if (data["payload"] == "ON") {
        $("#screenMonitorState").text("Allumé");
        imgAttribute = "../static/png/TV.png";

        $("#screenMonitor").removeClass("accessorie");
        $("#screenMonitor").addClass("accessorieActive");
        $("#screenMonitorState").removeClass("accessorieStatusOff");
        $("#screenMonitorState").addClass("accessorieStatusOn");
        $("#screenMonitorName").removeClass("accessorieNameOff");
        $("#screenMonitorName").addClass("accessorieNameOn");
      } else {
        $("#screenMonitorState").text("Éteint");
        imgAttribute = "../static/png/TVOff.png";

        $("#screenMonitor").removeClass("accessorieActive");
        $("#screenMonitor").addClass("accessorie");
        $("#screenMonitorState").removeClass("accessorieStatusOn");
        $("#screenMonitorState").addClass("accessorieStatusOff");
        $("#screenMonitorName").removeClass("accessorieNameOn");
        $("#screenMonitorName").addClass("accessorieNameOff");
      }
      img.setAttribute("src", imgAttribute);
    }

    if (data["topic"] == "stat/SmartSurgeDesk/POWER") {
      var img = document.getElementById("solderingIronImg");
      var imgAttribute = img.getAttribute("src");
      if (data["payload"] == "ON") {
        $("#solderingIronState").text("Allumé");
        imgAttribute = "../static/png/powerOutlet.png";

        $("#solderingIron").removeClass("accessorie");
        $("#solderingIron").addClass("accessorieActive");
        $("#solderingIronState").removeClass("accessorieStatusOff");
        $("#solderingIronState").addClass("accessorieStatusOn");
        $("#solderingIronName").removeClass("accessorieNameOff");
        $("#solderingIronName").addClass("accessorieNameOn");
      } else {
        $("#solderingIronState").text("Éteint");
        imgAttribute = "../static/png/powerOutletOff.png";

        $("#solderingIron").removeClass("accessorieActive");
        $("#solderingIron").addClass("accessorie");
        $("#solderingIronState").removeClass("accessorieStatusOn");
        $("#solderingIronState").addClass("accessorieStatusOff");
        $("#solderingIronName").removeClass("accessorieNameOn");
        $("#solderingIronName").addClass("accessorieNameOff");
      }
      img.setAttribute("src", imgAttribute);
    }

    // Salon

    if (data["topic"] == "stat/treeLED/POWER") {
      var img = document.getElementById("treeLEDImg");
      var imgAttribute = img.getAttribute("src");

      if (data["payload"] == "ON") {
        $("#treeLEDState").text("Allumé");
        imgAttribute = "../static/png/lamp3Glow.png";

        $("#treeLED").removeClass("accessorie");
        $("#treeLED").addClass("accessorieActive");
        $("#treeLEDState").removeClass("accessorieStatusOff");
        $("#treeLEDState").addClass("accessorieStatusOn");
        $("#treeLEDName").removeClass("accessorieNameOff");
        $("#treeLEDName").addClass("accessorieNameOn");
      } else {
        $("#treeLEDState").text("Éteint");
        imgAttribute = "../static/png/lamp3Off.png";

        $("#treeLED").removeClass("accessorieActive");
        $("#treeLED").addClass("accessorie");
        $("#treeLEDState").removeClass("accessorieStatusOn");
        $("#treeLEDState").addClass("accessorieStatusOff");
        $("#treeLEDName").removeClass("accessorieNameOn");
        $("#treeLEDName").addClass("accessorieNameOff");
      }
      img.setAttribute("src", imgAttribute);
    }

    if (data["topic"] == "stat/columnLED/POWER") {
      var img = document.getElementById("columnLEDImg");
      var imgAttribute = img.getAttribute("src");

      if (data["payload"] == "ON") {
        $("#columnLEDState").text("Allumé");
        imgAttribute = "../static/png/lamp1Glow.png";

        $("#columnLED").removeClass("accessorie");
        $("#columnLED").addClass("accessorieActive");
        $("#columnLEDState").removeClass("accessorieStatusOff");
        $("#columnLEDState").addClass("accessorieStatusOn");
        $("#columnLEDName").removeClass("accessorieNameOff");
        $("#columnLEDName").addClass("accessorieNameOn");
      } else {
        $("#columnLEDState").text("Éteint");
        imgAttribute = "../static/png/lamp1Off.png";

        $("#columnLED").removeClass("accessorieActive");
        $("#columnLED").addClass("accessorie");
        $("#columnLEDState").removeClass("accessorieStatusOn");
        $("#columnLEDState").addClass("accessorieStatusOff");
        $("#columnLEDName").removeClass("accessorieNameOn");
        $("#columnLEDName").addClass("accessorieNameOff");
      }
      img.setAttribute("src", imgAttribute);
    }
  });
});
