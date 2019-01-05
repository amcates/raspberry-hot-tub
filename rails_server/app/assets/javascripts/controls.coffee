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

  refreshGauge = (data) ->
    gauge = document.gauges.get('canvas-id')
    gauge.value = data

  updateState = (data) ->
    $('#state-button').removeClass()
    $('#state-button').html(data[0])
    $('#state-button').addClass('btn').addClass(data[1]).addClass('btn-block')

  gon.watch('current_temp', interval: 20000, url: '/controls', refreshGauge)
  gon.watch('current_state', interval: 20000, url: '/controls', updateState)
