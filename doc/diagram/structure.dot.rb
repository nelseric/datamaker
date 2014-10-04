#!/usr/bin/env ruby

require 'graphviz/dsl'

# A depends on B
def deps node, dep_nodes
  dep_nodes.each do |n|
    (n << node)[style: "dashed", color: "blue"]
  end
end

def object node, label
  node[label: label]
end

def inherits node_sub, node_super
  (node_sub << node_super)
end



digraph :G do
  graph[label: "Dependency Graph"]

  object feature, "datamaker.Feature"

  inherits indicator, feature
  inherits result, feature

  cluster_indicators do
    graph[label: "datamaker.indicator.*", style: "rounded,dotted"]
    object indicator, "some_indicator.SomeIndicator"
  end

  cluster_results do
    graph[label: "datamaker.result.*", style: "rounded,dotted"]
    object result, "should_buy.ShouldBuy"
  end


  object broker, "datamaker.Broker"
  object oandapy, "ext.oandapy"
  object oanda_broker, "datamaker.brokers.OandaBroker"
  inherits oanda_broker, broker
  deps oanda_broker, [oandapy]

  object experiment, "datamaker.Experiment"
  deps experiment, [feature]

  object water, "datamaker.water"

  object manager, "MarketManager"
  deps manager, [experiment, broker, water]

  output png: "structure.png"
end
