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


def tr(text, lang, **kw):
    """Translate a German UI text and fill its {placeholders}."""
    s = T.get(text, {}).get(lang, text)
    return s.format(**kw) if kw else s
