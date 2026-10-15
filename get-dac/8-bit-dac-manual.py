import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
leds = [16, 20, 21, 25, 26, 17, 27, 22]
GPIO.setup(leds, GPIO.OUT)
dynamic_range = 3.17

def Voltage_number(voltage):
    if not(0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за диапазон ЦАП (0.00 - {dynamic_range:.2f} B)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)

def number_to_dac(number):
    binary_str = bin(number)[2:].zfill(8)
    binary_list = [int(bit) for bit  in binary_str]
    GPIO.output(leds, binary_list)
    print(f"Число на вход ЦАП: {number}, биты: {binary_list}")

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = Voltage_number(voltage)
            number_to_dac(number)
        except ValueError:
            print("Вы не ввели число. Попробуте еще рвз\n")
finally:
    GPIO.output(leds, 0)
    GPIO.cleanup()