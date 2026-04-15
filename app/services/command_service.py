from ..commands.registry import PREFIX_COMMANDS, STATIC_COMMANDS, help_command

def execute_command(cmd: str) ->str:
    try:
        if cmd in ("help", "?"):
            return help_command()
        
        for prefix, handler in PREFIX_COMMANDS.items():
            if cmd.startswith(prefix):
                return handler(cmd)
        handler = STATIC_COMMANDS.get(cmd)
        if handler:
            return handler()
        
        return "Commande inconnue. Tapez 'help' pour voir la liste des commandes"
    except Exception as exc:
        return f"Erreur: {exc}"