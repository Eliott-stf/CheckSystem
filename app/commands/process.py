import psutil
from config import Config

def process_command() -> str:
  processes = []
  for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
    try:
      processes.append(proc.info)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
      pass
  
  processes = sorted(processes, key=lambda item: item['cpu_percent'] or 0, reverse=True)[:Config.MAX_PROCESS_DISPLAY]

  result = "🔄 Top 10 Processus (par CPU):\n\n"
  result += f"{'PID':<8} {'CPU%':<8} {'Nom'}\n"
  result+= "─" * 60 + "\n"
  for proc in processes:
    result += (
      f"{proc['pid']:<8 {proc['cpu_percent'] or 0:<8.1f}}"
      f"{proc['memory_percent'] or 0:<8.1f} {proc['name']}\n"
    )
  return result

def services_command() ->str:
  result = "⚡ Services Système Actifs:\n\n"
  result += f"{'PID':<8} {'Statut':<10} {'RAM%':<8} {'Nom'}"
  result+= "─" * 70 + "\n"

  services = []
  for proc in psutil.process_iter(["pid", "name", "status", "memory_percent", "username"]):
    try:
      if proc.info['username'] and "SYSTEM" in proc.info['username'].upper():services.append(proc.info)
    except Exception:
      pass

  services = sorted(services, key=lambda item: item['memory_percent'] or 0, reverse=True)[: Config.MAX_SERVICES_DISPLAY]

  for service in services:
    status = service['status'][:8] if service['status'] else "N/A"
    result += (
      f"{service['pid']:<8} {status:<10} "
      f"{service['memory_percent'] or 0:<8.2f} {service['name']}\n"
    )
  return result

def kill_command(cmd: str) -> str:
  try:
    pid = int(cmd.split()[1])
    proc = psutil.Process(pid)
    proc_name = proc.name()
    proc.terminate()
    proc.wait(timeout=3)
    return f"✅ Processus {proc_name} (PID: {pid}) arrêté avec succès"
  except psutil.NoSuchProcess:
    return f"❌ Aucun processus avec le PID {pid}"
  except psutil.AccessDenied:
    return f"❌ Permission refusée. Lancer l'application en administrateur"
  except ValueError:
    return f"❌ PID invalide. Utilisez: kill <PID>"
  except Exception as exc:
    return f"❌ Erreur: {exc}"