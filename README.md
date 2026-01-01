# Virtual RAM Downloader Pro 🚀

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

**Virtual RAM Downloader Pro** is a professional-grade system utility that allows users to expand their addressable memory pool by reconfiguring the Windows Page File (Swap Space). Unlike the standard Windows GUI, this tool features a **Force Clean** routine to ensure your settings aren't ignored by the OS.



## 🛠 Features
- **Dual-Phase Execution:** Separate "Clean" and "Expand" phases for maximum reliability.
- **PowerShell Powered:** Uses modern CIM instances for compatibility with Windows 10 and 11.
- **Dynamic Telemetry:** Real-time display of physical RAM and available disk space.
- **Verbose Kernel Log:** Provides technical feedback on every system modification.

## 🚀 How to Use
1. **Download:** Grab the latest `.exe` from the [Releases](link-to-your-release) page.
2. **Phase 1:** Click **FORCE CLEAN**. This unlocks the system's memory management.
3. **Phase 2:** Select your desired RAM size and click **EXPAND VIRTUAL RAM**.
4. **Reboot:** Restart your PC to allow the Windows kernel to create the new `pagefile.sys`.

## 🖥️ Building from Source
If you prefer to run the Python script directly:
1. Ensure you have Python 3.8+ installed.
2. Install dependencies:
   ```bash
   pip install PyQt6 psutil
