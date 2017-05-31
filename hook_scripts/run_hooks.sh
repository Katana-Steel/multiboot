#!/bin/bash

SRC_LOC=$(dirname $0)
. $SRC_LOC/live-config.hooks.cfg

function active() {
    for a in ${enabled[*]}; do
      [[ "$a" == "$s"]] && return 0
    done
    return 1
}

for s in $SRC_LOC/*.sh; do
  if active $s; then
    $s
  fi
done
