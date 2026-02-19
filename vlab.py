# vlab.py
import os
import base64
from utils import fetcher, checker, renamer

CONFIGS_DIR = "configs"
MAX_VLESS = 5
MAX_SS = 5
MONTHLY_LIMIT_GB = 130  # лимит для публичных конфигов

os.makedirs(CONFIGS_DIR, exist_ok=True)

def main():
    print("🔹 Получение ссылок из utils.fetcher...")
    all_links = fetcher.get_links()
    all_links["vless"] = list(set(all_links["vless"]))
    all_links["ss"] = list(set(all_links["ss"]))

    # ==========================
    # Проверка доступности и лимит 5+5
    # ==========================
    final_links = []

    # 1️⃣ VLESS
    vless_working = []
    for link in all_links["vless"]:
        host, port = checker.extract_host_port(link)
        if checker.check_alive(host, port):
            vless_working.append(link)
        if len(vless_working) >= MAX_VLESS:
            break
    final_links.extend(vless_working)

    # 2️⃣ SS
    ss_working = []
    for link in all_links["ss"]:
        host, port = checker.extract_host_port(link)
        if checker.check_alive(host, port):
            ss_working.append(link)
        if len(ss_working) >= MAX_SS:
            break
    final_links.extend(ss_working)

    print(f"Итоговые рабочие ссылки для публикации: {len(final_links)}")

    # ==========================
    # Сохранение публичного config.txt с лимитом
    # ==========================
    header_lines = [
        "#Profile-title : vlab.vpn",
        "#profile-update-interval : 3",
        "#announce : рабочие конфиги не гарантируются",
        "#script https://raw.githubusercontent.com/Dalaka79/myheroparser/refs/heads/main/vlab.py"
        f"#limit {MONTHLY_LIMIT_GB}GB / месяц",
        f"#remaining {MONTHLY_LIMIT_GB}GB",
        ""
    ]

    # 1️⃣ Публичный config.txt
    config_txt_path = os.path.join(CONFIGS_DIR, "config.txt")
    with open(config_txt_path, "w", encoding="utf-8") as f:
        for line in header_lines:
            f.write(line + "\n")
        for link in final_links:
            name = renamer.get_config_name(link)
            f.write(f"# {name}\n{link}\n")

    # 2️⃣ Base64 версия
    text = "\n".join(header_lines) + "\n"
    for link in final_links:
        name = renamer.get_config_name(link)
        text += f"# {name}\n{link}\n"

    with open(os.path.join(CONFIGS_DIR, "config_base64.txt"), "w", encoding="utf-8") as f:
        f.write(base64.b64encode(text.encode()).decode())

    # 3️⃣ Приватный owner файл без лимита
    owner_links = all_links["vless"] + all_links["ss"]
    owner_path = os.path.join(CONFIGS_DIR, "config_owner.txt")
    with open(owner_path, "w", encoding="utf-8") as f:
        for link in owner_links:
            name = renamer.get_config_name(link)
            f.write(f"# {name}\n{link}\n")

    print(f"✅ Публичный лимит: {MONTHLY_LIMIT_GB}GB. Осталось: {MONTHLY_LIMIT_GB}GB")
    print("✅ Все файлы обновлены в configs/")

if __name__ == "__main__":
    main()
