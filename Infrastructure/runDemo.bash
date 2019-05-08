#!/usr/bin/env bash

for ((i = 1 ; i < 5 ; i++)); do
  python main.py "zone_$i"
done



