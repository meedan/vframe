from enum import Enum

def find_type(name, enum_type):
  for enum_opt in enum_type:
    if name == enum_opt.name.lower():
      return enum_opt
  return None

# ---------------------------------------------------------------------
# Logger, monitoring
# --------------------------------------------------------------------

class LogLevel(Enum):
  """Loger vebosity"""
  DEBUG, INFO, WARN, ERROR, CRITICAL = range(5)