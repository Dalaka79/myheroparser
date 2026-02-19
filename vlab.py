# vlab.py
import os
import base64
from utils import fetcher, checker, renamer

# Папка для сохранения конфигов
CONFIGS_DIR = "configs"
MAX_VLESS = 5
MAX_SS = 5

os.makedirs(CONFIGS_DIR, exist_ok=True)

def main():
    print("🔹 Получение ссылок из utils.fetcher...")
    all_links = fetcher.get_links()  # возвращает {"vless": [...], "ss": [...]}

    # Контроль дубликатов
    all_links["vless"] = list(set(all_links["vless"]))
    all_links["ss"] = list(set(all_links["ss"]))

    print(f"VLESS найдено: {len(all_links['vless'])}")
    print(f"SS найдено: {len(all_links['ss'])}")

    # ==========================
    # Проверка доступности и лимит
    # ==========================
    final_links = []

    # 1️⃣ Сначала VLESS
    vless_working = []
    for link in all_links["vless"]:
        host, port = checker.extract_host_port(link)
        if checker.check_alive(host, port):
            vless_working.append(link)
        if len(vless_working) >= MAX_VLESS:
            break
    final_links.extend(vless_working)

    # 2️⃣ Потом SS
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
    # Сохранение файлов
    # ==========================
    # 1. Публичный config.txt
    with open(os.path.join(CONFIGS_DIR, "config.txt"), "w", encoding="utf-8") as f:
        for link in final_links:
            name = renamer.get_config_name(link)
            f.write(f"# {name}\n{link}\n")

    # 2. Base64 версия
    text = ""
    for link in final_links:
        name = renamer.get_config_name(link)
        text += f"# {name}\n{link}\n"
    with open(os.path.join(CONFIGS_DIR, "config_base64.txt"), "w", encoding="utf-8") as f:
        f.write(base64.b64encode(text.encode()).decode())

    # 3. Приватный для владельца — все ссылки
    owner_links = all_links["vless"] + all_links["ss"]
    with open(os.path.join(CONFIGS_DIR, "config_owner.txt"), "w", encoding="utf-8") as f:
        for link in owner_links:
            name = renamer.get_config_name(link)
            f.write(f"# {name}\n{link}\n")

    print("✅ Все файлы обновлены в configs/")

if __name__ == "__main__":
    main()
