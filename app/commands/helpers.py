import datetime

def build_progress_bar(percent: float, width: int=20) -> str:
  filled = int(percent // 5)
  return "█" * filled + "░" * (width - filled)

def to_gb(value: int) -> int:
  return value // (2**30)

def format_boot_time(timestamp: float) -> str:
  return datetime.datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y à %H:%M:%S")