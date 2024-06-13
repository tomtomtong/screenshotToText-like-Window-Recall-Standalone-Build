import sys

def timestamp_to_human_readable(timestamp):
    from datetime import datetime
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%Y-%m-%d_%H-%M-%S")

def get_active_window_title_osx():
    from AppKit import NSWorkspace
    active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    return active_app.localizedName()

def get_active_window_title_windows():
    import ctypes
    import ctypes.wintypes

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    hwnd = user32.GetForegroundWindow()
    pid = ctypes.wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    process_handle = kernel32.OpenProcess(0x0400 | 0x0010, False, pid.value)
    exe_name = (ctypes.c_char * 260)()
    kernel32.GetModuleBaseNameA(process_handle, None, exe_name, 260)
    kernel32.CloseHandle(process_handle)
    return exe_name.value.decode("utf-8")

def get_active_window_title_linux():
    import subprocess

    def get_window_property(prop):
        root = subprocess.run(['xprop', '-root', prop], capture_output=True, text=True).stdout.strip().split()[-1]
        return root

    def get_window_name(wid):
        window_name = subprocess.run(['xprop', '-id', wid, 'WM_NAME'], capture_output=True, text=True).stdout.strip().split('"', 1)[1][:-1]
        return window_name

    active_window_id = get_window_property('_NET_ACTIVE_WINDOW')
    return get_window_name(active_window_id)

def get_active_window_title():
    if sys.platform == "win32":
        return get_active_window_title_windows()
    elif sys.platform == "darwin":
        return get_active_window_title_osx()
    elif sys.platform.startswith("linux"):
        return get_active_window_title_linux()
    else:
        return "Unknown"
