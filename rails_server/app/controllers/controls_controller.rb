class ControlsController < ApplicationController
  def index
    temp = Client.send_msg('get_temp')
    @state = Client::STATE_TRANSLATION[Client.send_msg('get_state')]

    gon.watch.current_temp = temp
    gon.watch.current_state = @state
  end

  def send_command
    command = params[:command]
    @resp = Client.send_msg(command)
    respond_to do |format|
      format.json { render json: @resp.to_json }
    end
  end
end
