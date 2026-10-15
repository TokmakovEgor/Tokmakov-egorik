import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.dynamic_range = dynamic_range
        self.pwm_frequency =pwm_frequency
        self.verbose = verbose
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial = 0)

        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)

    def deinit(self):
        GPIO.output(self.gpio_pin, 0)
        GPIO.cleanup(self.gpio_pin)
        self.pwm.stop()

    def set_number(self, number):
        if number < 0:
            number = 0
        elif number > 255:
            number = 255
        duty = number / 255 * 100.0
        self.pwm.ChangeDutyCycle(duty)
        if self.verbose:
            print(f"number: {number}, duty: {duty :.2f}%")

    def set_voltage(self, voltage):
        dynamic_range = 3.179
        if not(0.0 <= voltage <= self.dynamic_range):
            if self.verbose:
                print(f"Напряжение выходит за диапазон ЦАП (0.00 - {dynamic_range:.2f} B)")
                print("Устанавливаем 0.0 В")
            self.set_number(0)
            return
        number = int(voltage / self.dynamic_range * 255)
        self.set_number(number)


if __name__ == "__main__":
    dac =   PWM_DAC(12, 1000, 3.25, True)
    try:
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы не ввели число. Попробуте еще рвз\n")
    finally:
        dac.deinit()
