import subprocess

class DeviceVolumeControlCrude:
    def get_system_volume(self) -> int:
        """
        Returns the current output volume (0–100).
        """
        cmd = ['osascript', '-e', 'output volume of (get volume settings)']
        out = subprocess.check_output(cmd, text=True).strip()
        return int(out)

    def set_system_volume(self, vol: int):
        """
        Sets the output volume to vol (0–100).
        """
        vol = max(0, min(100, vol))
        cmd = ['osascript', '-e', f'set volume output volume {vol}']
        subprocess.run(cmd, check=True)

    def mute_system(self):
        subprocess.run(['osascript', '-e', 'set volume output muted true'], check=True)

    def unmute_system(self):
        subprocess.run(['osascript', '-e', 'set volume output muted false'], check=True)

if __name__ == '__main__':
    vol = DeviceVolumeControlCrude()
    print("Current volume:", vol.get_volume())
    print("Setting volume to 30…")
    vol.set_system_volume(30)
    print("Muting…")
    vol.mute_system()
    print("Unmuted and set to 70 in 2 s…")
    import time; time.sleep(2)
    vol.unmute_system(); vol.set_system_volume(70)
