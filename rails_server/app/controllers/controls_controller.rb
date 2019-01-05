class ControlsController < ApplicationController
  def index
    temp = Client.send_msg('get_temp')
    @state = Client::STATE_TRANSLATION[Client.send_msg('get_state')]

    gon.watch.current_temp = temp
    gon.watch.current_state = @state
  end
end
