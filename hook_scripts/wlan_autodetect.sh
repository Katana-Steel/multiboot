#!/bin/bash


old_ifs=$IFS
IFS=$'\n'
for hw in $(lspci); do
  if [[ "${hw}" =~ Network ]]; then
    echo -n ''
  fi
done
IFS=$IFS
