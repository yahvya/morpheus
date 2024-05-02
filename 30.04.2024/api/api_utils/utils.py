"""
    @brief Utilitaires de l'api
"""

import os
from cryptography.fernet import Fernet

"""
    @brief Extension customisé de l'application
"""
class CustomException(Exception):
    """
        @param message d'erreur
        @param is_displayable Si le message peut être affiché à l'utitilisateur
    """
    def __init__(self, message: str, is_displayable: bool = True) -> None:
        super().__init__(message)
        self.is_displayable = is_displayable

    def get_error_message(self,default_message: str = "Une erreur s'est produite lors du traitement") -> str:
        return default_message if not self.is_displayable else str(self)

"""
    @brief Vérifie la signature
    @param signature signature à vérifier
    @return si la signature est valide
"""
def check_signature(signature: str):
    try:
        with open(f"{os.path.dirname(__file__)}/secret.txt") as secret_config_file:
            try:
                key = secret_config_file.readline()
                expected_message = secret_config_file.readline()

                # comparaison de la signature reçue avec le message attendu 
                encryption_manager = Fernet(key= key.encode())
                
                try:
                    decrypted = encryption_manager.decrypt(token= signature.encode())

                    if not decrypted.decode() == expected_message:
                        raise Exception()
                except:
                    raise CustomException(message= "Vous n'êtes pas autorisé à utiliser cette fonctionnalité")
            except CustomException as e:
                raise e
            except:
                raise CustomException(message= "Echec de vérification de la provenance")
    except CustomException as e:
        raise e
    except:
        raise CustomException(message= "Echec de vérification de la provenance")