from Map import *
from SequenceRunner import *
from Engine import Engine
from Configurers import *
from Servers import *
from Readers import *
from Interpreters import *
from StarvationMachine import *
from DoomsdayMachine import *
from ActionMachine import *
from Readers import *
from Display import Display

class Dummy:
    def __init__(self):
        pass

    def update(self, tiles):
        pass

class Game:
    def __init__(self, configuration, input, root):
        # Defineste harta, care trebuie sa fie vizibila din toate obiectele
        game_map = Map()
        self.command_buffer = []
        # In functie de parametru, configureaza harta
        if configuration == "Default":
            Configurers.default_configuration(game_map, None)
        elif configuration == "Recommended":
            Configurers.recommended_configuration(game_map, None)
        elif configuration == "FullyOpen":
            Configurers.fully_open_configuration(game_map, None)
        else:
            raise RuntimeError("Bad configuration parameter")
        # Defineste vizualizatorul
        if root:
            self.display = Display(game_map, root)
            for i in game_map.land_hex_list:
                i.display = self.display
        else:
            self.display = Dummy()

        # game_map.direct_ref_matrix[7][8].status = Status.CONTAMINATED
        # game_map.direct_ref_matrix[7][8].hex_type = HexType.ICE
        # UnitManager.add_unit(game_map, [game_map.direct_ref_matrix[7][8], UnitType.SOLDIER, Player.BLUE])
        # UnitManager.add_unit(game_map, [game_map.direct_ref_matrix[7][8], UnitType.CIV, Player.BLUE])
        # UnitManager.add_unit(game_map, [game_map.direct_ref_matrix[7][8], UnitType.CIV, Player.GREY])
        # tiles = [(7, 8)]
        # self.display.update(tiles)


        # In functie de parametru, configureaza cititorii
        if input == "CommandLine":
            reader = CommandLineReader()
        elif input == "GUI":
            reader = GUIReader
        elif input == "File":
            reader = FileReader()
        elif input == "Memory":
            reader = MemoryReader()
        else:
            raise RuntimeError("Bad specification for reader")
        # Defineste componentele pentru obiectul Sequencer pentru starvation
        starvation_interpreter = StarvationInterpreter(game_map)
        starvation_checker = StarvationMachine(game_map)
        starvation_executive = StarvationServer()
        # Defineste componentele pentru obiectul Sequencer pentru action
        action_interpreter = ActionInterpreter(game_map)
        action_checker = ActionMachine(game_map)
        action_executive = ActionServer()
        # Defineste componentele pentru obiectul Sequencer pentru doomsday
        doomsday_interpreter = DoomsdayInterpreter(game_map)
        doomsday_checker = DoomsdayMachine(game_map)
        doomsday_executive = DoomsdayServer()
        # Defineste obiectele Sequencer pentru toate fazele
        starvation_sequencer = SequenceRunner(reader, starvation_interpreter, starvation_checker, starvation_executive)
        action_sequencer = SequenceRunner(reader, action_interpreter, action_checker, action_executive)
        doomsday_sequencer = SequenceRunner(reader, doomsday_interpreter, doomsday_checker, doomsday_executive)
        # Defineste motorul jocului
        self.engine = Engine(starvation_sequencer, action_sequencer, doomsday_sequencer, game_map)

    def __call__(self):
        self.engine.run()


if __name__ == "__main__":
    # Doar pentru test.
    # Programul principal va deschide un fisier de configurare, de unde va afla ce configuratie va folosi,
    # daca va primi comenzi in linie de comanda sau cu interfata grafica, care e fisierul de log etc.
    # Sau va deschide un meniu principal din care sa fie facute toate initializarile
    logging.basicConfig(level=logging.INFO)
    logging.debug('This will get logged')
    game = Game("Default", "File", None)
    game.__call__()



