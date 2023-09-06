import yaml
from system.singleton import singleton
import os


@singleton
class YamlConfig:
    def __init__(self, file_path=os.path.join(os.getcwd(), "config", "config.yaml")):
        self.file_path = file_path
        self.load_config()

    def load_config(self):
        try:
            with open(self.file_path, mode="r", encoding="utf-8") as file:
                self.config = yaml.safe_load(file)
            self.status = True
        except Exception as e:
            self.err = f"异常错误, {e}"
            self.status = False

    def get_config(self):
        if self.status:
            return self.config
        else:
            return None

    def save_config(self, new_config):
        try:
            with open(self.file_path, "w") as file:
                yaml.safe_dump(new_config, file, default_flow_style=False)
            return True
        except Exception as e:
            self.err = f"异常错误, {e}"
        return False
