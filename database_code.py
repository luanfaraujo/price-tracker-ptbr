import requests
import re
import sqlite3
from datetime import date
import logging

logging.basicConfig(
    filename='price_tracker_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

logging.info("Script started")

current_date = date.today()
successful_scrapes = 0

kabum_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

ml_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def kabum_scrape(url):
    try:
        response = requests.get(url, headers=kabum_headers)
        logging.info(f"Fetched {url} - Status: {response.status_code}")

        if response.status_code == 200:
            con = sqlite3.connect("price_tracker_v2.db")
            cur = con.cursor()
            cur.execute('SELECT id FROM products WHERE product_url = ?', (url,))
            result = cur.fetchone()

            if result:
                product_id = result[0]

            else:
                name_pattern = r'"name":\s*"([^"]+)"'
                name_match = re.search(name_pattern, response.text)

                if name_match:
                    product_name = name_match.group(1)

                    cur.execute('''
                    INSERT INTO products (product_name, product_url, retailer_name)
                    VALUES (?, ?, ?)
                ''', (product_name, url, "Kabum"))
                    product_id = cur.lastrowid

            # Search for the price JSON in the HTML
            price_pattern = r'"prices":\{"oldPrice":([\d.]+),"priceWithDiscount":([\d.]+),"price":([\d.]+),"discountPercentage":(\d+)\}'
            price_match = re.search(price_pattern, response.text)

            if price_match:
                orig_price = float(price_match.group(1))
                cash_price = float(price_match.group(2))
                installments_price = float(price_match.group(3))

                # Fix problem of orig_price = 0 if no discount
                if orig_price == 0.0:
                    orig_price = installments_price

                else:
                    pass

                cur.execute('''
                    INSERT INTO price_history (product_id, date_recorded, original_price, installments_total_price, cash_total_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (product_id, current_date, orig_price, installments_price, cash_price))
                con.commit()

                global successful_scrapes
                successful_scrapes += 1
                logging.info(f"Successfully saved price: R${cash_price}")

            else:
                logging.warning(f"Price pattern NOT FOUND for {url}")

        else:
            logging.error(f"FAILED to access {url} - Status: {response.status_code}")

    except Exception as e:
        logging.error(f"ERROR processing {url}: {e}")

def ml_scrape(url):
    try:
        response = requests.get(url, headers=ml_headers)
        logging.info(f"Fetched {url} - Status: {response.status_code}")

        if response.status_code == 200:
            con = sqlite3.connect("price_tracker_v2.db")  # DO NOT CHANGE
            cur = con.cursor()
            cur.execute('SELECT id FROM products WHERE product_url = ?', (url,))
            result = cur.fetchone()

            if result:
                product_id = result[0]

            else:
                name_pattern = r'"title":"([^"]+)"'
                name_match = re.search(name_pattern, response.text)

                if name_match:
                    product_name = name_match.group(1)

                    cur.execute('''
                    INSERT INTO products (product_name, product_url, retailer_name)
                    VALUES (?, ?, ?)
                ''', (product_name, url, "Kabum"))
                    product_id = cur.lastrowid

            # Search for the price JSON in the HTML
            cash_price_pattern = r'"type":"price","value":([\d.]+)'
            cash_price_match = re.search(cash_price_pattern, response.text)

            installments_price_pattern = r'"installments_total":([\d.]+)'
            installments_price_match = re.search(installments_price_pattern, response.text)

            if cash_price_match and installments_price_match:
                orig_price = None
                cash_price = float(cash_price_match.group(1))
                installments_price = float(installments_price_match.group(1))

                cur.execute('''
                    INSERT INTO price_history (product_id, date_recorded, original_price, installments_total_price, cash_total_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (product_id, current_date, orig_price, installments_price, cash_price))
                con.commit()

                global successful_scrapes
                successful_scrapes += 1
                logging.info(f"Successfully saved price: R${cash_price}")

            else:
                logging.warning(f"Price pattern NOT FOUND for {url}")

        else:
            logging.error(f"FAILED to access {url} - Status: {response.status_code}")

    except Exception as e:
        logging.error(f"ERROR processing {url}: {e}")

url_list = ("https://www.kabum.com.br/produto/662405/processador-amd-ryzen-7-9800x3d-cache-8mb-8-nucleos-16-threads-am5-100-100001084wof",
            "https://www.kabum.com.br/produto/620992/monitor-gamer-lg-ultragear-27-fhd-180hz-1ms-ips-dp-e-hdmi-hdr10-freesync-g-sync-27gs60f-b",
            "https://www.kabum.com.br/produto/714574/placa-de-video-gigabyte-rtx-5070-windforce-oc-sff-12g-nvidia-geforce-12gb-gddr7-192bits-dlss-ray-tracing-9vn5070wo-00-g10",
            "https://www.kabum.com.br/produto/497573/processador-intel-core-i9-14900k-14-geracao-6ghz-max-turbo-cache-36mb-24-nucleos-32-threads-lga1700-bx8071514900k",
            "https://www.kabum.com.br/produto/103431/webcam-full-hd-logitech-c920s-com-microfone-embutido-protecao-de-privacidade-widescreen-1080p-compativel-logitech-capture-960-001257",
            "https://www.kabum.com.br/produto/405437/monitor-gamer-samsung-odyssey-g3-24-fhd-144hz-1ms-va-freesync-premium-altura-ajustavel-ls24bg300elmzd",
            "https://www.mercadolivre.com.br/watercooler-deepcool-le360-v2-argb-360mm-branco--rle360wh/up/MLBU3333522829",
            "https://www.mercadolivre.com.br/gamesir-g7-se-preto-unidade-1/p/MLB52135607?product_trigger_id=MLB41147255&pdp_filters=official_store%3A210282&applied_product_filters=MLB41147255&picker=true&quantity=1",
            "https://www.kabum.com.br/produto/472908/monitor-gamer-curvo-lg-ultragear-34-wqhd-ultrawide-160hz-1ms-freesync-premium-hdr10-som-integrado-34gp63a-b")

logging.info(f"Processing {len(url_list)} URLs")

for url in url_list:
    if "kabum.com" in url:
        kabum_scrape(url)
    elif "mercadolivre.com" in url:
        ml_scrape(url)
    else:
        logging.error(f"ERROR - URL NOT SUPPORTED: {url}")

logging.info(f"Script completed. Successfully scraped {successful_scrapes}/{len(url_list)} products")