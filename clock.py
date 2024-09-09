import network
import utime
import ntptime



class DummyClock(object):

    def __init__(self):
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        self.sta_if.connect('Enjoi_2.4-22990', 'Din0sauri0')

        if self.sta_if.isconnected():
            print('Conectado a la red Wi-Fi')
            print('Configuración IP:', self.sta_if.ifconfig())
        else:
            print('No conectado')


    def plug_wifi(self):
        utime.sleep(3)
        self.sta_if.connect('Enjoi_2.4-22990', 'Din0sauri0')
        print('Conectado a la red Wi-Fi')
        print('Configuración IP:', self.sta_if.ifconfig())

    def sincronize_ntp_server(self):
        ntptime.settime()

    def calc_your_time(self, hours_diff):
        return utime.localtime(utime.mktime(utime.localtime()) - hours_diff * 3600)

    def disconnect_from_wifi(self):
        if self.is_connected:
            self.sta_if.disconnect()
            self.sta_if.active(False)
            print('Desconectado de la RED')


    @property
    def is_connected(self):
        return self.sta_if.isconnected()
