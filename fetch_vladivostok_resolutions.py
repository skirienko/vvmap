#!/usr/bin/env python3
"""
Скачивает постановления администрации Владивостока о наименовании улиц
и остановок с docs.cntd.ru, primorye-gov.ru, topovl.ru, vlc25.ru, base.garant.ru
и prim-pravo.ru. Рендерит JS через Playwright, PDF обрабатывает через pypdf.
Сохраняет в markdown-файлы: YYYYMMDD-NNNN.md
"""

import os
import re
import time
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

OUT_DIR = "documents"
DELAY = 1.5  # секунд между документами

# (дата, номер, [список URL — пробует по очереди])
DOCUMENTS = [
    # --- 1994–2001 ---
    ("19960408", "452", [
        "https://base.garant.ru/30156539/",
    ]),
    ("20010406", "540", [
        "https://docs.cntd.ru/document/432860683",
        "https://base.garant.ru/30102287/",
    ]),

    # --- 2009–2014 ---
    ("20091002", "1079", [
        "https://docs.cntd.ru/document/432858713",
    ]),
    ("20110627", "1681", [
        "https://docs.cntd.ru/document/432857571",
    ]),
    ("20120523", "1974", [
        "https://docs.cntd.ru/document/432856981",
    ]),
    ("20120614", "2253", [
        "https://docs.cntd.ru/document/432856934",
        "https://topovl.ru/decree-2012.06.14-2253.html",
    ]),
    ("20120807", "2840", [
        "https://docs.cntd.ru/document/432856823",
    ]),
    ("20121227", "4534", [
        "https://docs.cntd.ru/document/432856551",
        "https://topovl.ru/decree-2012.12.27-4534.html",
    ]),
    ("20130129", "179", [
        "https://docs.cntd.ru/document/432856529",
        "https://topovl.ru/decree-2013.01.29-179.html",
    ]),
    ("20131022", "3025", [
        "https://docs.cntd.ru/document/432856025",
        "https://topovl.ru/decree-2013.10.22-3025.html",
    ]),
    ("20140130", "279", [
        "https://primorye-gov.ru/doc/14542",
    ]),
    ("20140626", "6835", [
        "https://docs.cntd.ru/document/432855518",
        "https://topovl.ru/decree-2014.06.26-6835.html",
    ]),
    ("20140715", "7237", [
        "https://docs.cntd.ru/document/432855482",
        "https://primorye-gov.ru/doc/27201",
        "https://topovl.ru/decree-2014.07.15-7237.html",
    ]),

    # --- 2015–2018 ---
    ("20150127", "1619", [
        "https://docs.cntd.ru/document/432855052",
        "https://primorye-gov.ru/doc/13153",
    ]),
    ("20150527", "7987", [
        "https://docs.cntd.ru/document/432854797",
    ]),
    ("20150603", "8091", [
        "https://docs.cntd.ru/document/432854776",
    ]),
    ("20160408", "1063", [
        "https://docs.cntd.ru/document/438877565",
    ]),
    ("20170131", "226", [
        "https://docs.cntd.ru/document/445090839",
        "https://topovl.ru/decree-2017.01.31-226.html",
    ]),
    ("20170531", "1374", [
        "https://docs.cntd.ru/document/450232259",
    ]),
    ("20170921", "2320", [
        "https://primorye-gov.ru/doc/44109",
    ]),
    ("20171215", "3026", [
        "https://docs.cntd.ru/document/446598337",
    ]),
    ("20180625", "1847", [
        "https://primorye-gov.ru/doc/45449",
    ]),
    ("20181114", "3111", [
        "https://www.vlc.ru/?menu=getfile&id=21026",
    ]),

    # --- 2019–2020 ---
    ("20190204", "570", [
        "https://docs.cntd.ru/document/550342853",
        "https://topovl.ru/decree-2019.02.04-570.html",
    ]),
    ("20190813", "2957", [
        "https://docs.cntd.ru/document/561514374",
    ]),
    ("20200423", "1635", [
        "https://docs.cntd.ru/document/570769114",
    ]),
    ("20200521", "1869", [
        "https://docs.cntd.ru/document/570801602",
    ]),
    ("20200521", "1874", [
        "https://docs.cntd.ru/document/570801603",
    ]),
    ("20200729", "2811", [
        "https://docs.cntd.ru/document/570892932",
    ]),

    # --- 2021 ---
    ("20210122", "147", [
        "https://docs.cntd.ru/document/571088872",
    ]),
    ("20210217", "564", [
        "https://docs.cntd.ru/document/574633150",
        "https://topovl.ru/decree-2021.02.17-564.html",
        "http://www.vlc25.ru/upload/iblock/87c/564.pdf",
    ]),
    ("20211221", "4376", [
        "https://docs.cntd.ru/document/578042977",
        "https://topovl.ru/decree-2021.12.21-4376.html",
        "http://www.vlc25.ru/docs/detail.php?ELEMENT_ID=2203",
    ]),

    # --- 2022 ---
    ("20220211", "285", [
        "https://docs.cntd.ru/document/578128061",
    ]),
    ("20220414", "777", [
        "https://docs.cntd.ru/document/406005941",
        "http://www.vlc25.ru/docs/detail.php?ELEMENT_ID=2637",
    ]),
    ("20220513", "1044", [
        "https://docs.cntd.ru/document/406039828",
        "https://prim-pravo.ru/postanovlenie/2022/05/13/n-1044/",
        "http://www.vlc25.ru/docs/detail.php?ELEMENT_ID=2766",
    ]),
    ("20220704", "1554", [
        "https://docs.cntd.ru/document/406130760",
        "https://primorye-gov.ru/doc/56170",
    ]),
    ("20220920", "2250", [
        "https://docs.cntd.ru/document/406239448",
    ]),

    # --- 2023 ---
    ("20230130", "182", [
        "https://docs.cntd.ru/document/406503677",
        "https://www.vlc.ru/documents/nap-heads-and-administration-of-Vladivostok/58967/",
    ]),
    ("20230321", "714", [
        "https://docs.cntd.ru/document/406585739",
        "https://topovl.ru/decree-2023.03.21-714.html",
        "http://www.vlc25.ru/docs/detail.php?ELEMENT_ID=4208",
    ]),
    ("20230623", "1593", [
        "https://docs.cntd.ru/document/406711771",
        "http://www.vlc25.ru/upload/iblock/53d/1593.pdf",
    ]),
    ("20230629", "1648", [
        "http://www.vlc25.ru/upload/iblock/fbb/1648.pdf",
    ]),
    ("20230815", "2056", [
        "https://topovl.ru/decree-2023.08.15-2056.html",
    ]),
    ("20230920", "2408", [
        "https://docs.cntd.ru/document/406817603",
        "https://topovl.ru/decree-2023.09.20-2408.html",
        "http://www.vlc25.ru/docs/detail.php?ELEMENT_ID=5196",
    ]),
    ("20231229", "3547", [
        "https://docs.cntd.ru/document/407058891",
    ]),

    # --- 2024 ---
    ("20240403", "806", [
        "https://docs.cntd.ru/document/407193036",
    ]),
    ("20240419", "951", [
        "https://docs.cntd.ru/document/407245434",
    ]),
    ("20240711", "1865", [
        "https://docs.cntd.ru/document/407341017",
    ]),
    ("20241009", "2825", [
        "https://docs.cntd.ru/document/407449455",
    ]),
    ("20241028", "3036", [
        "https://docs.cntd.ru/document/407466122",
    ]),
    ("20241225", "3720", [
        "https://docs.cntd.ru/document/407583094",
        "http://www.vlc25.ru/upload/iblock/dd8/tlhquxr5k2ik8cfxywy1zhiygxlfmjxk/3720.pdf",
    ]),

    # --- 2025 ---
    ("20250401", "880", [
        "https://docs.cntd.ru/document/407720618",
    ]),
    ("20250424", "1120", [
        "http://www.vlc25.ru/upload/iblock/2e2/jp69inkk4ypuxy1623roo3xbg8w9x7xs/1120.pdf",
    ]),
    ("20250714", "1911", [
        "http://www.vlc25.ru/docs/detail.php?ELEMENT_ID=8928",
    ]),
    ("20250723", "1989", [
        "http://www.vlc25.ru/upload/iblock/805/chggzrw7i1mtntdomxpodffn09f42mrk/1989.pdf",
    ]),
    ("20250929", "2702", [
        "https://www.vlc.ru/documents/nap-heads-and-administration-of-Vladivostok/121299/",
    ]),
    ("20251222", "3618", [
        "http://www.vlc25.ru/docs/detail.php?ELEMENT_ID=9961",
    ]),

    # --- 2026 ---
    ("20260326", "711", [
        "https://docs.cntd.ru/document/408242238",
        "http://www.vlc25.ru/docs/detail.php?ELEMENT_ID=10521",
    ]),
    ("20260707", "1807", [
        "http://www.vlc25.ru/docs/detail.php?ELEMENT_ID=11277",
    ]),
]


def is_pdf_url(url: str) -> bool:
    return url.lower().endswith(".pdf")


def extract_text_html(page, url: str) -> str:
    """Извлекает текст из HTML-страницы после рендеринга JS."""
    host = urlparse(url).netloc

    if "docs.cntd.ru" in host:
        selectors = [
            "div.document__text",
            "div.doc__text",
            "div#cont",
            "div.twelve.columns",
            "div.col-content",
            "main",
            "article",
            "div[class*='document']",
            "div[class*='content']",
        ]
        for sel in selectors:
            try:
                el = page.query_selector(sel)
                if el:
                    text = el.inner_text()
                    if len(text) > 200:
                        return text
            except Exception:
                continue
        return page.inner_text("body")

    elif "topovl.ru" in host:
        # topovl.ru — простой HTML, текст в основном блоке
        for sel in ["div.content", "article", "main", "div.post", "div.entry"]:
            try:
                el = page.query_selector(sel)
                if el:
                    text = el.inner_text()
                    if len(text) > 200:
                        return text
            except Exception:
                continue
        return page.inner_text("body")

    elif "prim-pravo.ru" in host:
        for sel in ["div.article-content", "div.post-content", "article", "main", "div.entry-content"]:
            try:
                el = page.query_selector(sel)
                if el:
                    text = el.inner_text()
                    if len(text) > 200:
                        return text
            except Exception:
                continue
        return page.inner_text("body")

    else:
        # primorye-gov.ru, base.garant.ru и прочие
        return page.inner_text("body")


def extract_text_pdf(pdf_path: str) -> str:
    """Извлекает текст из PDF через pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("  pypdf не установлен, пропускаю PDF")
        return ""
    try:
        reader = PdfReader(pdf_path)
        parts = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                parts.append(t)
        return "\n\n".join(parts)
    except Exception as e:
        print(f"  ОШИБКА чтения PDF: {e}")
        return ""


def text_to_markdown(text: str, date: str, number: str, url: str) -> str:
    """Форматирует текст в markdown."""
    lines = text.split("\n")
    md_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if md_lines and md_lines[-1] != "":
                md_lines.append("")
            continue
        upper = stripped.upper()
        if "АДМИНИСТРАЦИЯ" in upper and "ВЛАДИВОСТОКА" in upper:
            md_lines.append(f"# {stripped}")
        elif upper == "ПОСТАНОВЛЕНИЕ":
            md_lines.append(f"## {stripped}")
        elif re.match(r"^\d+\.\s", stripped):
            md_lines.append(f"### {stripped}")
        elif "постановляет" in stripped.lower():
            md_lines.append(f"**{stripped}**")
        else:
            md_lines.append(stripped)

    date_fmt = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
    md_lines.append("")
    md_lines.append("---")
    md_lines.append(f"**Дата:** {date_fmt}")
    md_lines.append(f"**Номер:** {number}")
    md_lines.append(f"**Источник:** {url}")
    return "\n".join(md_lines)


def process_document(page, date: str, number: str, urls: list) -> bool:
    filename = f"{date}-{number}.md"
    filepath = os.path.join(OUT_DIR, filename)

    if os.path.exists(filepath):
        print(f"  Уже скачан: {filename}")
        return True

    print(f"Загружаю: {filename}")

    for url in urls:
        tag = "PDF" if is_pdf_url(url) else "HTML"
        print(f"  Попытка [{tag}]: {url}")

        if is_pdf_url(url):
            # Скачиваем PDF через browser
            try:
                resp = page.context.request.get(url, timeout=30000)
                if resp.ok:
                    pdf_bytes = resp.body()
                    tmp_pdf = os.path.join(OUT_DIR, f"_tmp_{date}_{number}.pdf")
                    with open(tmp_pdf, "wb") as f:
                        f.write(pdf_bytes)
                    text = extract_text_pdf(tmp_pdf)
                    os.remove(tmp_pdf)
                    if len(text.strip()) > 100:
                        markdown = text_to_markdown(text, date, number, url)
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(markdown)
                        print(f"  Сохранён: {filepath} ({len(text)} символов)")
                        return True
                    else:
                        print(f"  PDF: текст слишком короткий ({len(text)} символов)")
                else:
                    print(f"  PDF: HTTP {resp.status}")
            except Exception as e:
                print(f"  PDF: ошибка — {e}")
        else:
            # HTML через Playwright
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                try:
                    page.wait_for_selector(
                        "div.document__text, div.doc__text, div#cont, "
                        "main, article, div.content, div.post",
                        timeout=15000,
                    )
                except Exception:
                    page.wait_for_timeout(3000)
            except Exception as e:
                print(f"  ОШИБКА навигации: {e}")
                continue

            text = extract_text_html(page, url)
            if len(text.strip()) > 200:
                markdown = text_to_markdown(text, date, number, url)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(markdown)
                print(f"  Сохранён: {filepath} ({len(text)} символов)")
                return True
            else:
                print(f"  Текст слишком короткий ({len(text)} символов)")

        time.sleep(0.5)

    print(f"  НЕ УДАЛОСЬ скачать — все источники исчерпаны")
    return False


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    total = len(DOCUMENTS)
    ok = 0
    fail = 0
    failed_list = []

    print(f"Всего документов: {total}")
    print(f"Папка: {OUT_DIR}/")
    print("-" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
            locale="ru-RU",
        )
        page = context.new_page()

        for date, number, urls in DOCUMENTS:
            success = process_document(page, date, number, urls)
            if success:
                ok += 1
            else:
                fail += 1
                failed_list.append(f"{date}-{number}")
            time.sleep(DELAY)

        browser.close()

    print("-" * 60)
    print(f"Готово: {ok} успешно, {fail} с ошибками из {total}")
    if failed_list:
        print("\nНе скачались:")
        for f in failed_list:
            print(f"  {f}.md")


if __name__ == "__main__":
    main()
