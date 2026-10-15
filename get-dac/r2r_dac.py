import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        binary_str = bin(number)[2:].zfill(8)
        binary_list = [int(bit) for bit in binary_str]
        GPIO.output(self.gpio_bits, binary_list)
        if self.verbose:
            print(f"Число на вход ЦАП: {number}, биты: {binary_list}")

    def set_voltage(self, voltage):
        dynamic_range = 3.183
        if not(0.0 <= voltage <= dynamic_range):
            if self.verbose:
                print(f"Напряжение выходит за диапазон ЦАП (0.00 - {dynamic_range:.2f} B)")
                print("Устанавливаем 0.0 В")
            self.set_number(0)
            return
        number = int(voltage / dynamic_range * 255)
        self.set_number(number)


if __name__ == "__main__":
    dac = None
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.300, True)
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы не ввели число. Попробуте еще рвз\n")
    finally:
        if dac is not None:
            dac.deinit()
