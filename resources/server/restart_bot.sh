#!/bin/bash
# Перезапустить бота
systemctl stop bot

# по сути только стоп, демон поднимется автоматически
#systemctl daemon-reload
#systemctl enable bot
#systemctl start bot