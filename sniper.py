import whois
import os
import time
import socket
import re
import csv
from datetime import datetime, timedelta
from collections import Counter
import requests
import dns.resolver

def clear():
    os.system("clear")

def banner():
    print("""
===========================================
   🔥 Domain Sniper Bot v1.4
   📱 Made by: radom duded
   💻 GitHub: github.com/YOUR_GITHUB
   ⚠️ Disclaimer: For educational/research use only.
===========================================
""")

def menu():
    print("📜 MENU")
    print("1️⃣  Run Domain Scan")
    print("2️⃣  Exit")
    print("3️⃣  Expand keywords with extra suffixes/prefixes (e.g. 'get', 'official')")

def is_valid_keyword(word):
    return len(word) >= 3 and re.match(r'^[A-Za-z0-9\-]+$', word)

def log_error(error_dir, domain, error_type, error, code=None, retry=None):
    nowstr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fname = (f"{code}_" if code else "") + f"{error_type.lower()}_error.txt"
    log_file = os.path.join(error_dir, fname)
    retry_str = f" (retry {retry})" if retry else ""
    with open(log_file, "a") as f:
        f.write(f"[{nowstr}] {domain}{retry_str} — {error}\n")

def log_retry(error_dir, domain, error_type, attempt):
    nowstr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = f"{error_type.lower()}_retries.txt"
    log_file = os.path.join(error_dir, file_name)
    with open(log_file, "a") as f:
        f.write(f"[{nowstr}] {domain} — retry {attempt}\n")

def load_keywords(filepath):
    if not os.path.exists(filepath):
        print(f"\033[91m❌ File '{filepath}' not found.\033[0m")
        return []
    with open(filepath, 'r') as f:
        words = [line.strip() for line in f if line.strip()]
        filtered = [w for w in words if is_valid_keyword(w)]
        print(f"\033[96mLoaded {len(filtered)} keywords ({len(words) - len(filtered)} filtered).\033[0m")
        return filtered

def save_keywords(filepath, keywords):
    with open(filepath, 'w') as f:
        for word in keywords:
            f.write(word+'\n')

def expand_keywords():
    download_path = "/storage/emulated/0/Download/"
    result_dir = os.path.join(download_path, "DomainSniper")
    os.makedirs(result_dir, exist_ok=True)

    txt_files = [f for f in os.listdir(download_path) if f.endswith(".txt")]

    if not txt_files:
        print("\033[91m⚠️ No .txt files found in Downloads.\033[0m")
        return

    print("\n\033[96m📁 TXT files in your Downloads:\033[0m")
    for idx, name in enumerate(txt_files):
        print(f"\033[94m{idx + 1}. {name}\033[0m")
    choice = input("\033[96m🔢 Enter the number of the file to expand: \033[0m")
    try:
        selected_file = txt_files[int(choice) - 1]
    except:
        print("\033[91m❌ Invalid choice.\033[0m")
        return

    keyword_path = os.path.join(download_path, selected_file)
    keywords = [w for w in load_keywords(keyword_path) if is_valid_keyword(w)]

    prefixes = ["get", "official", "the", "my", "go"]
    suffixes = ["app", "hq", "online", "store", "official"]

    expanded = set(keywords)
    for word in keywords:
        for p in prefixes:
            expanded.add(p + word)
        for s in suffixes:
            expanded.add(word + s)
        for p in prefixes:
            for s in suffixes:
                expanded.add(p + word + s)
    expanded = sorted(expanded)

    save_path = os.path.join(result_dir, f"expanded_{selected_file}")
    save_keywords(save_path, expanded)
    print(f"\033[92m✅ Expanded keywords saved to {save_path}\033[0m")

def whois_check(domain, error_dir=None, retries=2, error_counter=None):
    last_exc = None
    for attempt in range(1, retries+1):
        try:
            w = whois.whois(domain)
            return not w.domain_name
        except Exception as e:
            last_exc = e
            if error_dir:
                log_error(error_dir, domain, "WHOIS", str(e), retry=attempt)
                log_retry(error_dir, domain, "WHOIS", attempt)
            if error_counter is not None:
                error_counter['WHOIS'] += 1
            time.sleep(0.5)
    return False

def dns_check(domain, error_dir=None, retries=2, error_counter=None):
    last_exc = None
    for attempt in range(1, retries+1):
        try:
            socket.gethostbyname(domain)
            return True
        except socket.gaierror as e:
            last_exc = e
            if error_dir:
                log_error(error_dir, domain, "DNS", str(e), code="gaierror", retry=attempt)
                log_retry(error_dir, domain, "DNS", attempt)
            if error_counter is not None:
                error_counter['DNS'] += 1
            time.sleep(0.5)
        except Exception as e:
            last_exc = e
            if error_dir:
                log_error(error_dir, domain, "DNS", str(e), retry=attempt)
                log_retry(error_dir, domain, "DNS", attempt)
            if error_counter is not None:
                error_counter['DNS'] += 1
            time.sleep(0.5)
    return False

def http_check(domain, error_dir=None, error_counter=None, retries=2, delay=0.5):
    urls = [f"http://{domain}", f"https://{domain}"]
    for url in urls:
        for attempt in range(1, retries+1):
            try:
                response = requests.head(url, allow_redirects=True, timeout=4)
                return True, response.status_code
            except requests.RequestException as e:
                if error_dir:
                    log_error(error_dir, domain, "HTTP", str(e), retry=attempt)
                if error_counter is not None:
                    error_counter['HTTP'] += 1
                time.sleep(delay)
    return False, None

def advanced_dns_check(domain, error_dir=None, error_counter=None):
    record_types = ['NS', 'MX', 'TXT', 'SOA']
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype, lifetime=3)
            if answers:
                return True, rtype
        except Exception as e:
            if error_dir:
                log_error(error_dir, domain, f"DNS_{rtype}", str(e))
            if error_counter is not None:
                error_counter[f"DNS_{rtype}"] += 1
            continue
    return False, None

def format_time(seconds):
    return str(timedelta(seconds=int(seconds)))

def rotate_logs(result_dir, retention_days=7):
    now = time.time()
    for fname in os.listdir(result_dir):
        if fname.endswith("_error.txt") or fname.endswith("_retries.txt"):
            fullpath = os.path.join(result_dir, fname)
            if os.stat(fullpath).st_mtime < now - retention_days * 86400:
                os.remove(fullpath)
                print(f"\033[90m🧹 Deleted old log: {fname}\033[0m")

def run_sniper():
    download_path = "/storage/emulated/0/Download/"
    result_dir = os.path.join(download_path, "DomainSniper")
    os.makedirs(result_dir, exist_ok=True)
    rotate_logs(result_dir, 7)

    txt_files = [f for f in os.listdir(download_path) if f.endswith(".txt")]

    if not txt_files:
        print("\033[91m⚠️ No .txt files found in Downloads.\033[0m")
        return

    print("\n\033[96m📁 TXT files in your Downloads:\033[0m")
    for idx, name in enumerate(txt_files):
        print(f"\033[94m{idx + 1}. {name}\033[0m")

    choice = input("\033[96m🔢 Enter the number of the file to use: \033[0m")
    try:
        selected_file = txt_files[int(choice) - 1]
    except:
        print("\033[91m❌ Invalid choice.\033[0m")
        return

    keyword_path = os.path.join(download_path, selected_file)
    keywords = [w for w in load_keywords(keyword_path) if is_valid_keyword(w)]

    trending_tlds = [
        '.com', '.xyz', '.io', '.app', '.eth', '.sol', '.art', '.tech', '.store', '.site', 
        '.club', '.dev', '.link', '.design'
    ]
    print(f"\n\033[96m🌐 Default TLDs: {', '.join(trending_tlds)}\033[0m")
    tlds_input = input("\033[96mEnter comma-separated TLDs or press Enter to use default: \033[0m").strip()
    if tlds_input:
        tlds = [tld.strip() if tld.strip().startswith('.') else '.' + tld.strip() for tld in tlds_input.split(',')]
    else:
        tlds = trending_tlds

    delay = input("\033[96m⏳ Delay between checks (seconds, default 2): \033[0m").strip()
    try:
        delay = float(delay)
    except:
        delay = 2

    available = []
    failed = []
    checked = 0
    total_domains = len(keywords) * len(tlds)
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    result_path = os.path.join(result_dir, f'available_{timestamp}.txt')
    csv_path = os.path.join(result_dir, f'available_{timestamp}.csv')
    error_domains = []
    error_counter = Counter()

    print("\n\033[96m🔍 Scanning domains...\033[0m\n")
    try:
        for word in keywords:
            for tld in tlds:
                domain = word + tld
                checked += 1
                now = datetime.now().strftime("%H:%M:%S")
                try:
                    whois_free = whois_check(domain, error_dir=result_dir, error_counter=error_counter)
                    dns_taken = http_taken = advdns_taken = False
                    http_status = None
                    advdns_type = None

                    if whois_free:
                        dns_taken = dns_check(domain, error_dir=result_dir, error_counter=error_counter)
                        http_taken, http_status = http_check(domain, error_dir=result_dir, error_counter=error_counter)
                        advdns_taken, advdns_type = advanced_dns_check(domain, error_dir=result_dir, error_counter=error_counter)

                        if dns_taken or http_taken or advdns_taken:
                            status = "⚠️ Error"
                            color = "\033[93m"
                            failed.append(domain)
                            error_domains.append(domain)
                        else:
                            status = "✓ Available"
                            color = "\033[92m"
                            available.append(domain)
                    else:
                        status = "✗ Taken"
                        color = "\033[91m"
                        failed.append(domain)

                    domain_summary = (
                        f"{color}[{now}] {domain} — "
                        f"WHOIS free: {whois_free}, "
                        f"DNS: {dns_taken}, "
                        f"HTTP: {http_taken}{f' ({http_status})' if http_taken else ''}, "
                        f"AdvDNS: {advdns_taken}{f' ({advdns_type})' if advdns_taken else ''}\033[0m"
                    )
                    print(domain_summary)
                except Exception as e:
                    status = "⚠️ Error"
                    color = "\033[93m"
                    log_error(result_dir, domain, "GENERAL", str(e))
                    failed.append(domain)
                    error_domains.append(domain)

                remaining = total_domains - checked
                elapsed = time.time() - start_time
                avg_time = elapsed / checked if checked else 0
                eta = avg_time * remaining

                # Colored progress info
                print(f"\033[95mProgress: {checked}/{total_domains} checked, {remaining} remaining.\033[0m")
                print(f"\033[94mTime elapsed: {format_time(elapsed)} | Est. time left: {format_time(eta)}\033[0m\n")
                time.sleep(delay)

    except KeyboardInterrupt:
        print("\n\033[91m🛑 Scan stopped by user.\033[0m")

    # Write TXT results
    with open(result_path, 'w') as out:
        out.write(f"# Domain Sniper Results ({timestamp})\n")
        out.write(f"Total checked: {checked}\n")
        out.write(f"Available: {len(available)}\n")
        out.write(f"Failed: {len(failed)}\n")
        out.write(f"Duration: {format_time(time.time() - start_time)}\n\n")
        out.write("✓ Available domains:\n")
        for domain in available:
            out.write(domain + '\n')
        if failed:
            out.write("\n✗ Failed/Errors:\n")
            for domain in error_domains:
                out.write(domain + '\n')
        # Write error summary at the end
        out.write("\nError Summary:\n")
        for k, v in error_counter.items():
            out.write(f"  {k} errors: {v}\n")

    # Write CSV results
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['domain', 'status', 'checked_at'])
        for domain in available:
            writer.writerow([domain, 'Available', timestamp])
        for domain in failed:
            writer.writerow([domain, 'Failed', timestamp])

    print(f"\n\033[92m📦 Results saved to: {result_path}\033[0m")
    print(f"\033[96m📦 CSV saved to: {csv_path}\033[0m")
    print(f"\033[92m🎯 {len(available)} domains found available.\033[0m")
    print(f"\033[91m✗ {len(failed)} domains failed or taken.\033[0m")
    print(f"\033[96m⏱️ Total time: {format_time(time.time() - start_time)}\033[0m\n")

    # Print error summary
    if error_counter:
        print("\033[95mError Summary:\033[0m")
        for k, v in error_counter.items():
            print(f"  \033[93m{k} errors: {v}\033[0m")

def main():
    clear()
    banner()
    while True:
        menu()
        choice = input("\033[93mSelect an option: \033[0m")
        if choice == "1":
            run_sniper()
            input("\033[94m\n🔁 Press Enter to return to the menu...\033[0m")
            clear()
            banner()
        elif choice == "2":
            print("\033[92m👋 Exiting... Stay sharp, sniper.\033[0m")
            break
        elif choice == "3":
            expand_keywords()
            input("\033[94m\n🔁 Press Enter to return to the menu...\033[0m")
            clear()
            banner()
        else:
            print("\033[91m❌ Invalid selection. Try again.\033[0m")

if __name__ == "__main__":
    main()