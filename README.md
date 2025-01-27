# **Keylogger & Screenlogger**

## **Overview**

This repository contains two Python scripts: a **Keylogger** and a **Screenlogger**. The **Keylogger** tracks keyboard input and logs it along with the active window title. Meanwhile, the **Screenlogger** captures periodic screenshots of your screen and uploads them to a designated webhook URL. 

These tools can be useful for personal productivity tracking, system monitoring, or remote access use cases. However, it’s important to use them responsibly, respecting privacy and legal boundaries.

## **Keylogger**

### **Description**

The Keylogger script monitors keyboard activity and logs the captured keystrokes into a log file. It also tracks which window was active when each keystroke was registered. Every predefined period, the log file is sent to a specified webhook URL, allowing for secure and remote tracking.

### **Features**
- **Keystroke Logging:** Records every keystroke and identifies the active window.
- **Real-time Uploading:** Sends the log file periodically to a specified webhook URL.
- **Customizable Time Intervals:** Adjust the frequency of log file uploads.
- **Window Title Tracking:** Tracks which program is currently in focus while logging inputs.

### **Installation**

To get started with the Keylogger, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-repository/keylogger-screenlogger.git
   cd keylogger-screenlogger
