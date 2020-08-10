require 'sinatra'

get '/' do
    location = '/sys/bus/w1/devices/28-021892458db6/w1_slave'

    lines = IO.readlines(location)
    last_line = lines.last

    raw_temp = last_line.split("=").last.gsub("\n", "")
    temp_readout = (raw_temp.to_f/1000.0 * 1.8) + 32
    temp_readout += 3 # adding offset
    
    @temp_readout = temp_readout.round(2)

    erb :temp
end
