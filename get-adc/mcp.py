import mcp3021_driver as md
import adc_plot as ap
import time


adc = None
voltage_values = []
time_values = []
duration = 5.0
max_voltage = 3.5

try:
    adc = md.MCP3021(dynamic_range = 3.3, verbose=False)
    start_time = time.time()

    while (time.time() - start_time) < duration:
        current_time = time.time() - start_time
        voltage = adc.get_voltage()
        voltage_values.append(voltage)
        time_values.append(current_time)

    ap.plot_voltage_vs_time(time_values, voltage_values, max_voltage)
    ap.plot_sampling_period_hist(time_values)

finally:
    if adc is not None:
        adc.deinit()