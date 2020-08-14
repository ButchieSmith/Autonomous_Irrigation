#Bernard Smith
#waterWeb.py
#Utilizes Flask to create a webserver to monitor system activity.

#This flask server is temporary until I can implement a full LAMP stack
# to provide the server for this system

from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import water
import os

application = Flask(__name__) #Create the server application

#Provides a template to render into the server upon action
def template(title = "Hello!", text = ""):
  now = datetime.datetime.now()
  timeStr = now
  tempDate = {
    'title' : title,
    'time' : timeStr,
    'text' : text
  }
  return tempDate


#Main server page
@application.route("/")
def intro():
  templateData = template()
  return render_template('main.html', **templateData)


#Provide last watered time and date
@application.route("/lastWatered")
def checkWatered():
  templateData = template(text = water.lastWatered())
  return render_template('main.html', **templateData)


#Gets sensor status; tells whether it needs to be watered or not
@application.route("/sensor")
def status():
  currentStatus = water.getStatus()
  msg = ""
  if (currentStatus == 1):
    msg = "Plant needs water!"
  else:
    msg = "Plant is watered!"
  templateData = template(text = msg)
  return render_template('main.html', **templateData)


#Turn water on from server
@application.route("/water")
def action():
  water.pumpOn();
  templateData = template(text = "Plant has been watered.")
  return render_template('main.html', **templateData)


#Toggle the autonomous watering
@application.route("/auto/water/<toggle>")
def autoWater(toggle):
  running = False
  if toggle == "ON":
    templateData = template(text = "Autonomous watering is on.")
    for p in psutil.process_iter():
      try:
        if p.cmdline()[1] == 'autoWater.py':
          templateData = template(text = "Autonomous watering is already on!")
          running = true
      except:
        pass
    if not running:
      os.system("python3 autoWater.py&")
  else:
    templateData = template(text = "Autonomous watering is off.")
    os.system("pkill -f water.py")

  return render_template('main.html', **templateData)


if __name__ == "__main__":
  application.run(host='0.0.0.0', port=80, debug=True)
