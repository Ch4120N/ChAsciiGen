# -*- coding: UTF-8 -*-
# core/io.py


import os
import json

from core.config import Config, DEFAULT_CONFIG
from ui.decorators import MsgDCR

class IO:
    @staticmethod
    def load_config():
        if os.path.exists(Config.CONFIG_FILE):
            try:
                with open(Config.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()

    @staticmethod
    def save_config(data):
        try:
            with open(Config.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            MsgDCR.FailureMessage(f'Failed to save config: {e}')