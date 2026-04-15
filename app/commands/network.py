import platform
import subprocess
import psutil
from config import Config

def ping_command(cmd: str) -> str:
  host = cmd.split(" ")[1]
  param = "-n" if platform.system().lower() == "windows" else "-c"
  encoding = "cp850" if platform.system().lower() == "windows" else "utf-8"
  result = subprocess.run(
    ["ping", param, str(Config.PING_COUNT), host],
    capture_output=True,
    test=True,
    encoding=encoding
  )
  return result.stdout

def network_command() -> str:
  net_io = psutil.net_io_counters()
  addrs = psutil.net_if_addrs()
  result = "🌐 Informations réseau:\n\n"
  result+= f"Paquets reçu: {net_io.packets_recv }\n"
  result+= f"Paquets envoyés: {net_io.packets_sent }\n"
  result += f"Données envoyées: {net_io.bytes_sent // (2**20)} Mo\n"
  result += f"Données reçus: {net_io.bytes_recv // (2**20)} Mo\n\n"

  result += "Interfaces réseaux:\n"
  for interface, addrs_list in addrs.items():
    result+= f"\n{interface}:\n"
    for addr in addrs_list:
      if addr.family == 2:
        result += f"  IPv4: {addr.address}"
      elif addr.family == 23:
        result += f"  IPv6: {addr.address}"
  return result

def ports_command() -> str:
  connections = psutil.net_connections(kind="inet")
  listening = [conn for conn in connections if conn.status == "LISTEN"]

  result = "🔌 Ports TCP/UDP en écoute:\n\n"
  result += f"{'Protocole:':<10} {'Adresse Locale':<25} {'PID':<10} {'Programme'}\n"
  result += "─" * 80 + "\n"

  seen_ports = set()
  for conn in listening:
    if conn.laddr.port in seen_ports:
      continue
    seen_ports.add(conn.laddr.port)
    try:
      proc = psutil.Process(conn.pid) if conn.pid else None
      proc_name = proc.name() if proc else "N/A"
    except Exception:
      proc_name = "N/A"
    
    proto = "TCP" if conn.type == 1 else "UDP"
    addr = f"{conn.laddr.ip}:{conn.laddr.port}"
    result += f"{proto:<10} {addr:<25} {conn.pid or 'N/A':<10} {proc_name}"
  
  return result