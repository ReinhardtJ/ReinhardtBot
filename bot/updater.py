import os
import sys
import logging
import shutil

from bot import bot_token_provider


class Updater:



    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.abs_path = os.path.dirname(os.path.abspath(__file__))

    def update(self, user_update_token: str) -> None:
        update_token = bot_token_provider.BotTokenProvider().update_token
        if user_update_token != update_token:
            self.logger.info('update token incorrect')
        else:
            self.logger.info('update token correct')
            self.fetch_source_files()
            self.update_source_files()
            self.restart()

    def fetch_source_files(self):
        temp_repository_path = os.path.join(self.abs_path, '')
        if os.path.exists(temp_repository_path):
            shutil.rmtree(temp_repository_path)
            os.system('git clone https://github.com/ReinhardtJ/ReinhardtBot.git')
        pass

    def update_source_files(self):
        pass

    def restart(self):
        pass


Updater().update("")
