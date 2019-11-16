import logging
from CommandObject import *
from Hex import *
from UnitManager import *

class SequenceRunner:
    def __init__(self, reader, syntax_checker, semantics_checker, executive):
        self.reader = reader
        self.syntax_checker = syntax_checker
        self.semantics_checker = semantics_checker
        self.executive = executive

    def set_player(self, player):
        self.syntax_checker.player = player
        self.executive.player = player

    @staticmethod
    def report_reading_error(error):
        pass

    @staticmethod
    def report_syntax_error(error):
        pass

    @staticmethod
    def report_semantics_error(cmd):
        pass

    @staticmethod
    def report_execution_failure(cmd):
        pass

    @staticmethod
    def report(info):
        pass

    # Obiect de tip "callable" (un obiect este de tip "callable" daca metoda sa __call_ face ceva), care are o singura metoda (ar putea avea oricate).
    # Nu este functie pentru ca are multe obiecte interne.
    # Daca ar fi functie, toate obiectele interne ar trebui date ca parametri la chemare. Asa, sunt dati o singura data, la constructia obiectului.
    # In plus, apelatorul functiei ar trebui sa cunoasca aceste obiecte, ceea ce trebuie evitat daca se poate.
    # Cand apelatorul obiectului nu e cel care l-a construit (a fost construit de altcineva si dat apelatorului),
    # primul nu are nici un motiv sa stie ce are obiectul in interior.
    def __call__(self, player):
        while True:
            # Extrage un sir de caractere de la intrare, corespunzator unei comenzi. Intrarea poate fi:
            # - un fisier text, pentru teste
            # - consola, pentru joc cu linii de comanda
            # - interfata utilizator, pentru joc cu interfata grafica
            (success, input_data) = self.reader.read()
            if success:
                # Formatul in care e primit mesajul poate sa nu fie cel folosit intern pentru desfasurarea jocului.
                # Verifica sintaxa mesajului. De asemenea, face conversia spre un format de date mai util.
                # In cel mai simplu caz, desparte si copiaza input_data in command si data.
                (success, cmd, data) = self.syntax_checker(input_data, player)
                if success:
                    # Verifica semantica mesajului (comanda are sens? Se poate executa in starea actuala?)
                    # Creeaza obiectul comanda -pentru executia ulterioara- sau obiectul eroare
                    (result_type, executable, error) = self.semantics_checker.accept_message(cmd, data)
                    # Continua in functie de rezultatul verificarii
                    if result_type == OutputType.COMMAND:
                        # Executa comanda
                        success = self.executive.execute(executable)
                        # Verifica daca, dupa executia comenzii, jocul a fost lasat intr-o stare consistenta si corecta
                        # In cel mai bun caz, nu face nimic si intoarce True, pentru ca verificarea preconditiei a fost suficienta
                        if success:
                            # Comanda executata corect
                            SequenceRunner.report("OK")
                            if self.semantics_checker.current_state.value == RESET_CODE:
                                # Daca a ajuns din nou in starea RESET, inseamna ca s-a incheiat faza
                                return True
                        else:
                            SequenceRunner.report_execution_failure(executable)
                    elif result_type == OutputType.SURRENDER:
                        return False
                    elif result_type == OutputType.DO_NOTHING:
                        SequenceRunner.report("Nothing to do")
                    elif result_type == OutputType.IGNORED:
                        SequenceRunner.report("Ignored cmd")
                    elif result_type == OutputType.ERROR:
                        SequenceRunner.report_semantics_error("Semantics error")
                    else:
                        raise TypeError("Wrong cmd result type")
                else:
                    SequenceRunner.report_syntax_error("Syntax error")
            else:
                SequenceRunner.report_reading_error("Reading error")

    player = property(None, set_player)

