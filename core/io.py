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
    
    @staticmethod
    def save_file(data:str) -> bool:
        try:
            if not os.path.exists(Config.OUTPUT_FILE):
                os.makedirs(os.path.dirname(os.path.realpath(Config.OUTPUT_FILE)), exist_ok=True)

            with open(Config.OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(data)
            MsgDCR.SuccessMessage(f"ASCII art saved successfully to: {Config.OUTPUT_FILE}")
            return True
        except Exception as e:
            MsgDCR.FailureMessage(f"Error writing to file: {e}")
            return False
    
    @staticmethod
    def save_writelines_file(data) -> bool:
        try:
            if not os.path.exists(Config.OUTPUT_FILE):
                os.makedirs(os.path.dirname(os.path.realpath(Config.OUTPUT_FILE)), exist_ok=True)

            with open(Config.OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.writelines(data)
            MsgDCR.SuccessMessage(f"ASCII art saved successfully to: {Config.OUTPUT_FILE}")
            return True
        except Exception as e:
            MsgDCR.FailureMessage(f"Error writing to file: {e}")
            return False