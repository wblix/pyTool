# Keylogger and Screenlogger

## Overview

This repository contains two Python scripts: a Keylogger and a Screenlogger. The Keylogger captures keyboard input and logs it to a file, while the Screenlogger captures periodic screenshots and sends them to a specified webhook URL.

## Keylogger

### Description

The Keylogger captures keyboard input and logs the keystrokes along with the active window title to a temporary file. The log file is periodically sent to a specified webhook URL.

### Installation

1. Install the required libraries:
   ```bash
   pip install keyboard requests pygetwindow
