import sys
import subprocess
import importlib.util
import os

# --- AUTO-INSTALL DEPENDENCIES ---
def install_if_missing(package):
    if importlib.util.find_spec(package) is None:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_if_missing('PyQt6')
install_if_missing('psutil')

import psutil
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QComboBox, QPushButton, QTextEdit, QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt, QTimer

class VirtualRamDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Virtual RAM Downloader Pro')
        self.setFixedSize(550, 620)
        self.setStyleSheet("background-color: #0d0d0d; color: #00d4ff;")
        
        layout = QVBoxLayout()
        
        # System Telemetry
        self.stats_label = QLabel(self.get_system_stats())
        self.stats_label.setStyleSheet("font-family: 'Consolas'; color: #ffcc00; padding: 10px; border: 1px solid #333; margin-bottom: 10px;")
        layout.addWidget(self.stats_label)

        # Action 1: Force Clean
        layout.addWidget(QLabel("PHASE 1: KERNEL PREPARATION"))
        self.btn_clean = QPushButton("FORCE CLEAN (Purge Registry & PageFile)")
        self.btn_clean.setStyleSheet("""
            QPushButton { background-color: #c0392b; color: white; font-weight: bold; padding: 12px; border-radius: 4px; }
            QPushButton:hover { background-color: #e74c3c; }
        """)
        self.btn_clean.clicked.connect(self.run_force_clean)
        layout.addWidget(self.btn_clean)

        # Action 2: Expansion
        layout.addWidget(QLabel("PHASE 2: CAPACITY ALLOCATION"))
        self.ram_options = {
            "4GB": 4096, "8GB": 8192, "16GB": 16384, 
            "32GB": 32768, "64GB": 65536, "96GB": 98304, "128GB": 131072
        }
        self.combo = QComboBox()
        self.combo.addItems(self.ram_options.keys())
        self.combo.setStyleSheet("background-color: #1a1a1a; border: 1px solid #00d4ff; padding: 5px; color: white;")
        layout.addWidget(self.combo)

        self.btn_allocate = QPushButton("EXPAND VIRTUAL RAM")
        self.btn_allocate.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: white; font-weight: bold; padding: 12px; border-radius: 4px; }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        self.btn_allocate.clicked.connect(self.run_expansion)
        layout.addWidget(self.btn_allocate)

        # Status & Logs
        self.pbar = QProgressBar()
        self.pbar.setStyleSheet("QProgressBar { border: 1px solid #00d4ff; text-align: center; } QProgressBar::chunk { background-color: #00d4ff; }")
        layout.addWidget(self.pbar)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("background-color: #000; color: #00ff41; font-family: 'Consolas'; font-size: 10px;")
        layout.addWidget(self.log)

        self.setLayout(layout)

    def get_system_stats(self):
        phys = round(psutil.virtual_memory().total / (1024**3), 2)
        disk = round(psutil.disk_usage('C:').free / (1024**3), 2)
        return f"PHYSICAL RAM: {phys} GB | DISK AVAILABLE: {disk} GB"

    def log_msg(self, text):
        self.log.append(f"[V-RAM-PRO]> {text}")

    def run_ps_cmd(self, command):
        return subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)

    def run_force_clean(self):
        self.log_msg("INITIATING SECTOR PURGE...")
        # Step A: Disable Windows Auto-Management
        self.run_ps_cmd("Set-CimInstance -Query 'Select * from Win32_ComputerSystem' -Property @{AutomaticManagedPagefile=$False}")
        # Step B: Remove existing pagefile registration
        result = self.run_ps_cmd("Get-CimInstance Win32_PageFileSetting | Remove-CimInstance")
        
        if result.returncode == 0:
            self.log_msg("SUCCESS: System Managed PageFile has been decoupled.")
            QMessageBox.information(self, "Phase 1 Complete", "Force Clean Successful. Proceed to Expansion.")
        else:
            self.log_msg(f"ERROR: {result.stderr}")

    def run_expansion(self):
        selected_mb = self.ram_options[self.combo.currentText()]
        req_gb = selected_mb / 1024
        free_gb = psutil.disk_usage('C:').free / (1024**3)

        if req_gb > free_gb:
            QMessageBox.critical(self, "Space Warning", f"Required: {req_gb}GB | Found: {free_gb:.2f}GB. Clear disk space first.")
            return

        self.log_msg(f"MAPPING {selected_mb}MB VIRTUAL BRIDGE...")
        create_ps = f"New-CimInstance -ClassName Win32_PageFileSetting -Property @{{Name='C:\\pagefile.sys'; InitialSize={selected_mb}; MaximumSize={selected_mb}}}"
        result = self.run_ps_cmd(create_ps)

        if result.returncode == 0:
            self.log_msg("SUCCESS: Virtual Address Space reserved.")
            self.pbar.setValue(100)
            self.finalize_reboot()
        else:
            self.log_msg("ERROR: Phase 1 bypass required or Access Denied (Run as Admin).")

    def finalize_reboot(self):
        reply = QMessageBox.question(self, 'Virtual RAM Downloader Pro', 
                                    "System update successful. Reboot is required to initialize the new memory pool.\n\nRestart now?", 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            os.system("shutdown /r /t 1")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VirtualRamDownloader()
    window.show()
    sys.exit(app.exec())