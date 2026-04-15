import time
import psutil
from config import Config
from .system_metrics import get_primary_disk_path

_last_stats = {"cpu":0, "ram":0, "disk":0, "time":0}

def get_quick_stats() -> dict:
  current_time = time.time()
  
  if current_time - _last_stats['time'] > Config.STAT_REFRESH_INTERAL:
    try:
      _last_stats["cpu"] = int(psutil.cpu_percent(interval=0.5))
      _last_stats["ram"] = int(psutil.virtual_memory().percent)
      _last_stats["disk"] = int(psutil.disk_usage(get_primary_disk_path()).percent)
      _last_stats["time"] = current_time
    except Exception:
      pass
    
  return _last_stats