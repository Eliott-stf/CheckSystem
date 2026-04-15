import platform
import psutil

def get_primary_disk_path() ->str:
  return "C:\\" if platform.system() == "windows" else "/"

def get_live_monitoring_data() -> dict:
  cpu_percent = psutil.cpu_percent(interval=0.5)
  cpu_freq = psutil.cpu_freq()
  cpu_count_physical = psutil.cpu_count(logical=False)
  cpu_count_logical = psutil.cpu_count(logical=True)

  mem = psutil.virtual_memory()
  disk = psutil.disk_usage(get_primary_disk_path())
  net = psutil.net_io_counters()

  return {
    "cpu": round(cpu_percent, 1),
    "cpu_freq": cpu_freq.current if cpu_freq else 0,
    "cpu_cores": cpu_count_physical,
    "cpu_threads": cpu_count_logical,
    "ram": round(mem.percent, 1),
    "ram_total": mem.total,
    "ram_used": mem.used,
    "ram_available": mem.available,
    "disk": round(disk.percent, 1),
    "disk_total": disk.total,
    "disk_used": disk.used,
    "disk_free": disk.free,
    "network": {
      "sent": net.bytes_sent,
      "recv": net.bytes_recv,
      "packets_sent": net.packets_sent,
      "packets_recv": net.packets_recv
    }
  }