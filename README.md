# Wendigo

Wendigo is an extensible malware/botnet framework using GitHub for C2. It downloads a configuation file from GitHub and then reads the modules to run in separate threads. If a module isn't present in memory it downloads it from GitHub. The framework is lightweight and unassuming, with all potentially suspicious code only running in memory after being securely downloaded.
