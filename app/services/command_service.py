from ..commands.registry import PREFIX_COMMAND, STATIC_COMMAND, help_command

def execute_command(cmd: str) ->str:
    try:
        if cmd in ("help", "?"):
            return help_command()
        
        for prefix, handler in PREFIX_COMMAND.items():
            if cmd.startswith(prefix):
                return handler(cmd)
        handler = STATIC_COMMAND.get(cmd)
        if handler:
            return handler()
        
        return "Commande inconnue. Tapez 'help' pour voir la liste des commandes"
    except Exception as exc:
        return f"Erreur: {exc}"