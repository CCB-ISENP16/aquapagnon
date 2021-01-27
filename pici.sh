#!/bin/bash

install_all() {
  # install python pip3
  sudo apt -y update
  sudo apt -y upgrade
  sudo apt -y install python3-pip
  sudo apt -y install python3-smbus
  sudo apt -y install git
  sudo apt -y install mosquitto
  sudo apt -y install mosquitto-clients

  # install python dependencies
  pip3 install paho-mqtt
  pip3 install pyserial
  pip3 install requests
  pip3 install pigpio
  pip3 install pytz
  pip3 install spidev

  pip3 install eventlet
  pip3 install Flask
  pip3 install Flask-MQTT
  pip3 install Flask-SocketIO

  pip3 install Flask-SQLAlchemy
  pip3 install flask-restplus


  # install gpio daemon
  sudo apt -y install pigpio python-pigpio python3-pigpio
  sudo systemctl enable pigpiod.service
}

case $1 in
install)
  install_all
  ;;
*)
  echo "Usage: "
  echo "  run install   : install software and all dependencies. may be used on a raspbian clean install"
  ;;
esac
