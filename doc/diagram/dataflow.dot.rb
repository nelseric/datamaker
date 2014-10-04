#!/usr/bin/env ruby

require 'graphviz/dsl'


digraph :G do
  cluster_training do
    graph[color: "red", label: "Training"]
    edge[color: "red"]

    (dukdata << base_hdf)[label: "Convert Tick data to OHLCV"]
    (base_hdf << experiment)[label: "Generate experiment features"]
    (experiment << training_data)[label: "Create Training Data from experiment features"]

    (training_data << water)[label: "Train NN Model"]
  end

  cluster_predicting do
    graph[color: "blue", label: "Predition/Market Manager"]
    edge[color: "blue"]

    (oanda << broker)[label: "Collect Recent Data"]

    (broker << experiment)[label: "Use recent data to produce features for a prodiction"]
    (experiment << water)[label: "Send Prediction features to NN Model"]
    (water << broker)[constraint: false, label: "Send prediction to broker"]
    (broker << oanda)[constraint: false, label: "Place order based on prediction"]
  end

  experiment[label: "Experiment"]
  broker[label: "Broker Driver"]
  oanda[label: "OANDA"]
  graph[label: "Training"]
  dukdata[label: "Tick Data"]
  base_hdf[label: "OHLCV Data"]
  training_data[label: "Training Data"]
  water[label: "H2O NN Model"]


  graph[label: "Data Flow Diagram"]
  output png: "dataflow.png"
end
