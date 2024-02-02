##
# @author https://github.com/yahvya/

##
# @brief exception custom permettant l'ajout d'un statut message affichable ou non
class CustomException(Exception):
    def __init__(self, error, is_displayable):
        super(CustomException, self).__init__(error)

        self.is_displayable = is_displayable

    ##
    # @return le message d'erreur s'il peut être affiché sinon le message par défaut
    def get_error_message(self):
        return str(self) if self.is_displayable else "Une erreur s'est produite"

    ##
    # @return si l'exception peut être affiché
    def get_is_displayable(self):
        return self.is_displayable
