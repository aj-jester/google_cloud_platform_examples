#!/bin/bash

sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" > /etc/sysctl.d/40-ip-forwarding.conf

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables-save
