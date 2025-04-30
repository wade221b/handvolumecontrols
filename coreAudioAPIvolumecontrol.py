import ctypes
from ctypes import byref, c_uint32
import CoreAudio #todo : install CoreAudio and run this. 
# Check documentation https://developer.apple.com/documentation/coreaudio/building-an-audio-server-plug-in-and-driver-extension

# shorthand for the system object
kSystemObject = CoreAudio.kAudioObjectSystemObject

# get the AudioObjectPropertyAddress struct from PyObjC
AudioObjectPropertyAddress = CoreAudio.AudioObjectPropertyAddress

def _get_default_output_device() -> int:
    """
    Returns the AudioObjectID of the system's default output device.
    """
    # prepare an AudioObjectPropertyAddress for default output device
    addr = AudioObjectPropertyAddress(
        mSelector=CoreAudio.kAudioHardwarePropertyDefaultOutputDevice,
        mScope=CoreAudio.kAudioObjectPropertyScopeGlobal,
        mElement=CoreAudio.kAudioObjectPropertyElementMaster
    )

    device_id = c_uint32(0)
    size = c_uint32(ctypes.sizeof(device_id))
    # AudioObjectGetPropertyData(AudioObjectID inObjectID,
    #                            const AudioObjectPropertyAddress* inAddress,
    #                            UInt32 inQualifierDataSize,
    #                            const void* inQualifierData,
    #                            UInt32* ioDataSize,
    #                            void* outData) → OSStatus
    status = CoreAudio.AudioObjectGetPropertyData(
        kSystemObject, byref(addr), 0, None,
        byref(size), byref(device_id)
    )
    if status:
        raise OSError(f"AudioObjectGetPropertyData failed: {status}")
    return device_id.value

def set_output_mute(mute: bool):
    """
    Mutes (mute=True) or unmutes (mute=False) the default output device.
    """
    device_id = _get_default_output_device()

    addr = AudioObjectPropertyAddress(
        mSelector=CoreAudio.kAudioDevicePropertyMute,
        mScope=CoreAudio.kAudioObjectPropertyScopeOutput,
        mElement=CoreAudio.kAudioObjectPropertyElementMaster
    )

    val = c_uint32(1 if mute else 0)
    size = c_uint32(ctypes.sizeof(val))
    status = CoreAudio.AudioObjectSetPropertyData(
        device_id, byref(addr), 0, None,
        size, byref(val)
    )
    if status:
        raise OSError(f"AudioObjectSetPropertyData failed: {status}")

if __name__ == "__main__":
    # mute…
    # set_output_mute(True)
    print(_get_default_output_device())
    # …then unmute a couple seconds later
    # import time; time.sleep(2)
    # set_output_mute(False)
