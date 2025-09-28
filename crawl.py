# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import re
# import json
# import os

# # File chứa URL và class
# urls_file = "urls.txt"
# # File lưu dữ liệu
# output_file = "products.json"

# # Đọc file JSON cũ (nếu có)
# if os.path.exists(output_file):
#     with open(output_file, "r", encoding="utf-8") as f:
#         products = json.load(f)
# else:
#     products = []

# # Lấy danh sách URL đã crawl rồi
# crawled_urls = {p["url"] for p in products}
# p_classes = {p["class"] for p in products}

# # Cấu hình Chrome
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# # bach hoa xanh
# def crawl_(line, name_="div.sticky h1", price_="div.text-red-price", desc_="div.detail-style", image_="div.swiper-slide.swiper-slide-active img"):
#     parts = line.strip().split(" ", 1)
#     if len(parts) != 2:
#         return  # bỏ qua dòng sai định dạng
#     url, product_class = parts

#     if product_class in p_classes:
#         print(f"⏩ Bỏ qua {url} (đã crawl)")
#         return
#     # if url in crawled_urls:
#     #     print(f"⏩ Bỏ qua {url} (đã crawl)")
#     #     return

#     driver.get(url)
#     time.sleep(3)
#     # Crawl dữ liệu
#     try:
#         try:
#             name = driver.find_element(By.CSS_SELECTOR, name_).text.strip()
#         except:
#             name = "Name"

#         # --- price ---
#         try:
#             price_text = driver.find_element(By.CSS_SELECTOR, price_).text.strip()
#             price = int(re.sub(r"\D", "", price_text))
#         except:
#             price = 0  # hoặc 0

#         # --- description ---
#         try:
#             description = driver.find_element(By.CSS_SELECTOR, desc_).get_attribute("innerHTML")
#         except:
#             description = "Test"

#         # --- image ---
#         try:
#             image_tag = driver.find_element(By.CSS_SELECTOR, image_)
#             image_path = image_tag.get_attribute("src") if image_tag else None
#         except:
#             image_path = "null"

#         product_data = {
#             "url": url,
#             "class": product_class,   # thêm trường class
#             "name": name,
#             "price": price,
#             "description": description,
#             "image_path": image_path,
#             "size": ""
#         }

#         products.append(product_data)
#         crawled_urls.add(url)

#         # Ghi lại vào file JSON
#         with open(output_file, "w", encoding="utf-8") as out:
#             json.dump(products, out, ensure_ascii=False, indent=4)

#         print(f"✅ Đã crawl: {url}")

#     except Exception as e:
#         print(f"❌ Lỗi khi crawl {url}: {e}")


# try:
#     with open(urls_file, "r", encoding="utf-8") as f:
#         for line in f:
#             if "bachhoaxanh" in line:
#                 crawl_(line)
#             elif "concung" in line:
#                 crawl_(line, "h1.product-name", "span.product-price", "div.content-product.position-relative", "img.image-zoom")
#             elif "muathongminh" in line:
#                 crawl_(line, "h1.product-name a.cursor-text", "p.price-current", "div#product-description-section", "img.w-full.aspect-h1-w1.object-contain")
#             elif "bachhoa.extra.vn" in line:
#                 crawl_(line, "h1", "span.special-price span", "div#tab-content", "li.carousel__slide img.lazyloaded")
#             elif "nhathuocminhchau" in line:
#                 crawl_(line, "div.title.h3", "div.gia.h5", "div#chitiet", "div.owl-item.active img")
#             elif "www.lazada.vn" in line:
#                 crawl_(line, "h1.pdp-mod-product-badge-title-v2", "span.pdp-v2-product-price-content-salePrice-amount", "div.pdp-product-detail-v2", "img.pdp-mod-common-image.gallery-preview-panel-v2__image")
#             elif "lottemart" in line:
#                 crawl_(line, "h2.field-name", "div.field-price", "div#desc", "div.field-img img")
#             elif "doxaco.com.vn" in line:
#                 crawl_(line, "div.product-heading", "span.pro-price", "div#nav-desc", "a.product-gallery__item img")
#             elif "www.guardian.com.vn" in line:
#                 crawl_(line, "h1.page-title span.base", "span.price-container span.price", "div#description", "img.fotorama__img")
#             elif "tiki.vn" in line:
#                 crawl_(line, "h1", "div.product-price__current-price", "h1", "div.image-frame img")
#             elif "bachhoathai.vn" in line:
#                 crawl_(line, "h1.text-strong", "span.text-red", "div.padding-30._tablet-padding-20.cf", "div.swiper-slide img")
#             elif "chiaki.vn" in line:
#                 crawl_(line, "span#js-product-title", "span#price-show", "div.product-contentbox.detail-component-item", "img.product-img-main")
#             else :
#                 print("có 1 link không hợp lệ: " + line)
#     # crawl_("https://concung.com/gel-condom/bao-cao-su-durex-invisible-hop-3-goi-41359.html hello", "h1.product-name", "span.product-price", "div.content-product.position-relative", "img.image-zoom")
# finally:
#     driver.quit()



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import json
import os

# File dữ liệu đã sync
input_file = "products_synced.json"
output_file = "products_fixed.json"

# Đọc dữ liệu JSON
if os.path.exists(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        products = json.load(f)
else:
    print("❌ Không tìm thấy file products_synced.json")
    exit()

# --- Cấu hình Chrome ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def recrawl(product, name_="div.sticky h1", price_="div.text-red-price",
            desc_="div.detail-style", image_="div.swiper-slide.swiper-slide-active img"):
    """Hàm crawl lại dữ liệu cho 1 sản phẩm"""
    url = product["url"]
    driver.get(url)
    time.sleep(3)

    try:
        try:
            name = driver.find_element(By.CSS_SELECTOR, name_).text.strip()
        except:
            name = product.get("name", "Name")
            print("loi crawl name at: " + product["url"])

        # --- price ---
        try:
            price_text = driver.find_element(By.CSS_SELECTOR, price_).text.strip()
            price = int(re.sub(r"\D", "", price_text))
        except:
            price = product.get("price", 0)
            print("loi crawl price at: " + product["url"])

        # --- description ---
        try:
            description = driver.find_element(By.CSS_SELECTOR, desc_).get_attribute("innerHTML")
        except:
            description = product.get("description", "")
            print("loi crawl desc at: " + product["url"])

        # --- image ---
        try:
            image_tag = driver.find_element(By.CSS_SELECTOR, image_)

            image_path = (image_tag.get_attribute("src") if image_tag.get_attribute("src") else image_tag.get_attribute("srcset")) if image_tag else product.get("image_path", "")
        except:
            image_path = product.get("image_path", "")
            print("loi crawl image_path at: " + product["url"])

        # cập nhật dữ liệu
        product.update({
            "name": name,
            "price": price,
            "description": description,
            "image_path": image_path
        })

        print(f"✅ Đã recrawl: {url}")

    except Exception as e:
        print(f"❌ Lỗi recrawl {url}: {e}")


# --- Áp dụng cho từng sản phẩm ---
try:
    for p in products:
        if p.get("price", 0) == 45000 or not p.get("image_path") or p.get("image_path") == "null":
            print(f"⚠️ Dữ liệu lỗi -> recrawl: {p['url']}")
            # chọn rule crawl dựa trên domain
            url = p["url"]
            if "concung" in url:
                recrawl(p, "h1.product-name", "span.product-price",
                        "div.content-product.position-relative", "img.image-zoom")
            elif "muathongminh" in url:
                recrawl(p, "h1.product-name a.cursor-text", "p.price-current",
                        "div#product-description-section", "img.w-full.aspect-h1-w1.object-contain")
            elif "bachhoa.extra.vn" in url:
                recrawl(p, "h1", "span.special-price span", "div#tab-content",
                        "li.carousel__slide img.lazyloaded")
            elif "nhathuocminhchau" in url:
                recrawl(p, "div.title.h3", "div.gia.h5", "div#chitiet", "div.owl-item.active img")
            elif "www.lazada.vn" in url:
                recrawl(p, "h1.pdp-mod-product-badge-title-v2",
                        "span.pdp-v2-product-price-content-salePrice-amount",
                        "div.pdp-product-detail-v2",
                        "img.pdp-mod-common-image.gallery-preview-panel-v2__image")
            elif "lottemart" in url:
                recrawl(p, "h2.field-name", "div.field-price", "div#desc", "div.field-img img")
            elif "doxaco.com.vn" in url:
                recrawl(p, "div.product-heading", "span.pro-price", "div#nav-desc",
                        "a.product-gallery__item img")
            elif "www.guardian.com.vn" in url:
                recrawl(p, "h1.page-title", "span.price",
                        "div.data-content-inner", "img.fotorama__img")
            elif "tiki.vn" in url:
                recrawl(p, "h1", "div.product-price__current-price", "h1", "div.image-frame img")
            elif "bachhoathai.vn" in url:
                recrawl(p, "h1.text-strong", "span.text-red",
                        "div.padding-30._tablet-padding-20.cf", "div.swiper-slide img")
            elif "chiaki.vn" in url:
                recrawl(p, "span#js-product-title", "span#price-show",
                        "div.product-contentbox.detail-component-item", "img.product-img-main")
            else:
                recrawl(p)  # mặc định cho bachhoaxanh
finally:
    driver.quit()

# --- Lưu lại file JSON đã fix ---
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(products, out, ensure_ascii=False, indent=4)

print(f"💾 Đã lưu file {output_file}")
