# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

$ ->
  gauge = new RadialGauge({
    renderTo: 'canvas-id'
    minTicks: '10'
    minValue: '0'
    maxValue: '140'
    majorTicks: [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140]
    value: gon.current_temp
    units: '°F'
    height: '400'
    highlights: [
        {
            "from": 0,
            "to": 90,
            "color": "rgba(0,0, 255, .3)"
        },
        {
            "from": 90,
            "to": 101,
            "color": "rgba(255, 0, 0, .3)"
        },
        {
            "from": 101,
            "to": 105,
            "color": "rgba(127, 191, 63, 1)"
        },
        {
            "from": 105,
            "to": 140,
            "color": "rgba(191, 63, 63, 1)"
        }
    ]
  }).draw();
