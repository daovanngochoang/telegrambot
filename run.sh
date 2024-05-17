#!/bin/bash
sudo systemctl start docker 


echo "Please login to GHCR using github account and TOKEN."

# read -p "Enter github Username:" username

read -p "Please type your name:" username

read -s -p "Password: " pasword

echo "$username $password"

docker login ghcr.io -u $username -p $pasword

# docker login ghcr.io -u $username --password-stdin 

docker pull ghcr.io/inbox-team/telegrambot:main

docker run telegrambot 
