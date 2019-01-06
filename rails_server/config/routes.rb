Rails.application.routes.draw do
  resources :controls do
    collection do
      get 'send_command'
    end
  end

  root to: "controls#index"
end
