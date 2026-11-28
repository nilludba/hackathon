"""UI translations. Key = the German text (the app's source language); missing entries fall back to German."""

LANGS = {"DE": "de", "EN": "en"}

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
    "7. Fragen an CBAM Helper": {"en": "7. Ask CBAM Helper", "ru": "7. Вопросы помощнику"},
    "KI-Assistent aus (kein GEMINI_API_KEY) — Sie erhalten eine feste Zusammenfassung.": {
        "en": "AI assistant off (no GEMINI_API_KEY) — you get a fixed summary.",
        "ru": "ИИ-помощник выключен (нет GEMINI_API_KEY) — вы получите готовую сводку."},
    "z. B. Was passiert, wenn ich im Herbst noch 20 t Profile kaufe?": {
        "en": "e.g. What happens if I buy another 20 t of profiles in autumn?",
        "ru": "например: что будет, если осенью я куплю ещё 20 t профилей?"},
    "CBAM Helper rechnet …": {"en": "Calculating …", "ru": "Считаю …"},
    "Werkzeug": {"en": "Tool", "ru": "Инструмент"},
    "**So funktioniert es**\n\n1. Rechnungen hochladen oder Demo laden\n2. Ergebnis lesen: Betrifft mich CBAM?\n3. Nächsten Schritt wählen und Dokumente herunterladen": {
        "en": "**How it works**\n\n1. Upload invoices or load the demo\n2. Read the result: does CBAM apply to me?\n3. Pick the next step and download documents",
        "ru": "**Как это работает**\n\n1. Загрузите счета или откройте демо\n2. Прочитайте итог: касается ли меня CBAM?\n3. Выберите следующий шаг и скачайте документы"},
    "Ersteinschätzung, keine Rechtsberatung. Zuständig in Österreich: AnEH, cbam@bmf.gv.at.": {
        "en": "First assessment, not legal advice. Competent authority in Austria: AnEH, cbam@bmf.gv.at.",
        "ru": "Предварительная оценка, не юридическая консультация. Ведомство в Австрии: AnEH, cbam@bmf.gv.at."},
    "Was ist CBAM? (30 Sekunden)": {"en": "What is CBAM? (30 seconds)", "ru": "Что такое CBAM? (30 секунд)"},
    "Seit 1. Jänner 2026 kostet die Einfuhr von Stahl, Aluminium, Zement, Dünger, Strom und Wasserstoff in die EU einen CO₂-Preis. Wer mehr als **50 Tonnen** solcher Waren pro Jahr einführt, braucht vorher eine Zulassung. Ohne Zulassung drohen **€ 300–500 Strafe je Tonne CO₂**. Ob eine Ware zählt, entscheidet ihr Zolltarif-Code (KN-Code).": {
        "en": "Since 1 January 2026, importing steel, aluminium, cement, fertilisers, electricity and hydrogen into the EU carries a CO₂ price. Anyone importing more than **50 tonnes** of such goods per year needs an authorisation first. Without it, the penalty is **€ 300–500 per tonne of CO₂**. Whether a product counts depends on its customs code (CN code).",
        "ru": "С 1 января 2026 года за ввоз в ЕС стали, алюминия, цемента, удобрений, электроэнергии и водорода нужно платить за CO₂. Кто ввозит больше **50 тонн** таких товаров в год, должен заранее получить допуск. Без допуска штраф — **€ 300–500 за тонну CO₂**. Подпадает ли товар, решает его таможенный код (код КН)."},
    "Schritt 1": {"en": "Step 1", "ru": "Шаг 1"},
    "Schritt 2": {"en": "Step 2", "ru": "Шаг 2"},
    "Schritt 3": {"en": "Step 3", "ru": "Шаг 3"},
    "Ihre Einkäufe": {"en": "Your purchases", "ru": "Ваши закупки"},
    "Demo ausprobieren": {"en": "Try the demo", "ru": "Попробовать демо"},
    "Metallbau Gruber GmbH (Beispiel): Träger und Schrauben aus der Türkei, Alu-Profile aus China, Ventile.": {
        "en": "Metallbau Gruber GmbH (example): beams and screws from Turkey, aluminium profiles from China, valves.",
        "ru": "Metallbau Gruber GmbH (пример): балки и винты из Турции, алюминиевые профили из Китая, вентили."},
    "Laden Sie die Demo oder Ihre Rechnungen — das Ergebnis erscheint dann hier.": {
        "en": "Load the demo or your invoices — the result will appear here.",
        "ru": "Откройте демо или загрузите свои счета — итог появится здесь."},
    "Erkannte Positionen prüfen und korrigieren ({n})": {
        "en": "Check and correct the recognised lines ({n})", "ru": "Проверить и исправить распознанные строки ({n})"},
    "Ware": {"en": "Product", "ru": "Товар"},
    "KN-Code": {"en": "CN code", "ru": "Код КН"},
    "Nettomasse (kg)": {"en": "Net mass (kg)", "ru": "Масса нетто (кг)"},
    "Land": {"en": "Country", "ru": "Страна"},
    "Datum": {"en": "Date", "ru": "Дата"},
    "Lieferant": {"en": "Supplier", "ru": "Поставщик"},
    "Ihr Ergebnis": {"en": "Your result", "ru": "Ваш итог"},
    "Sie sind befreit: {t:.1f} t von 50 t": {"en": "You are exempt: {t:.1f} t of 50 t", "ru": "Вы освобождены: {t:.1f} t из 50 t"},
    "Achtung: {t:.1f} t von 50 t — knapp unter der Schwelle": {
        "en": "Careful: {t:.1f} t of 50 t — just below the threshold", "ru": "Внимание: {t:.1f} t из 50 t — почти на пороге"},
    "Schwelle überschritten: {t:.1f} t von 50 t": {"en": "Threshold exceeded: {t:.1f} t of 50 t", "ru": "Порог превышен: {t:.1f} t из 50 t"},
    "Sie müssen derzeit nichts zahlen. Geben Sie die Befreiung in der Zollanmeldung an und behalten Sie die Menge im Blick.": {
        "en": "You pay nothing for now. State the exemption in the customs declaration and keep an eye on the quantity.",
        "ru": "Сейчас платить ничего не нужно. Укажите освобождение в таможенной декларации и следите за объёмом."},
    "Noch {left:.1f} t, dann brauchen Sie eine Zulassung als CBAM-Anmelder — sonst drohen hohe Strafen.": {
        "en": "{left:.1f} t more and you need authorisation as a CBAM declarant — otherwise high penalties apply.",
        "ru": "Ещё {left:.1f} t — и понадобится допуск декларанта CBAM, иначе грозят большие штрафы."},
    "Sie brauchen den Status als zugelassener CBAM-Anmelder. Ohne Zulassung drohen hohe Strafen.": {
        "en": "You need the status of authorised CBAM declarant. Without it, high penalties apply.",
        "ru": "Нужен статус уполномоченного декларанта CBAM. Без него грозят большие штрафы."},
    "Ihre geplanten Lieferungen ({p:.1f} t) würden die Schwelle überschreiten.": {
        "en": "Your planned deliveries ({p:.1f} t) would exceed the threshold.",
        "ru": "Запланированные поставки ({p:.1f} t) превысят порог."},
    "Was jetzt?": {"en": "What now?", "ru": "Что делать?"},
    "✅ Nächste Schritte": {"en": "✅ Next steps", "ru": "✅ Следующие шаги"},
    "📦 Waren": {"en": "📦 Goods", "ru": "📦 Товары"},
    "💶 Kosten": {"en": "💶 Cost", "ru": "💶 Стоимость"},
    "💬 Fragen": {"en": "💬 Questions", "ru": "💬 Вопросы"},
    "Dokumente": {"en": "Documents", "ru": "Документы"},
    "**{y}** CBAM-Ware(n) · **{n}** nicht betroffen · **{u}** unklar": {
        "en": "**{y}** CBAM good(s) · **{n}** not affected · **{u}** unclear",
        "ru": "Товаров CBAM: **{y}** · не подпадают: **{n}** · неясно: **{u}**"},
    "Menge (t)": {"en": "Quantity (t)", "ru": "Количество (t)"},
    "So rechnen wir: **Menge × Standardwert der EU (t CO₂ je t Ware) × Zertifikatspreis des Quartals**.": {
        "en": "How we calculate: **quantity × EU default value (t CO₂ per t of goods) × certificate price of the quarter**.",
        "ru": "Как считаем: **количество × значение ЕС по умолчанию (t CO₂ на t товара) × цена сертификата за квартал**."},
    "Rechnung": {"en": "Calculation", "ru": "Расчёт"},
    "Ihre Frage": {"en": "Your question", "ru": "Ваш вопрос"},
    "Fragen": {"en": "Ask", "ru": "Спросить"},

    "{n} Zeile(n) ohne Gewicht oder Datum werden nicht gezählt — bitte oben ergänzen.": {
        "en": "{n} line(s) without weight or date are not counted — please complete them above.",
        "ru": "Строк без веса или даты: {n} — они не учитываются, допишите их в таблице выше."},
}


# --- added by Matvey + Claude: CN suggestions, decision costs, what-if, self-check ---
T.update({
    '**Kein KN-Code** bei „{d}“': {'en': '**No CN code** for “{d}”', 'ru': '**Нет кода КН** у «{d}»'},
    'Bitte einen gültigen KN-Code eingeben (mindestens 4 Ziffern).': {'en': 'Please enter a valid CN code (at least 4 digits).', 'ru': 'Введите корректный код КН (не меньше 4 цифр).'},
    'Danach: **{n:.1f} t** von 50 t (bisher {b:.1f} t inkl. geplanter Lieferungen).': {'en': 'Afterwards: **{n:.1f} t** of 50 t (so far {b:.1f} t incl. planned deliveries).', 'ru': 'После этого: **{n:.1f} т** из 50 т (сейчас {b:.1f} т с учётом запланированных поставок).'},
    'Die KI liest nur und erklärt. Anhang I, Schwelle und Kosten rechnet geprüfter Code. Sie können die automatischen Tests hier selbst laufen lassen.': {'en': 'The AI only reads and explains. Annex I, the threshold and the costs are computed by tested code. You can run the automated tests here yourself.', 'ru': 'ИИ только читает и объясняет. Приложение I, порог и стоимость считает проверенный код. Автоматические тесты можно запустить здесь самому.'},
    'Dieselbe Menge aus verschiedenen Ländern (EU-Standardwerte, Preis des Einfuhrquartals):': {'en': 'The same quantity from different countries (EU default values, price of the import quarter):', 'ru': 'То же количество из разных стран (стандартные значения ЕС, цена квартала ввоза):'},
    'EU-Tabelle': {'en': 'EU table', 'ru': 'Таблица ЕС'},
    'Für diesen KN-Code gibt es in unseren Daten keinen Standardwert.': {'en': 'There is no default value for this CN code in our data.', 'ru': 'Для этого кода КН в наших данных нет стандартного значения.'},
    'Herkunft': {'en': 'Origin', 'ru': 'Страна происхождения'},
    'KN-Code der Ware': {'en': 'CN code of the goods', 'ru': 'Код КН товара'},
    'Kein Vorschlag möglich — bitte Code in der Tabelle unten eintragen ([Zolltarif TARIC]({u})).': {'en': 'No suggestion possible — please enter the code in the table below ([TARIC tariff]({u})).', 'ru': 'Подсказать не получается — впишите код в таблицу ниже ([тариф TARIC]({u})).'},
    'Keine CBAM-Ware — zählt nicht zur 50-t-Schwelle.': {'en': 'Not a CBAM good — does not count towards the 50 t threshold.', 'ru': 'Не товар CBAM — в порог 50 т не входит.'},
    'Kosten im Jahr': {'en': 'Cost for the year', 'ru': 'Затраты за год'},
    'Menge': {'en': 'Quantity', 'ru': 'Количество'},
    'Mit geplanter Lieferung und Zulassung': {'en': 'With planned delivery and authorisation', 'ru': 'С запланированной поставкой и статусом декларанта'},
    'Ohne geplante Lieferung': {'en': 'Without planned delivery', 'ru': 'Без запланированной поставки'},
    'Schwelle überschritten — Zulassung nötig.': {'en': 'Threshold exceeded — authorisation needed.', 'ru': 'Порог превышен — нужен статус декларанта.'},
    'Standardwert': {'en': 'Default value', 'ru': 'Стандартное значение'},
    'Szenario': {'en': 'Scenario', 'ru': 'Сценарий'},
    'Tests ausführen': {'en': 'Run tests', 'ru': 'Запустить тесты'},
    'Vorschlag nach Warenbeschreibung, bitte prüfen ([Zolltarif TARIC]({u})).': {'en': 'Suggestion based on the description, please check ([TARIC tariff]({u})).', 'ru': 'Подсказка по описанию товара, пожалуйста, проверьте ([тариф TARIC]({u})).'},
    'Vorschlag: **{cn}** — {label} · {v} · Sicherheit: {c}': {'en': 'Suggestion: **{cn}** — {label} · {v} · confidence: {c}', 'ru': 'Подсказка: **{cn}** — {label} · {v} · уверенность: {c}'},
    'Was kostet welche Entscheidung?': {'en': 'What does each decision cost?', 'ru': 'Сколько стоит каждое решение?'},
    'Was passiert mit einer zusätzlichen Bestellung? Und was kostet dieselbe Ware aus einem anderen Land?': {'en': 'What happens with an extra order? And what does the same goods cost from another country?', 'ru': 'Что будет при дополнительном заказе? И сколько стоит тот же товар из другой страны?'},
    'Weiter befreit.': {'en': 'Still exempt.', 'ru': 'По-прежнему освобождены.'},
    'Wird die Schwelle überschritten, zählen alle CBAM-Waren des Jahres, nicht nur die Menge über 50 t. Lieferung später planen ist zulässig; Lieferungen künstlich aufzuteilen, um unter 50 t zu bleiben, ist es nicht.': {'en': 'Once the threshold is exceeded, all CBAM goods of the year count, not only the amount above 50 t. Planning a delivery later is allowed; artificially splitting deliveries to stay below 50 t is not.', 'ru': 'При превышении порога считаются все товары CBAM за год, а не только то, что сверх 50 т. Перенести поставку можно; искусственно дробить поставки, чтобы остаться ниже 50 т, нельзя.'},
    'Zahlen gelten, wenn Sie über 50 t liegen. Echte Lieferantendaten können niedriger sein (Option C).': {'en': 'These figures apply if you are above 50 t. Real supplier data may be lower (option C).', 'ru': 'Цифры действуют, если вы выше 50 т. Реальные данные поставщика могут быть ниже (вариант C).'},
    'Zertifikate': {'en': 'Certificates', 'ru': 'Сертификаты'},
    'keine CBAM-Ware': {'en': 'not a CBAM good', 'ru': 'не товар CBAM'},
    't CO₂ je t Ware': {'en': 't CO₂ per t of goods', 'ru': 'т CO₂ на т товара'},
    'Über 50 t ohne Zulassung': {'en': 'Above 50 t without authorisation', 'ru': 'Выше 50 т без статуса декларанта'},
    'Übernehmen': {'en': 'Apply', 'ru': 'Принять'},
    '€ 0 (befreit)': {'en': '€ 0 (exempt)', 'ru': '€ 0 (освобождены)'},
    '🔮 Was wäre wenn': {'en': '🔮 What if', 'ru': '🔮 Что если'},
    '🧪 Wie prüfen wir uns selbst?': {'en': '🧪 How do we check ourselves?', 'ru': '🧪 Как мы себя проверяем?'},
    'hoch': {'en': 'high', 'ru': 'высокая'},
    'mittel': {'en': 'medium', 'ru': 'средняя'},
    'niedrig': {'en': 'low', 'ru': 'низкая'},
})


T.update({
    'Achtung: Ihre geplante Lieferung bringt Sie auf {n:.1f} t von 50 t': {'en': 'Careful: your planned delivery takes you to {n:.1f} t of 50 t', 'ru': 'Внимание: запланированная поставка доведёт вас до {n:.1f} т из 50 т'},
    'Eingeführt {year}: {t:.1f} t': {'en': 'Imported {year}: {t:.1f} t', 'ru': 'Ввезено в {year}: {t:.1f} т'},
    'Falls über 50 t: Zertifikate': {'en': 'If above 50 t: certificates', 'ru': 'Если выше 50 т: сертификаты'},
    'Geplant: {p:.1f} t': {'en': 'Planned: {p:.1f} t', 'ru': 'Запланировано: {p:.1f} т'},
    'Heute sind Sie mit {t:.1f} t noch befreit. Die bestätigte Bestellung über {p:.1f} t würde die Schwelle überschreiten — entscheiden Sie vorher (Schritt 3).': {'en': 'Today you are still exempt with {t:.1f} t. The confirmed order of {p:.1f} t would cross the threshold — decide before it arrives (step 3).', 'ru': 'Сейчас у вас {t:.1f} т и вы освобождены. Подтверждённый заказ на {p:.1f} т превысит порог — решите заранее (шаг 3).'},
    'Heute zu zahlen': {'en': 'To pay today', 'ru': 'К оплате сейчас'},
    'Mit Zulassung: Menge × EU-Standardwert × Zertifikatspreis des Quartals, für alle Waren des Jahres.': {'en': 'With authorisation: quantity × EU default value × certificate price of the quarter, for all goods of the year.', 'ru': 'Со статусом декларанта: количество × стандартное значение ЕС × цена сертификата квартала, по всем товарам за год.'},
    'Nach der Lieferung ohne Zulassung': {'en': 'After the delivery, without authorisation', 'ru': 'После поставки без статуса декларанта'},
    'Nach der Lieferung: Zertifikate': {'en': 'After the delivery: certificates', 'ru': 'После поставки: сертификаты'},
    'Strafe 3–5 × € 100 je fehlendem Zertifikat (Art. 26 Abs. 2a).': {'en': 'Fine of 3–5 × €100 per missing certificate (Art. 26(2a)).', 'ru': 'Штраф 3–5 × €100 за каждый недостающий сертификат (ст. 26(2a)).'},
    'Zertifikate für alle CBAM-Waren des Jahres, sobald Sie über 50 t liegen.': {'en': 'Certificates for all CBAM goods of the year once you are above 50 t.', 'ru': 'Сертификаты на все товары CBAM за год, как только вы выше 50 т.'},
})


# CN suggestion labels (cbam/suggest.py)
T.update({
    'Nägel, Drahtstifte, Krampen aus Eisen oder Stahl': {'en': 'Nails, tacks, staples of iron or steel', 'ru': 'Гвозди, кнопки, скобы из железа или стали'},
    'Schrauben, Bolzen, Muttern … aus Aluminium': {'en': 'Screws, bolts, nuts … of aluminium', 'ru': 'Винты, болты, гайки … из алюминия'},
    'Schrauben, Bolzen, Muttern … aus Eisen oder Stahl': {'en': 'Screws, bolts, nuts … of iron or steel', 'ru': 'Винты, болты, гайки … из железа или стали'},
    'Armaturen, Hähne, Ventile': {'en': 'Taps, cocks, valves', 'ru': 'Арматура, краны, клапаны'},
    'Konstruktionen und Konstruktionsteile aus Aluminium': {'en': 'Structures and parts of structures of aluminium', 'ru': 'Конструкции и их части из алюминия'},
    'Konstruktionen und Konstruktionsteile aus Eisen oder Stahl': {'en': 'Structures and parts of structures of iron or steel', 'ru': 'Конструкции и их части из железа или стали'},
    'Stangen (Stäbe) und Profile aus Aluminium': {'en': 'Aluminium bars, rods and profiles', 'ru': 'Прутки и профили из алюминия'},
    'Profile aus Eisen oder nicht legiertem Stahl (Träger, Winkel)': {'en': 'Sections of iron or non-alloy steel (beams, angles)', 'ru': 'Профили из железа или нелегированной стали (балки, уголки)'},
    'Rohre aus Aluminium': {'en': 'Aluminium tubes and pipes', 'ru': 'Трубы из алюминия'},
    'Andere Rohre und Hohlprofile aus Eisen oder Stahl': {'en': 'Other tubes, pipes and hollow profiles of iron or steel', 'ru': 'Прочие трубы и полые профили из железа или стали'},
    'Folien und dünne Bänder aus Aluminium': {'en': 'Aluminium foil and thin strip', 'ru': 'Алюминиевая фольга и тонкая лента'},
    'Bleche und Bänder aus Aluminium (> 0,2 mm)': {'en': 'Aluminium plates, sheets and strip (> 0.2 mm)', 'ru': 'Листы и ленты из алюминия (> 0,2 мм)'},
    'Flachgewalzte Erzeugnisse aus Stahl (warmgewalzt) — Breite/Behandlung prüfen': {'en': 'Flat-rolled steel products (hot-rolled) — check width/treatment', 'ru': 'Плоский прокат из стали (горячекатаный) — проверьте ширину и обработку'},
    'Draht aus Aluminium': {'en': 'Aluminium wire', 'ru': 'Алюминиевая проволока'},
    'Draht aus Eisen oder nicht legiertem Stahl': {'en': 'Wire of iron or non-alloy steel', 'ru': 'Проволока из железа или нелегированной стали'},
    'Portlandzement (grau) — Zementart prüfen': {'en': 'Portland cement (grey) — check cement type', 'ru': 'Портландцемент (серый) — проверьте тип цемента'},
})


# Minimal redesign (hero, sections, footer)
T.update({
    '1 Minute': {"en": '1 minute'},
    'Auftragsbestätigungen zählen als geplante Einfuhr, nicht als bereits eingeführt. CSV-Spalten: ': {"en": 'Order confirmations count as planned imports, not as already imported. CSV columns: '},
    'Betrifft mich CBAM?': {"en": 'Does CBAM apply to me?'},
    'Demo starten': {"en": 'Start demo'},
    'Entscheidung': {"en": 'Decision'},
    'Ergebnis': {"en": 'Result'},
    'Kosten': {"en": 'Cost'},
    'Laden Sie Ihre Rechnungen. In einer Minute wissen Sie, ob die CO₂-Grenzabgabe der EU Sie trifft, was sie kostet und was jetzt zu tun ist.': {"en": 'Upload your invoices. In one minute you know whether the EU carbon border levy applies to you, what it costs and what to do next.'},
    'Nächste Schritte': {"en": 'Next steps'},
    'Oder eigene Rechnungen hochladen — PDF oder CSV': {"en": 'Or upload your own invoices — PDF or CSV'},
    'Quellen: Verordnung (EU) 2023/956, (EU) 2025/2083, DVO (EU) 2025/2621, Europäische Kommission.': {"en": 'Sources: Regulation (EU) 2023/956, (EU) 2025/2083, Impl. Reg. (EU) 2025/2621, European Commission.'},
    'Strafe je Tonne CO₂ ohne Zulassung — auf alle Emissionen des Jahres.': {"en": 'penalty per tonne of CO₂ without authorisation — on all emissions of the year.'},
    'Waren': {"en": 'Goods'},
    'Was wäre wenn': {"en": 'What if'},
    'Wie prüfen wir uns selbst?': {"en": 'How do we test ourselves?'},
    'pro Jahr. Darunter sind Sie befreit, darüber brauchen Sie eine Zulassung.': {"en": 'per year. Below it you are exempt, above it you need an authorisation.'},
    'von der Rechnung zur Entscheidung. Jede Zahl mit Quelle.': {"en": 'from invoice to decision. Every number with a source.'},
})

T.update({'CBAM-Pflicht seit 1. Jänner 2026': {'en': 'CBAM obligations since 1 January 2026'}})

T.update({
    "Los geht's": {"en": "Let's start"},
    'Befreit': {"en": 'Exempt'},
    'Knapp unter dem Limit': {"en": 'Just below the limit'},
    'Limit überschritten': {"en": 'Limit exceeded'},
    'Geplante Lieferung überschreitet das Limit': {"en": 'Planned delivery exceeds the limit'},
    '+{o:.1f} t über dem Limit': {"en": '+{o:.1f} t over the limit'},
})

T.update({
    'Home': {"en": 'Home'},
    'Prüfen': {"en": 'Check'},
    'Fragen & Antworten': {"en": 'Questions & answers'},
    'Hilfe': {"en": 'Help'},
    'In drei Schritten': {"en": 'In three steps'},
    "So funktioniert's": {"en": 'How it works'},
    'Rechnungen hochladen': {"en": 'Upload invoices'},
    'Ergebnis lesen': {"en": 'Read the result'},
    'Entscheiden': {"en": 'Decide'},
    'PDF oder CSV — oder die Demo starten. Codes, Gewichte und Herkunft werden erkannt.': {"en": 'PDF or CSV — or start the demo. Codes, weights and origin are recognised.'},
    'Welche Waren zählen, wie nah Sie an 50 t sind und was es kosten würde.': {"en": 'Which goods count, how close you are to 50 t and what it would cost.'},
    'Unter 50 t bleiben, Zulassung beantragen oder echte Daten beim Lieferanten anfragen — mit fertigen Dokumenten.': {"en": 'Stay below 50 t, apply for authorisation or ask your supplier for real data — with ready-made documents.'},
    'Was ist CBAM?': {"en": 'What is CBAM?'},
    'Betrifft mich das?': {"en": 'Does it apply to me?'},
    'Ja, wenn Sie pro Kalenderjahr mehr als 50 t Waren aus Anhang I einführen — z. B. Träger, Rohre, Schrauben aus Stahl oder Profile aus Aluminium. Alle CBAM-Waren des Jahres werden zusammengezählt. Für Strom und Wasserstoff gibt es keine Schwelle.': {"en": 'Yes, if you import more than 50 t of Annex I goods per calendar year — e.g. steel beams, tubes, screws or aluminium profiles. All CBAM goods of the year are added up. Electricity and hydrogen have no threshold.'},
    'Was kostet es?': {"en": 'What does it cost?'},
    'Pro Tonne Ware: Standardwert der EU (t CO₂ je t Ware) × Preis eines CBAM-Zertifikats des Einfuhrquartals. Zertifikate für Einfuhren 2026 werden ab 1. Februar 2027 verkauft, die erste Jahreserklärung ist bis 30. September 2027 fällig.': {"en": 'Per tonne of goods: EU default value (t CO₂ per t of goods) × price of a CBAM certificate in the import quarter. Certificates for 2026 imports are sold from 1 February 2027; the first annual declaration is due by 30 September 2027.'},
    'Was passiert ohne Zulassung?': {"en": 'What happens without authorisation?'},
    'Wer über 50 t kommt, ohne zugelassener CBAM-Anmelder zu sein, zahlt das 3- bis 5-Fache der Strafe von € 100 je fehlendem Zertifikat — auf alle Emissionen des Jahres, nicht nur auf die Menge über 50 t.': {"en": 'Anyone above 50 t without being an authorised CBAM declarant pays 3 to 5 times the € 100 penalty per missing certificate — on all emissions of the year, not only on the quantity above 50 t.'},
    'Wie beantrage ich die Zulassung?': {"en": 'How do I apply for authorisation?'},
    'In Österreich beim Amt für den nationalen Emissionszertifikatehandel (AnEH), cbam@bmf.gv.at, über das CBAM-Register der EU — bevor Sie die Schwelle überschreiten. Die Checkliste dafür finden Sie unter „Prüfen“ → „Nächste Schritte“.': {"en": 'In Austria with the Amt für den nationalen Emissionszertifikatehandel (AnEH), cbam@bmf.gv.at, through the EU CBAM Registry — before you exceed the threshold. The checklist is under “Check” → “Next steps”.'},
    'Woher kommen die Zahlen?': {"en": 'Where do the numbers come from?'},
    'Aus Anhang I der Verordnung (EU) 2023/956, dem CBAM-Omnibus (EU) 2025/2083, den Standardwerten der DVO (EU) 2025/2621 und den Zertifikatspreisen der Europäischen Kommission. Die KI liest nur Rechnungen und erklärt — gerechnet wird mit geprüftem Code.': {"en": "From Annex I of Regulation (EU) 2023/956, the CBAM Omnibus (EU) 2025/2083, the default values of Implementing Regulation (EU) 2025/2621 and the European Commission's certificate prices. The AI only reads invoices and explains — the calculations are tested code."},
    'Werden meine Rechnungen gespeichert?': {"en": 'Are my invoices stored?'},
    'Nein, wir legen sie in keiner Datenbank ab; sie werden nur für die Berechnung verarbeitet. Stellen Sie der KI eine Frage, werden Ihre Positionen dafür an Google Gemini gesendet.': {"en": 'No, we keep them in no database; they are only processed for the calculation. If you ask the AI a question, your line items are sent to Google Gemini for that.'},
    'Ist das Rechtsberatung?': {"en": 'Is this legal advice?'},
    'Nein. CBAM Helper ist eine Ersteinschätzung und bereitet Unterlagen vor. Die Entscheidung treffen Sie bzw. die Behörde.': {"en": "No. CBAM Helper is a first assessment and prepares documents. The decision is yours and the authority's."},
})

T.update({
    "Eigene Rechnungen prüfen": {"en": "Check my own invoices"},
    "Beispiel ansehen – 30 Sekunden": {"en": "See an example – 30 seconds"},
    "Kostenlos · ohne Anmeldung · Ihre Rechnungen werden nicht gespeichert": {"en": "Free · no sign-up · your invoices are not stored"},
    "Ihr nächster Schritt": {"en": "Your next step"},
    "Zulassung beantragen, bevor die Ware kommt": {"en": "Apply for authorisation before the goods arrive"},
    "Ohne Zulassung drohen Strafen auf alle Emissionen des Jahres. Die Checkliste zeigt Schritt für Schritt, was das AnEH braucht.": {"en": "Without authorisation, penalties apply to all emissions of the year. The checklist shows step by step what the AnEH needs."},
    "Lieferanten nach echten Emissionsdaten fragen": {"en": "Ask your supplier for actual emissions data"},
    "Sie sind knapp unter 50 t. Echte Daten sind oft niedriger als die EU-Standardwerte — der fertige Brief spart Ihnen die Formulierung.": {"en": "You are just under 50 t. Actual data is often lower than the EU default values — the ready-made letter saves you the wording."},
    "Befreiung dokumentieren": {"en": "Document your exemption"},
    "Laden Sie den Bericht mit Quellen herunter — so können Sie jederzeit belegen, warum Sie befreit sind.": {"en": "Download the report with sources — so you can always show why you are exempt."},
    "Checkliste öffnen": {"en": "Open checklist"},
    "Checkliste für die Zulassung": {"en": "Checklist for authorisation"},
    "Brief erstellen": {"en": "Create letter"},
    "Brief an Ihren Lieferanten": {"en": "Letter to your supplier"},
    "Lieferant": {"en": "Supplier"},
})

T.update({
    "Eigene Rechnungen hochladen — PDF oder CSV": {"en": "Upload your invoices — PDF or CSV"},
    "Laden Sie Ihre Rechnungen hoch — das Ergebnis erscheint dann hier.": {"en": "Upload your invoices — the result will appear here."},
})

T.update({
    "PDF oder CSV — oder erst das Beispiel ansehen. Codes, Gewichte und Herkunft werden erkannt.": {"en": "PDF or CSV — or look at the example first. Codes, weights and origin are recognised."},
})

T.update({
    "{f} wird mit KI gelesen …": {"en": "Reading {f} with AI …"},
    "{f}: per KI gelesen — bitte Codes und Gewichte unten prüfen.": {"en": "{f}: read by AI — please check codes and weights below."},
    "{f}: konnte nicht gelesen werden. Bitte als CSV hochladen oder Positionen unten von Hand eintragen.":
        {"en": "{f}: could not be read. Please upload it as CSV or enter the items below by hand."},
})

T.update({
    "nicht berechenbar": {"en": "cannot be calculated"},
    "mind. {v}": {"en": "at least {v}"},
    "Für einige Positionen ({c}) gibt es keinen EU-Standardwert (nur Eisen/Stahl und Aluminium sind hinterlegt). Die Menge zählt für die 50-t-Schwelle, die Kosten können wir dafür nicht schätzen.":
        {"en": "Some items ({c}) have no EU default value (only iron/steel and aluminium are included). The quantity counts towards the 50 t threshold, but we cannot estimate its cost."},
})

T.update({
    "Strafe 3–5 × € 100 je Tonne CO₂ (Art. 26 Abs. 2a VO 2023/956), auf alle Emissionen des Jahres. Deshalb eine Spanne: Den genauen Betrag legt die Behörde (AnEH) fest — je nach Dauer, Schwere und Vorsatz. Die € 100 werden zusätzlich an die Inflation angepasst, die echte Strafe kann also etwas höher sein.":
        {"en": "Fine of 3–5 × €100 per tonne of CO₂ (Art. 26(2a) Reg. 2023/956), on all emissions of the year. That is why it is a range: the authority (AnEH) sets the exact amount depending on duration, gravity and intent. The €100 is also adjusted for inflation, so the real fine can be somewhat higher."},
})

T.update({
    "Größer als der Schwellenwert (+{o:.1f} t).": {"en": "Above the threshold (+{o:.1f} t)."},
})

T.update({
    "Für {y} geht diese Option nicht mehr — es zählen alle Einfuhren des Jahres. Ab {n} beginnt die Zählung neu: Einkäufe früh planen, dann reicht vielleicht wieder die Befreiung.":
        {"en": "For {y} this option is no longer possible — all imports of the year count. From {n} the count starts again: plan purchases early and the exemption may be enough again."},
})

def tr(text, lang, **kw):
    """Translate a German UI text and fill its {placeholders}."""
    s = T.get(text, {}).get(lang, text)
    return s.format(**kw) if kw else s
