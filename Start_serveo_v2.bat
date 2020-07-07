@echo off
start ssh -o ServerAliveInterval=60 -R YOUR DOMAIN:80:127.0.0.1:5000 serveo.net
