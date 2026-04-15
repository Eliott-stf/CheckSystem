import datetime
import platform
import time

import psutil

from config import Config

from .helpers import build_progress_bar, format_boot_time, to_gb


def cpu_command() -> str:
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_avg = psutil.cpu_percent(interval=1)
    result = f"⚙️ CPU Utilisation Globale: {cpu_avg}%\n\n"
    result += "Détails par cœur:\n"
    for index, percent in enumerate(cpu_percent): # enumerate sert à
        result += f"  Core {index}: {build_progress_bar(percent)} {percent}%\n"
    return result


def ram_command() -> str:
    mem = psutil.virtual_memory()
    return (
        f"🧠 RAM Utilisée: {mem.percent}%\n"
        f"   {build_progress_bar(mem.percent)}\n\n"
        f"   Total: {to_gb(mem.total)} Go\n"
        f"   Utilisé: {to_gb(mem.used)} Go\n"
        f"   Disponible: {to_gb(mem.available)} Go\n"
        f"   Libre: {to_gb(mem.free)} Go"
    )


def disk_space_command() -> str:
    parts = psutil.disk_partitions()
    lines = ["💾 État des Disques:\n"]
    for part in parts:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            lines.append(f"\n{part.device} ({part.fstype})")
            lines.append(f"  {build_progress_bar(usage.percent)} {usage.percent}%")
            lines.append(f"  Total: {to_gb(usage.total)} Go")
            lines.append(f"  Utilisé: {to_gb(usage.used)} Go")
            lines.append(f"  Libre: {to_gb(usage.free)} Go")
        except PermissionError:
            pass
    return "\n".join(lines)


def uptime_command() -> str:
    boot_timestamp = psutil.boot_time()
    uptime_seconds = datetime.datetime.now().timestamp() - boot_timestamp
    uptime_days = int(uptime_seconds // 86400)
    uptime_hours = int((uptime_seconds % 86400) // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)
    return (
        f"🕰️ Système démarré le: {format_boot_time(boot_timestamp)}\n"
        f"   Uptime: {uptime_days}j {uptime_hours}h {uptime_minutes}min"
    )


def system_info_command() -> str:
    uname = platform.uname()
    return (
        f"💻 Informations Système:\n\n"
        f"Système: {uname.system}\n"
        f"Nom PC: {uname.node}\n"
        f"Version: {uname.version}\n"
        f"Architecture: {uname.machine}\n"
        f"Processeur: {uname.processor or platform.processor()}\n"
        f"Cœurs physiques: {psutil.cpu_count(logical=False)}\n"
        f"Cœurs logiques: {psutil.cpu_count(logical=True)}\n"
        f"RAM totale: {to_gb(psutil.virtual_memory().total)} Go\n"
        f"Démarré le: {format_boot_time(psutil.boot_time())}"
    )


def dashboard_command() -> str:
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk_path = "C:\\" if platform.system() == "Windows" else "/"
    disk = psutil.disk_usage(disk_path)
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_str = f"{int(uptime_seconds // 86400)}j {int((uptime_seconds % 86400) // 3600)}h"

    result = "═" * 60 + "\n"
    result += "                    📊 DASHBOARD SYSTÈME                    \n"
    result += "═" * 60 + "\n\n"
    result += f"🖥️  SYSTÈME: {platform.system()} {platform.release()}\n"
    result += f"💻 PC: {platform.node()}\n"
    result += f"🕰️  Uptime: {uptime_str}\n\n"
    result += "─" * 60 + "\n"
    result += "📊 RESSOURCES:\n"
    result += "─" * 60 + "\n"
    result += f"⚙️  CPU:    {build_progress_bar(cpu)} {cpu}%\n"
    result += f"🧠 RAM:    {build_progress_bar(mem.percent)} {mem.percent}% ({to_gb(mem.used)}/{to_gb(mem.total)} Go)\n"
    result += f"💾 Disque: {build_progress_bar(disk.percent)} {disk.percent}% ({to_gb(disk.used)}/{to_gb(disk.total)} Go)\n\n"

    processes = []
    for proc in psutil.process_iter(["name", "cpu_percent"]):
        try:
            processes.append(proc.info)
        except Exception:
            pass
    processes = sorted(processes, key=lambda item: item["cpu_percent"] or 0, reverse=True)[:3]

    result += "─" * 60 + "\n"
    result += "🔄 TOP 3 PROCESSUS:\n"
    result += "─" * 60 + "\n"
    for index, proc in enumerate(processes, 1):
        result += f"{index}. {proc['name']:<30} {proc['cpu_percent'] or 0:.1f}%\n"

    net = psutil.net_io_counters()
    result += f"\n─" + "─" * 59 + "\n"
    result += "🌐 RÉSEAU:\n"
    result += "─" * 60 + "\n"
    result += f"📤 Envoyé:  {net.bytes_sent // (2**20):,} Mo\n"
    result += f"📥 Reçu:    {net.bytes_recv // (2**20):,} Mo\n"
    result += "\n" + "═" * 60
    return result


def health_command() -> str:
    result = "❤️  SANTÉ SYSTÈME GLOBALE\n"
    result += "═" * 60 + "\n\n"

    health_score = 100
    warnings = []

    cpu = psutil.cpu_percent(interval=1)
    if cpu > Config.CPU_CRITICAL_THRESHOLD:
        health_score -= Config.HEALTH_PENALTY_CPU_CRITICAL
        warnings.append("⚠️  CPU critique (>90%)")
        result += f"⚙️  CPU: ❌ CRITIQUE ({cpu}%)\n"
    elif cpu > Config.CPU_WARNING_THRESHOLD:
        health_score -= Config.HEALTH_PENALTY_CPU_HIGH
        warnings.append("⚠️  CPU élevé (>70%)")
        result += f"⚙️  CPU: ⚠️  ÉLEVÉ ({cpu}%)\n"
    else:
        result += f"⚙️  CPU: ✅ NORMAL ({cpu}%)\n"

    mem = psutil.virtual_memory()
    if mem.percent > Config.RAM_CRITICAL_THRESHOLD:
        health_score -= Config.HEALTH_PENALTY_RAM_CRITICAL
        warnings.append("⚠️  Mémoire critique (>90%)")
        result += f"🧠 RAM: ❌ CRITIQUE ({mem.percent}%)\n"
    elif mem.percent > Config.RAM_WARNING_THRESHOLD:
        health_score -= Config.HEALTH_PENALTY_RAM_HIGH
        warnings.append("⚠️  Mémoire élevée (>75%)")
        result += f"🧠 RAM: ⚠️  ÉLEVÉ ({mem.percent}%)\n"
    else:
        result += f"🧠 RAM: ✅ NORMAL ({mem.percent}%)\n"

    disk_path = "C:\\" if platform.system() == "Windows" else "/"
    disk = psutil.disk_usage(disk_path)
    if disk.percent > Config.DISK_CRITICAL_THRESHOLD:
        health_score -= Config.HEALTH_PENALTY_DISK_CRITICAL
        warnings.append("⚠️  Disque plein (>90%)")
        result += f"💾 Disque: ❌ PLEIN ({disk.percent}%)\n"
    elif disk.percent > Config.DISK_WARNING_THRESHOLD:
        health_score -= Config.HEALTH_PENALTY_DISK_HIGH
        warnings.append("⚠️  Disque rempli (>80%)")
        result += f"💾 Disque: ⚠️  REMPLI ({disk.percent}%)\n"
    else:
        result += f"💾 Disque: ✅ NORMAL ({disk.percent}%)\n"

    try:
        temps = psutil.sensors_temperatures()
        if temps:
            max_temp = max(entry.current for entries in temps.values() for entry in entries)
            if max_temp > Config.TEMP_CRITICAL_THRESHOLD:
                health_score -= Config.HEALTH_PENALTY_TEMP_HIGH
                warnings.append(f"⚠️  Température élevée ({max_temp}°C)")
                result += f"🌡️  Temp: ⚠️  CHAUD ({max_temp}°C)\n"
            else:
                result += f"🌡️  Temp: ✅ NORMAL ({max_temp}°C)\n"
    except Exception:
        result += "🌡️  Temp: ℹ️  Non disponible\n"

    result += "\n" + "─" * 60 + "\n"
    result += f"\n📊 SCORE DE SANTÉ: {health_score}/100\n\n"

    if health_score >= 90:
        result += "✅ EXCELLENT - Système en parfait état\n"
    elif health_score >= 75:
        result += "✅ BON - Système fonctionne normalement\n"
    elif health_score >= 50:
        result += "⚠️  MOYEN - Surveillance recommandée\n"
    else:
        result += "❌ CRITIQUE - Action immédiate requise\n"

    if warnings:
        result += "\n⚠️  Avertissements:\n"
        for warning in warnings:
            result += f"   {warning}\n"

    return result
 