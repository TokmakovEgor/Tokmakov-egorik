import r2r_adc as current_adc
import adc_plot as ap
import time


adc = None
voltage_values = []
time_values = []
duration = 5.0
max_voltage = 3.5

try:
    adc = current_adc.R2R_ADC(dynamic_range = 3.3, compare_time=0.0001)
    start_time = time.time()

    while (time.time() - start_time) < duration:
        current_time = time.time() - start_time
        voltage = adc.get_sc_voltage()
        voltage_values.append(voltage)
        time_values.append(current_time)

    ap.plot_voltage_vs_time(time_values, voltage_values, max_voltage)
    ap.plot_sampling_period_hist(time_values)

finally:
    if adc is not None:
        adc.deinit()