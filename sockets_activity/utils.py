def read_cpu_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = f.read().strip()
        return str(int(temp) / 1000.0)
    except FileNotFoundError:
        return "Unknown"
    