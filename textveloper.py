#coding=utf-8
# Programado por:
#    Israel Fermín Montilla <iferminm@gmail.com>
from metaclasses import Singleton
import simplejson
import requests
import time

class Textveloper(object):
    api_url = 'http://api.textveloper.com/{0}/'


class API(Textveloper):
    """
    Implementación del API para sub-cuentas
    de Textveloper
    """
    def __init__(self, cuenta_token, sub_token):
        super(API, self).__init__()
        self.account_token = cuenta_token
        self.token = sub_token
        
    def enviar_mensaje(self, telefono, mensaje):
        """docstring for enviar_mensaje"""
        payload = {
            'cuenta_token': self.account_token,
            'subcuenta_token': self.token,
            'telefono': telefono,
            'mensaje': mensaje
        }
        request_url = self.api_url.format('enviar')
        response = requests.post(request_url, data=payload)

        return simplejson.loads(response.content)

    def enviar_mensaje_masivo(self, telefonos, mensaje):
        """
        docstring
        """
        responses = {}.fromkeys(telefonos)

        for telefono in telefonos:
            time.sleep(1)
            responses[telefono] = self.enviar_mensaje(telefono, mensaje)
            

        return responses

    def consultar_puntos(self):
        """docstring for consultar_puntos"""
        payload = {
            'cuenta_token': self.account_token,
            'subcuenta_token': self.token
        }
        request_url = self.api_url.format('saldo-subcuenta')
        response = requests.post(request_url, data=payload)

        return eval(response.content) # Debido a un error en el API retorna un json mal formado

    def historial_transferencias(self):
        """docstring for historial_transferencias"""
        payload = {
            'cuenta_token': self.account_token, 
            'subcuenta_token': self.token
        }
        request_url = self.api_url.format('historial-transferencias')
        response = requests.post(request_url, data=payload)

        return simplejson.loads(response.content)

    def historial_mensajes(self):
        """
        docstring
        """
        payload = {
            'cuenta_token': self.account_token,
            'subcuenta_token': self.token
        }
        request_url = self.api_url.format('historial-envios')
        response = requests.post(request_url, data=payload)

        return simplejson.loads(response.content)


class AccountManager(Textveloper):
    """
    Clase que interactúa con el api para envío de 
    mensajes de texto
    """
    __metaclass__ = Singleton

    sub_accounts = {}

    def __init__(self, cuenta_token, registro_subcuentas=True):
        super(Textveloper, self).__init__()
        self.token = cuenta_token
        self.memoizing = registro_subcuentas

    def api_subcuenta(self, sub_token):
        if self.memoizing: 
            if sub_token not in AccountManager.sub_accounts.keys():
                AccountManager.sub_accounts[sub_token] = API(cuenta_token=self.token, sub_token=sub_token)

            return AccountManager.sub_accounts[sub_token]

        return API(cuenta_token=self.token, sub_token=sub_token)

    def consultar_puntos(self):
        """docstring for saldo_cuenta"""
        payload = {'cuenta_token': self.token}
        request_url = self.api_url.format('saldo-cuenta')
        response = requests.post(request_url, data=payload)
        return eval(response.content)  # Debido a un error en el API retorna un json mal formado

    def historial_compras(self):
        """docstring for historial_transferencias"""
        payload = {'cuenta_token': self.token}
        request_url = self.api_url.format('historial-compras')
        response = requests.post(request_url, data=payload)

        return simplejson.loads(response.content)
