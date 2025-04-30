import subprocess

def get_volume() -> int:
    """
    Returns the current output volume (0–100).
    """
    cmd = ['osascript', '-e', 'output volume of (get volume settings)']
    out = subprocess.check_output(cmd, text=True).strip()
    return int(out)

def set_volume(vol: int):
    """
    Sets the output volume to vol (0–100).
    """
    vol = max(0, min(100, vol))
    cmd = ['osascript', '-e', f'set volume output volume {vol}']
    subprocess.run(cmd, check=True)

def mute():
    subprocess.run(['osascript', '-e', 'set volume output muted true'], check=True)

def unmute():
    subprocess.run(['osascript', '-e', 'set volume output muted false'], check=True)

if __name__ == '__main__':
    print("Current volume:", get_volume())
    print("Setting volume to 30…")
    set_volume(30)
    print("Muting…")
    mute()
    print("Unmuted and set to 70 in 2 s…")
    import time; time.sleep(2)
    unmute(); set_volume(70)
