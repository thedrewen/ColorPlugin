from endstone.plugin import Plugin
from endstone.command import CommandSender, Command
from endstone.form import ActionForm, Button
from color_plugin.src.utils import sendCustomNameToPlayerForPlayer
from endstone import Player

class ColorPlugin(Plugin):

    api_version = "0.10"

    commands = {
        "color" : {
            "description" : "Configures the color of a player.",
            "usages" : ["/color [player: player]"],
            "permissions" : ["color.command.default"]
        },
        "listcolor" : {
            "description" : "Displays the list of colored players.",
            "usages" : ["/listcolor"],
            "permissions" : ["color.command.default"]
        }
    }

    permissions = {
        "color.command.default": {
            "description": "Allow users to use commands.",
            "default": True,
        }
    }

    def on_enable(self) -> None:
        self.logger.info("Plugin enabled!")
        self.server.scheduler.run_task(self, self.run_clock, delay=0, period=1)

    def on_disable(self) -> None:
        self.logger.info("Plugin disabled!")

    names_color = {}
    clock = 0
    colors = ['', '§c', '§e', '§a', '§d', '§b', '§u']

    def run_clock(self):

        self.clock += 1
        self.updateColors()

    def updateColors(self):
        for player in self.server.online_players:
            if player.name in list(self.names_color.keys()):
                for playerName, color in self.names_color[player.name].items():
                    player_target = self.server.get_player(playerName)
                    if player_target:
                        sendCustomNameToPlayerForPlayer(player, player_target.runtime_id, f'{self.colors[color]}{player_target.name_tag}')

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:

        if command.name == "color":
            if isinstance(sender, Player):
                player: Player = sender

                if(len(args) > 0):
                    player_target : Player = self.server.get_player(args[0])

                    if player_target == None:
                        player.send_error_message('§cPlayer not found!')
                        return False

                    def formColors(player : Player, color: int):
                        if player.name in self.names_color:
                            self.names_color[player.name][f'{player_target.name}'] = color
                        else:
                            self.names_color[player.name] = {
                                f'{player_target.name}' : color
                            }

                    player.send_form(ActionForm('Colors', 'Choose a color:', [Button('Reset'), Button('§cRed'), Button('§eYellow'), Button('§aGreen'), Button('§dPink'), Button('§bBlue'), Button('§uPurple')], formColors))
                else:
                    player.send_error_message(' '.join(command.usages))
                    return False
        elif command.name == "listcolor":
            if isinstance(sender, Player):
                player: Player = sender

                if not player.name in self.names_color:
                    player.send_message("§cNo player has a color configured.")
                    return True

                result = []
                for player_name, color in self.names_color[player.name].items():
                    result.append(f'- {self.colors[color]}{player_name}§r')

                player.send_message(f'§eList of colored players:\n{'\n'.join(result)}')

        return True