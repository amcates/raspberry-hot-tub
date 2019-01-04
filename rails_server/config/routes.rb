Rails.application.routes.draw do
  resources :controls

  root to: "controls#index"
end
