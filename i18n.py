"""UI translations. Key = the German text (the app's source language); missing entries fall back to German."""

LANGS = {"Deutsch": "de", "English": "en", "Русский": "ru"}

T = {
    "Betrifft mich CBAM? Prüfung Ihrer Stahl- und Aluminiumimporte gegen Anhang I und die 50-Tonnen-Schwelle — jede Zahl mit Quelle.": {
        "en": "Does CBAM apply to me? Checks your steel and aluminium imports against Annex I and the 50-tonne threshold — every number with a source.",
        "ru": "Касается ли меня CBAM? Проверка импорта стали и алюминия по Приложению I и порогу 50 тонн — у каждой цифры есть источник."},
    "data/annex_i.json fehlt — ohne Anhang I ist keine Prüfung möglich.": {
        "en": "data/annex_i.json is missing — no check is possible without Annex I.",
        "ru": "Нет файла data/annex_i.json — без Приложения I проверка невозможна."},
    "1. Importe erfassen": {"en": "1. Enter imports", "ru": "1. Внести импорт"},
    "Rechnungen (PDF) hochladen": {"en": "Upload invoices (PDF)", "ru": "Загрузить счета (PDF)"},
    "CSV hochladen": {"en": "Upload CSV", "ru": "Загрузить CSV"},
    "{n} Dokument(e) gelesen: {inv} Rechnungszeile(n), {plan} geplante Zeile(n) aus Auftragsbestätigungen.": {
        "en": "{n} document(s) read: {inv} invoice line(s), {plan} planned line(s) from order confirmations.",
        "ru": "Прочитано документов: {n}. Строк счетов: {inv}, запланированных строк из подтверждений заказа: {plan}."},
    "Rechnungen und Auftragsbestätigungen als PDF (mit Textebene). Auftragsbestätigungen zählen als **geplante** Einfuhr, nicht als bereits eingeführt.": {
        "en": "Invoices and order confirmations as PDF (with a text layer). Order confirmations count as **planned** imports, not as already imported.",
        "ru": "Счета и подтверждения заказов в PDF (с текстовым слоем). Подтверждения заказов считаются **запланированным** ввозом, а не уже ввезённым."},
    "PDF-Dokumente": {"en": "PDF documents", "ru": "PDF-документы"},
    "Spalten: ": {"en": "Columns: ", "ru": "Колонки: "},
    "Einkaufsliste (CSV)": {"en": "Purchase list (CSV)", "ru": "Список закупок (CSV)"},
    "Demo-Rechnungen laden (CSV)": {"en": "Load demo invoices (CSV)", "ru": "Загрузить демо-счета (CSV)"},
    "Demo-PDFs einlesen ({n} Dokumente)": {"en": "Read demo PDFs ({n} documents)", "ru": "Прочитать демо-PDF ({n} док.)"},
    "Demo-Daten fehlen (demo/purchases_2026.csv).": {"en": "Demo data missing (demo/purchases_2026.csv).", "ru": "Нет демо-данных (demo/purchases_2026.csv)."},
    "Fehlende Spalten: ": {"en": "Missing columns: ", "ru": "Не хватает колонок: "},
    "Bitte KN-Codes und Gewichte prüfen — Sie können jede Zelle korrigieren.": {
        "en": "Please check CN codes and weights — you can correct any cell.",
        "ru": "Проверьте коды КН и вес — любую ячейку можно исправить."},
    "2. Welche Waren sind CBAM-Waren?": {"en": "2. Which goods are CBAM goods?", "ru": "2. Какие товары подпадают под CBAM?"},
    "CBAM-Ware": {"en": "CBAM good", "ru": "Товар CBAM"},
    "Anhang I": {"en": "Annex I", "ru": "Приложение I"},
    "Quelle": {"en": "Source", "ru": "Источник"},
    "{n} Zeile(n) ohne gültigen KN-Code — bitte oben ergänzen.": {
        "en": "{n} line(s) without a valid CN code — please add it above.",
        "ru": "Строк без корректного кода КН: {n} — допишите код в таблице выше."},
    "3. 50-Tonnen-Schwelle": {"en": "3. 50-tonne threshold", "ru": "3. Порог 50 тонн"},
    "Kalenderjahr": {"en": "Calendar year", "ru": "Календарный год"},
    "{t:.1f} t von {max:.0f} t CBAM-Waren im Jahr {year}": {
        "en": "{t:.1f} t of {max:.0f} t of CBAM goods in {year}",
        "ru": "{t:.1f} t из {max:.0f} t товаров CBAM за {year} год"},
    "Unter der Schwelle: von CBAM-Pflichten befreit. Die Befreiung ist in der Zollanmeldung anzugeben.": {
        "en": "Below the threshold: exempt from CBAM obligations. State the exemption in the customs declaration.",
        "ru": "Ниже порога: вы освобождены от обязанностей CBAM. Освобождение нужно указать в таможенной декларации."},
    "Über 80 % der Schwelle — weitere Importe können die Pflicht auslösen.": {
        "en": "Above 80 % of the threshold — further imports can trigger the obligation.",
        "ru": "Больше 80 % порога — следующие закупки могут сделать вас обязанным по CBAM."},
    "Schwelle überschritten (oder Strom/Wasserstoff importiert): Sie brauchen den Status als zugelassener CBAM-Anmelder.": {
        "en": "Threshold exceeded (or electricity/hydrogen imported): you need the status of authorised CBAM declarant.",
        "ru": "Порог превышен (или ввезены электроэнергия/водород): нужен статус уполномоченного декларанта CBAM."},
    "Prognose beim bisherigen Tempo: Schwelle erreicht am **{d}**.": {
        "en": "Forecast at the current pace: threshold reached on **{d}**.",
        "ru": "Прогноз при текущем темпе: порог будет достигнут **{d}**."},
    "Geplante Lieferungen laut Auftragsbestätigung: **{p:.1f} t** CBAM-Waren → danach **{a:.1f} t** von {max:.0f} t.": {
        "en": "Planned deliveries per order confirmation: **{p:.1f} t** of CBAM goods → afterwards **{a:.1f} t** of {max:.0f} t.",
        "ru": "Запланировано по подтверждениям заказа: **{p:.1f} t** товаров CBAM → после поставки **{a:.1f} t** из {max:.0f} t."},
    " Diese Lieferung würde die Schwelle überschreiten — Zulassung vorher beantragen (Option B) oder Menge reduzieren (Option A).": {
        "en": " This delivery would exceed the threshold — apply for authorisation first (option B) or reduce the quantity (option A).",
        "ru": " Эта поставка превысит порог — заранее подайте заявку на допуск (вариант B) или уменьшите объём (вариант A)."},
    "Quelle: [Verordnung (EU) 2025/2083 (CBAM-Omnibus)]({o}), Anhang I der [Verordnung (EU) 2023/956]({r}).": {
        "en": "Source: [Regulation (EU) 2025/2083 (CBAM Omnibus)]({o}), Annex I of [Regulation (EU) 2023/956]({r}).",
        "ru": "Источник: [Регламент (ЕС) 2025/2083 (CBAM Omnibus)]({o}), Приложение I [Регламента (ЕС) 2023/956]({r})."},
    "4. Kosten und Risiko": {"en": "4. Cost and risk", "ru": "4. Стоимость и риск"},
    "Standardwerte oder Zertifikatspreise fehlen noch (data/default_values.csv, data/cbam_prices.json).": {
        "en": "Default values or certificate prices are missing (data/default_values.csv, data/cbam_prices.json).",
        "ru": "Нет значений по умолчанию или цен сертификатов (data/default_values.csv, data/cbam_prices.json)."},
    "Graue Emissionen": {"en": "Embedded emissions", "ru": "Встроенные выбросы"},
    "Zertifikate (Quartalspreise)": {"en": "Certificates (quarterly prices)", "ru": "Сертификаты (квартальные цены)"},
    "Strafe ohne Zulassung": {"en": "Penalty without authorisation", "ru": "Штраф без допуска"},
    "{n} Zeile(n) ohne Standardwert für Herkunftsland/KN — nicht geschätzt.": {
        "en": "{n} line(s) without a default value for origin/CN — not estimated.",
        "ru": "Строк без значения по умолчанию для страны/кода: {n} — не оценены."},
    "Standardwerte inkl. Aufschlag des Jahres (DVO (EU) 2025/2621). Zertifikatspreis des Einfuhrquartals: [Europäische Kommission]({u}). Strafe: 3–5 × € 100 je fehlendem Zertifikat, auf alle Emissionen des Jahres (Art. 26 Abs. 2a, vor Indexierung).": {
        "en": "Default values incl. the year's mark-up (Impl. Reg. (EU) 2025/2621). Certificate price of the import quarter: [European Commission]({u}). Penalty: 3–5 × € 100 per missing certificate, on all emissions of the year (Art. 26(2a), before indexation).",
        "ru": "Значения по умолчанию с надбавкой года (Исп. регламент (ЕС) 2025/2621). Цена сертификата — квартала ввоза: [Еврокомиссия]({u}). Штраф: 3–5 × € 100 за каждый недостающий сертификат, на все выбросы года (ст. 26(2a), до индексации)."},
    "5. Ihre Optionen": {"en": "5. Your options", "ru": "5. Ваши варианты"},
    "A · Unter 50 t bleiben": {"en": "A · Stay below 50 t", "ru": "A · Остаться ниже 50 t"},
    "Noch **{t:.1f} t** bis zur Schwelle. Käufe planen und dokumentieren.": {
        "en": "**{t:.1f} t** left until the threshold. Plan and document purchases.",
        "ru": "До порога осталось **{t:.1f} t**. Планируйте и документируйте закупки."},
    "B · Zulassung beantragen": {"en": "B · Apply for authorisation", "ru": "B · Подать заявку на допуск"},
    "Antrag als zugelassener CBAM-Anmelder beim AnEH (cbam@bmf.gv.at), bevor die Schwelle überschritten wird.": {
        "en": "Apply to the AnEH (cbam@bmf.gv.at) as authorised CBAM declarant before the threshold is exceeded.",
        "ru": "Подайте заявку на статус уполномоченного декларанта CBAM в AnEH (cbam@bmf.gv.at) до превышения порога."},
    "Checkliste Antrag": {"en": "Application checklist (German)", "ru": "Чек-лист заявки (на немецком)"},
    "C · Lieferant fragen": {"en": "C · Ask your supplier", "ru": "C · Запросить поставщика"},
    "Echte Emissionsdaten beim Lieferanten anfordern — oft niedriger als die Standardwerte.": {
        "en": "Request actual emission data from the supplier — often lower than the default values.",
        "ru": "Запросите у поставщика фактические данные о выбросах — часто они ниже значений по умолчанию."},
    "6. Dokumente": {"en": "6. Documents", "ru": "6. Документы"},
    "Ihr Unternehmen": {"en": "Your company", "ru": "Ваша компания"},
    "Brief an Lieferanten (Anfrage echter Emissionsdaten)": {
        "en": "Letter to supplier (request for actual emission data)",
        "ru": "Письмо поставщику (запрос фактических выбросов)"},
    "Sprache des Briefs": {"en": "Letter language", "ru": "Язык письма"},
    "Brief": {"en": "Letter", "ru": "Письмо"},
    "Brief herunterladen (.txt)": {"en": "Download letter (.txt)", "ru": "Скачать письмо (.txt)"},
    "Bericht herunterladen (PDF)": {"en": "Download report (PDF, German)", "ru": "Скачать отчёт (PDF, на немецком)"},
    "7. Fragen an den Lotsen": {"en": "7. Ask the pilot", "ru": "7. Вопросы помощнику"},
    "KI-Assistent aus (kein GEMINI_API_KEY) — Sie erhalten eine feste Zusammenfassung.": {
        "en": "AI assistant off (no GEMINI_API_KEY) — you get a fixed summary.",
        "ru": "ИИ-помощник выключен (нет GEMINI_API_KEY) — вы получите готовую сводку."},
    "z. B. Was passiert, wenn ich im Herbst noch 20 t Profile kaufe?": {
        "en": "e.g. What happens if I buy another 20 t of profiles in autumn?",
        "ru": "например: что будет, если осенью я куплю ещё 20 t профилей?"},
    "Der Lotse rechnet …": {"en": "Calculating …", "ru": "Считаю …"},
    "Werkzeug": {"en": "Tool", "ru": "Инструмент"},
}


def tr(text, lang, **kw):
    """Translate a German UI text and fill its {placeholders}."""
    s = T.get(text, {}).get(lang, text)
    return s.format(**kw) if kw else s
