class ControlsController < ApplicationController
  def index
    response = Client.send_msg('get_temp')
    gon.push current_temp: response['get_temp']
  end
end
