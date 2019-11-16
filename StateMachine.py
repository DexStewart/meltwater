class StateMachine:
    def __init__(self, game_map):
        self.states = {}
        self.current_state = None
        self.game_map = game_map

    # Comanda, cu informatia aferenta, e executata de starea curenta. Masina de stare e doar dispecer.
    def accept_message(self, cmd, data):
        # Toate starile au nevoie de adresa automatului pentru a defini starea urmatoare, care e stocata in membrul current_state al automatului
        # Din acest motiv, un argument (aici e primul, dar putea fi pe orice pozitie) cu care e chemata functia starii curente e adresa automatului
        # Functionare: dupa ce starea curenta a prelucrat comanda si a generat iesirile e inlocuita de starea urmatoare
        return self.states[self.current_state](cmd, data)

    # Metoda chemata de functiile de stare ale acestui automat pentru a defini starea urmatoare
    def set_state(self, new_state):
        self.current_state = new_state

    # Metoda chemata daca stari ale altor automate au nevoie sa stie, pentru functiile lor de decizie, in ce stare se afla acest automat
    # Nu stiu ce e mai bine de intors: obiectul "stare" sau identificatorul lui din enumerare. Aici intorc obiectul. Isentificatorul ar trebui gasit sau memorat anterior
    def get_state(self):
        return self.current_state




# game start
#
# Parser:
# [cmd] [source hex] [unit identities] [target]
#
# Command examples:
#
# Starvation:
# SRESOLVE [cmd] [target]
# FLEE [cmd] [source hex] [target] [unit identity1]
# DEFECT [cmd] [source hex] [target] [unit identity1]
# DIE [cmd] [source hex] [unit identity]
# SEND
#
# Action:
# MARCH [cmd] [source hex] [target] [unity identity1] [unit identity2] ...
# THREATEN [cmd] [source hex] [target] [march target]* * special
# code XX for 'no valid march target so remove unit'
# PRESSGANG [cmd] [source hex] [target] [march target]* * special
# code XX for 'do not move'
# TRANSPORT [cmd] [source hex] [target]
# ATTACK [cmd] [source hex] [target]
# POLLUTE [cmd] [target]
# MILITARIZE [cmd] [target1] [target2]* * special code XX for "no
# second target"
# PASS [cmd]
# AEND
#
# Doomsday:
# DRESOLVE [cmd] [target]
# KILLHEX [cmd] [target]
# ADDCIV [cmd] [target]
# DEND
#
# CleanUp:
# REVEAL [cmd]
# alternate: [cmd] [card code]
#
#
#
# unit identity codes:
# bc bs Blue civ/soldier
# rc rs Red civ/soldier
# gc Grey civ
# sc supply center
