import json
import sys
import subprocess
import threading
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import pystray

from metrics import Metrics
from paths import ensure_user_config

BASE_DIR = Path(__file__).parent.parent
_LOCAL_CONFIG_PATH = BASE_DIR / "conf" / "config.json"
CONFIG_PATH = _LOCAL_CONFIG_PATH if _LOCAL_CONFIG_PATH.exists() else ensure_user_config()
GUI_SCRIPT = Path(__file__).parent / "led_display_ui.py"
PYTHON_BIN = sys.executable


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def write_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


def make_icon_image(text, color="white"):
    size = 64
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]), text, fill=color, font=font)
    return image


class TrayApp:
    def __init__(self):
        self.metrics = Metrics()
        self.config = load_config()
        self.icon = pystray.Icon(
            "cpu-cooler-lcd",
            make_icon_image("--"),
            "CPU Cooler LCD",
            menu=self.build_menu(),
        )

    def build_menu(self):
        return pystray.Menu(
            pystray.MenuItem(
                "Display On",
                self.toggle_display,
                checked=lambda item: self.config.get("enabled", True),
            ),
            pystray.MenuItem("Open Settings", self.open_settings),
            pystray.MenuItem("Quit Tray Icon", self.quit),
        )

    def toggle_display(self, icon, item):
        self.config = load_config()
        self.config["enabled"] = not self.config.get("enabled", True)
        write_config(self.config)
        self.icon.update_menu()

    def open_settings(self, icon, item):
        subprocess.Popen([PYTHON_BIN, str(GUI_SCRIPT), str(CONFIG_PATH)])

    def quit(self, icon, item):
        self.icon.stop()

    def update_loop(self):
        temp_unit = {"cpu": "celsius", "gpu": "celsius"}
        while True:
            try:
                self.config = load_config()
                temp_unit = {
                    "cpu": self.config.get("cpu_temperature_unit", "celsius"),
                    "gpu": self.config.get("gpu_temperature_unit", "celsius"),
                }
                metrics_vals = self.metrics.get_metrics(temp_unit)
                cpu_temp = metrics_vals["cpu_temp"]
                gpu_temp = metrics_vals["gpu_temp"]
                unit_c = "C" if temp_unit["cpu"] == "celsius" else "F"
                unit_g = "C" if temp_unit["gpu"] == "celsius" else "F"
                self.icon.icon = make_icon_image(str(cpu_temp))
                self.icon.title = f"CPU: {cpu_temp}°{unit_c}  GPU: {gpu_temp}°{unit_g}"
            except Exception as e:
                print(f"Error updating tray: {e}")
            time.sleep(2)

    def run(self):
        threading.Thread(target=self.update_loop, daemon=True).start()
        self.icon.run()


if __name__ == "__main__":
    TrayApp().run()
