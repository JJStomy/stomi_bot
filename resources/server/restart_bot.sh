#!/bin/bash
# Перезапустить бота
systemctl stop bot
systemctl daemon-reload
systemctl enable bot
systemctl start bot