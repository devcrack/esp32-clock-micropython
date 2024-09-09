# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import utime
from machine import (Pin, RTC)
# Local
from tm1637 import TM1637
from clock import DummyClock

def example_measure_time():
    ts = utime.time()
    sum_x = 0
    
    for i in range(1000000):
            sum_x += i
    utime.sleep(3)

    print(f"Elapsed time:{utime.time() - ts} seconds")

def blink_led_board_by_a_minute():
    p = Pin(2, Pin.OUT)
    ts = utime.time()

    while True:
        p.value(1)
        utime.sleep(0.3)
        p.value(0)
        utime.sleep(0.3)
        elapsed = utime.time() - ts

        if elapsed > 59:
            break


def dummy_pomodoro():
    board_led = Pin(2, Pin.OUT)
    display = TM1637(clk=Pin(13), dio=Pin(4))
    
    for i in range (1, 2700):
        val = 2701 - i        
        display.show(str(val))
        board_led.value(0)
        utime.sleep(0.5)
        board_led.value(1)
        utime.sleep(0.5)

    display.write([0b00111001, 0b00111111, 0b00111111, 0b00111000])
    utime.sleep(5)
    display.show('0000')
    for i in range(1, 500):
        val = 501 - i
        display.show(str(val))
        utime.sleep(1)


def blink_board_led(led_pin, how_many_times):
    for i in range(how_many_times):
        led_pin.value(0)
        utime.sleep(0.5)
        led_pin.value(1)
        utime.sleep(0.5)
    return 1


def core_function(counter, d, led):    
    for i in range(counter, 0, -1):
        for j in range(59, 0, -1):
            d.numbers(i, j)
            blink_board_led(led, 1)
            

def leds_off(d):
    d.write([0, 0, 0, 0])
    d.show('    ')

    
def blink_cool(disp):
    leds_off(disp)
    
    for i in range(0, 6):
        disp.write([0b00111001, 0b00111111, 0b00111111, 0b00111000])
        utime.sleep(0.5)
        leds_off(disp)
        utime.sleep(0.5)
        
            
def pomodoro_v0(how_many):
    board_led = Pin(2, Pin.OUT)
    display = TM1637(clk=Pin(13), dio=Pin(4))
    # DummyClock()
    leds_off(display)
    core_function(29, display, board_led)
    blink_cool(display)
    core_function(9, display, board_led)


def try_to_connect(display, dummy_clock):
    while not dummy_clock.is_connected:
        leds_off(display)
        display.scroll("UnU", 500)
        dummy_clock.plug_wifi()


def ini_board_clock(simple_clock, _rtc):
    simple_clock.sincronize_ntp_server()
    (year, month, day, hour, minute, second, weekday, yearday) = simple_clock.calc_your_time(6)
    _rtc.datetime((year, month, day, 0, hour, minute, second + 5, 0))


def dummy_clock():
    board_led = Pin(2, Pin.OUT)
    display = TM1637(clk=Pin(13), dio=Pin(4))
    dummy_clock = DummyClock()
    rtc = RTC()

    display.scroll("HOLI ANDER", 800)
    display.scroll("HOLI ANDREA", 800)

    if not dummy_clock.is_connected:
        try_to_connect(display, dummy_clock)

    ini_board_clock(dummy_clock, rtc)
    dummy_clock.disconnect_from_wifi()

    while True:
        display.numbers(rtc.datetime()[4], rtc.datetime()[5])
        blink_board_led(board_led, 30)




if __name__ == "__main__":
    print("Hello from ESP32")
    dummy_clock()
    

