<a name="Русский"></a>

# LLM Book Rewriter (Переписчик Книг с Помощью LLM)

[Go to English](#english)

## 📖 Описание

Эта программа предназначена для помощи авторам, редакторам или читателям в пакетной обработке текстов книг с использованием больших языковых моделей (LLM). Она автоматизирует процесс применения изменений (например, исправление ошибок, стилизация, перефразирование) к большим текстовым файлам, разбивая их на управляемые фрагменты, обрабатывая каждый фрагмент через LLM и собирая результат обратно. Например, читатель может скачать купленную книгу в FB2, исправить в ней ошибки с помощью программы и комфортно читать.

**Ключевые возможности:**

*   **Обработка фрагментами (Chunking):** Разбивает большие тексты на фрагменты заданного размера, стараясь учитывать границы предложений или тегов.
*   **Интеграция с LLM:** Поддерживает Google Gemini и OpenRouter в качестве провайдеров LLM.
*   **Асинхронная обработка:** Использует `asyncio` для параллельной обработки фрагментов, значительно ускоряя процесс.
*   **Настраиваемый Промпт:** Позволяет пользователю точно указать LLM, какие изменения необходимо внести в текст.
*   **Поддержка форматов:** Работает с файлами `.fb2`, `.txt` и `.docx`.
*   **Эвристики:** Применяет опциональные эвристики до и после обработки LLM для улучшения качества обработки.
*   **Сохранение состояния:** Кеширует обработанные фрагменты, позволяя возобновить работу после прерывания без потери прогресса.
*   **Обработка ошибок и повторы:** Умеет обрабатывать ошибки API (например, лимиты запросов) и автоматически повторять неудачные попытки обработки фрагмента.
*   **Валидация тегов:** Проверяет, что LLM не добавила и не удалила теги в форматах, где они важны (`fb2`, `docx`).
*   **Сохранение форматирования:** Старается сохранить исходные пробельные символы вокруг текста и тегов при форматировании ответа LLM.

## 📦 Поддерживаемые форматы

*   **FB2:** Извлекает содержимое тега `<body>`, обрабатывает его и заменяет исходное тело обработанным текстом. (Использует библиотеку `lxml` для разбора XML).
*   **TXT:** Читает весь файл как простой текст, обрабатывает и записывает результат в новый файл.
*   **DOCX:** Обрабатывает текст по частям (`run`), вставляя временные теги `<RUN/>` для отслеживания. После обработки LLM заменяет текст в соответствующих `run`. (Использует библиотеку `python-docx`).

## 🔑 API Ключи и Провайдеры LLM

Программа поддерживает два провайдера LLM:

1.  **Google Gemini:**
    *   **Получение ключа:**
        1.  Перейдите по ссылке: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
        2.  Следуйте инструкциям Google для создания и получения вашего API-ключа.
    *   **Модели (примеры):** `models/gemini-2.0-flash`, `models/gemini-2.5-pro-exp-03-25`.
    *   **Бесплатные лимиты (примерные):**
        *   `models/gemini-2.0-flash`: ~1500 запросов в день.
        *   `models/gemini-2.5-pro-exp-03-25`: ~25 запросов в день.
2.  **OpenRouter:**
    *   **Получение ключа:** Зарегистрируйтесь на [OpenRouter.ai](https://openrouter.ai/) и получите API-ключ.
    *   **Модели (примеры):** `deepseek/deepseek-chat-v3-0324:free`, `google/gemini-flash-1.5`. OpenRouter предоставляет доступ к множеству моделей, включая бесплатные.
    *   **Бесплатные лимиты (примерные):** ~50 запросов в день на модели из категории "Free".

## ❗ Важные Замечания

*   **Доступ к API:** В **Российской Федерации** доступ к API Google Gemini на данный момент **заблокирован**. В **Нидерландах**, впрочем, всё работает. OpenRouter может служить альтернативой.
*   **Конфиденциальность данных (Google):** При выполнении запросов из стран Европейской экономической зоны (EEA)(**и Нидерланды сюда входят**), Швейцарии или Великобритании, Google в соответствии со своей политикой, **не использует ваши данные для обучения моделей.**
*   **Фильтры контента (Google Gemini):** Модели Gemini имеют встроенные фильтры безопасности. Иногда они могут срабатывать **слишком агрессивно**, блокируя даже безобидные фрагменты текста. Если вы сталкиваетесь с частыми блокировками, попробуйте упростить промпт, использовать менее строгую модель (Flash) или переключиться на OpenRouter, где политика фильтрации может отличаться.
*   **Отслеживание изменений в Google Docs (для DOCX):** Если вы хотите сравнить оригинальный `.docx` и обработанный файл с помощью функции "Сравнить документы" в Google Docs, стандартный способ (загрузить оба) может не показать изменения корректно. Чтобы сравнение работало надежно:
    1.  Загрузите *оригинальный* файл (`.docx`) в Google Docs.
    2.  **Скачайте** его обратно из Google Docs в формате `.docx`. Этот скачанный файл будет вашей "базовой" версией для сравнения.
    3.  Загрузите обработанный программой файл (`_rewritten.docx`).
    4.  Используйте функцию "Инструменты" -> "Сравнить документы", выбрав скачанный на шаге 2 файл в качестве базового и загруженный на шаге 3 файл в качестве сравниваемого.

## ⚙️ Настройка

1.  Положите исполняемый файл программы (`.exe`) в одну папку с config.yaml
2.  Откройте файл `config.yaml` в текстовом редакторе и внесите необходимые изменения:
    *   **`google.api_key` / `openrouter.api_key`:** Вставьте ваш API-ключ для выбранного провайдера в кавычках.
    *   **`processing.provider`:** Укажите `google` или `openrouter`.
    *   **`google.model` / `openrouter.model`:** Укажите желаемую модель LLM (см. примеры выше).
    *   **`processing.chunk_size`:** Размер фрагмента в символах. **Рекомендуемое значение: 8000.** Меньшие значения могут улучшить качество обработки, но увеличат количество запросов и время. Большие значения ускоряют, но могут ухудшить качество.
    *   **`processing.workers_amount`:** Количество одновременных запросов к API. Высокие значения **потенциально увеличивают скорость** обработки. Программа работает стабильно при любых значениях, но слишком высокие могут привести к большому количеству ошибок (Resourse Exhausted) в консоли.
        *   Для "медленных" моделей (например, `gemini-2.5-pro-exp-03-25`): рекомендуется **1-3**.
        *   Для "быстрых" моделей (например, `gemini-2.0-flash`): рекомендуется **10-20**.
    *   **`processing.number_of_passes`:** Сколько раз каждый фрагмент будет обработан LLM. В текущей версии значение больше 1 **практически бесполезно**. Оставьте **1**.
    *   **`processing.output_dir`:** Папка для сохранения обработанных файлов (например, `"output_books"`).
    *   **`processing.retry_if_failed`:** `True` (рекомендуется), чтобы повторять обработку фрагмента при ошибке, `False` - чтобы пропустить фрагмент (оставить оригинальным).
    *   **`processing.docx_merge_runs`:** `True` (рекомендуется), чтобы включить слияние одинаковых 'run'-ов (единица текста в формате docx), `False` - чтобы выключить (оставить исходные).

    **⚠️ Внимание!** Эта функция является **экспериментальной**, но её включение (`True`) **КРАЙНЕ РЕКОМЕНДУЕТСЯ**.

    **Что она делает?** Объединяет соседние участки текста (элементы `<run>` в DOCX), если у них **полностью совпадает форматирование** (шрифт, размер, цвет, стиль и т.д.).

    **Почему это так важно?**
    *   **🚀 Значительно повышает качество и стабильность:** Убирает "шум" из документа, позволяя моделям обрабатывать текст как единое целое.
    *   **💰 Снижает стоимость обработки:** Уменьшает количество служебной информации и общую длину текста, передаваемого модели.

    **Потенциальный недостаток:** Будучи экспериментальной, функция теоретически может привести к потере *некоторых* специфических метаданных(история правок, источник), связанных с границами исходных `<run>`. Однако основное форматирование (цвет, стиль, размер и т.д.) при слиянии **должно сохраняться**, так как объединяются только идентично отформатированные участки.

    **Наглядный пример:**
    Допустим, в документе есть строка "Маша ела кашу". Из-за особенностей форматирования, копирования или конвертации, внутри DOCX она может быть разбита на множество `<run>` (технически это элементы `<w:r>`, но для простоты используем `<RUN>`):
    `<RUN1/>М<RUN2/>АШ</RUN2>А ЕЛА КА<RUN3/>ШУ`

    *   **Без слияния (`False`):** Модель получит нечто вроде `@М@АШ@А ЕЛА КА@ШУ` (утрированно, реальное представление зависит от препроцессинга, но суть в фрагментации).
        *   Это **увеличивает стоимость** из-за избыточных данных/токенов.
        *   Модели **крайне сложно** адекватно обработать такой "рваный" текст. Результат может быть непредсказуемым: буквы переставятся, слова исказятся, текст может "перепрыгнуть" в другой абзац или вовсе исчезнуть.

    *   **Со слиянием (`True`):** Если все эти `<RUN>` имеют одинаковое форматирование, функция объединит их:
        `<RUN/>Маша ела кашу`
        Такой текст модель обрабатывает **корректно, надежно и дешевле**.

    **Вывод:** Несмотря на статус экспериментальной, **настоятельно рекомендуется** оставлять эту опцию включенной (`True`) для большинства задач обработки DOCX-файлов.
    *   **`prompt`:** **Очень важный параметр.** Это инструкция для LLM.
        *   Отредактируйте текст промпта под ваши задачи (исправление ошибок, переписывание, стилизация и т.д.).
        *   Промпт должен содержать плейсхолдер `{text_chunk}`, куда будет подставлен фрагмент текста.
        *   Промпт по умолчанию очень консервативный и стремится свести к нулю изменения авторского стиля, даже при оборотах вроде "скрипя сердцем". Возможно, вы захотите поменять его.
        *   **Важно:** Стандартный промпт на русском языке. Если вы обрабатываете текст на другом языке, **переведите промпт на этот язык**, включая инструкции по сохранению тегов и пробельных символов. Качество работы LLM сильно зависит от языка и четкости инструкций.
    *   **`heuristics`:** Настройки эвристик (см. ниже). Включаются/выключаются установкой `True` или `False`.

## ✨ Эвристики

Эвристики - это опциональные преобразования текста *до* отправки в LLM (preprocessing) и *после* получения ответа (postprocessing), предназначенные для **улучшения качества обработки**. Настраиваются в файле `config.yaml` в секции `heuristics`.

*   **`remove_commas` (Preprocessing, только 1-й проход):**
    *   **Что делает:** Удаляет все запятые из фрагмента *перед* отправкой в LLM (только на первом проходе, если `number_of_passes: 1`).
    *   **Когда использовать:** Может улучшить результат, если в исходном тексте **много лишних или неправильно расставленных запятых**, и вы хотите, чтобы модель расставила их заново "с чистого листа". **Рекомендуется для сильных моделей** (например, `gemini-2.5-pro-exp-03-25`), которые лучше справляются с восстановлением пунктуации.
    *   **Предостережения:** Слабые модели могут не расставить запятые обратно или расставить их неправильно.
*   **`replace_tags_with_placeholder` (Preprocessing + Postprocessing):**
    *   **Что делает:**
        *   *Preprocessing:* Находит все теги вида `<...>` (например, `<p>`, `</emphasis>`, `<RUN123/>`) и заменяет их на специальные символы-плейсхолдеры (например, `@`, `#`, `$`). Информация о замененных тегах сохраняется.
        *   *Postprocessing:* После получения ответа от LLM, заменяет плейсхолдеры обратно на оригинальные теги в том же порядке.
    *   **Когда использовать:** **Настоятельно рекомендуется для форматов FB2 и DOCX.** LLM часто плохо справляются с сохранением HTML/XML-подобных тегов. Эта эвристика "прячет" теги от LLM. **Слабые модели (обычно локальные) без этой эвристики могут вообще не справиться с обработкой тегированных форматов.**
    *   **Предостережения:** Если LLM удалит или добавит символ-плейсхолдер в тексте, восстановление тегов не удастся, и валидация (`validate_response`) скорее всего провалится.

## 🚀 Запуск

1.  Поместите ваши книги (`.fb2`, `.txt`, `.docx`) в одну папку с исполняемым файлом программы (`.exe`) и файлом `config.yaml`.
2.  Запустите `.exe` файл.
3.  Программа начнет обрабатывать найденные файлы один за другим. Вы будете видеть логи процесса в консоли.
4.  Обработанные файлы будут сохранены в папке, указанной в `processing.output_dir` (по умолчанию `output_books`), с суффиксом `_rewritten` (например, `my_book_rewritten.fb2`).
5.  **Кеш:** Во время обработки создается папка `book_temp`, содержащая подпапки для каждой книги с обработанными фрагментами (`chunkXXXXX.txt`). Если процесс прервется, при следующем запуске программа прочитает эти файлы и продолжит с того места, где остановилась. **Опционально**: Откройте в режиме просмотра изменений в Word/Google Docs и проверьте предложенные правки.
6.  **Сброс кеша:** Если вы хотите начать обработку книги заново (например, после изменения промпта или настроек), удалите соответствующую подпапку внутри `book_temp` (например, `book_temp/my_book_name/`).

## 🔧 Устранение Неполадок

*   **`RESOURCE_EXHAUSTED` (Ошибка 429 в логах):** Слишком много одновременных запросов к API, или исчерпан дневной лимит бесплатных запросов, или закончились средства на балансе при платном использовании. Уменьшите значение `processing.workers_amount` в `config.yaml` или подождите следующего дня/пополните баланс.
*   **Сообщения о блокировке от Google (Filter):** Сработал фильтр безопасности Google Gemini. См. раздел "Важные Замечания". Попробуйте изменить промпт, использовать другую модель или провайдера (OpenRouter).
*   **`ValidationFailedError`:** LLM изменила количество тегов `<` или `>`. Часто случается, если эвристика `replace_tags_with_placeholder` отключена для FB2/DOCX, или если LLM добавила/удалила символ-плейсхолдер при включенной эвристике. Иногда случается, обычно со второй попытки модель справляется. Убедитесь, что эвристика включена для FB2/DOCX и промпт содержит четкую инструкцию сохранять теги/плейсхолдеры.
*   **Медленная обработка:** Увеличьте `processing.workers_amount` (осторожно!) или `processing.chunk_size`. Используйте более быстрые модели (Flash вместо Pro).

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле `LICENSE`.

---

<a name="english"></a>

# LLM Book Rewriter

[Go to Русский](#Русский)

## 📖 Description

This program is designed to assist authors, editors, or readers in batch processing book texts using large language models (LLM). It automates the process of applying changes (e.g., error correction, stylization, paraphrasing) to large text files by breaking them down into manageable chunks, processing each chunk via an LLM, and reassembling the result. For example, a reader can download a purchased book in FB2 format, correct errors in it using the program, and read it comfortably.

**Key Features:**

*   **Chunking:** Splits large texts into chunks of a specified size, attempting to respect sentence or tag boundaries.
*   **LLM Integration:** Supports Google Gemini and OpenRouter as LLM providers.
*   **Asynchronous Processing:** Uses `asyncio` for parallel chunk processing, significantly speeding up the process.
*   **Customizable Prompt:** Allows the user to specify exactly what changes the LLM should make to the text.
*   **Format Support:** Works with `.fb2`, `.txt`, and `.docx` files.
*   **Heuristics:** Applies optional heuristics before and after LLM processing to improve output quality.
*   **State Persistence:** Caches processed chunks, allowing work to be resumed after interruption without losing progress.
*   **Error Handling and Retries:** Handles API errors (e.g., rate limits) and automatically retries failed chunk processing attempts.
*   **Tag Validation:** Verifies that the LLM has not added or removed tags in formats where they are important (`fb2`, `docx`).
*   **Formatting Preservation:** Attempts to preserve original whitespace around text and tags when formatting the LLM response.

## 📦 Supported Formats

*   **FB2:** Extracts the content of the `<body>` tag, processes it, and replaces the original body with the processed text. (Uses the `lxml` library for XML parsing).
*   **TXT:** Reads the entire file as plain text, processes it, and writes the result to a new file.
*   **DOCX:** Processes text in parts (`run`), inserting temporary `<RUN/>` tags for tracking. After LLM processing, it replaces the text in the corresponding `run`s. (Uses the `python-docx` library).

## 🔑 API Keys and LLM Providers

The program supports two LLM providers:

1.  **Google Gemini:**
    *   **Getting a Key:**
        1.  Go to the link: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
        2.  Follow Google's instructions to create and obtain your API key.
    *   **Models (examples):** `models/gemini-1.0-pro`, `models/gemini-1.5-flash-latest`.
    *   **Free Tier Limits (approximate):**
        *   `models/gemini-1.5-flash-latest`: ~60 requests per minute (RPM). Limits might vary.
        *   `models/gemini-1.0-pro`: ~2 RPM.
2.  **OpenRouter:**
    *   **Getting a Key:** Register at [OpenRouter.ai](https://openrouter.ai/) and obtain an API key.
    *   **Models (examples):** `google/gemini-flash-1.5`, `anthropic/claude-3-haiku`. OpenRouter provides access to numerous models, including free and paid ones with varying limits.
    *   **Free Tier Limits (approximate):** Varies by model. Check the OpenRouter models page for details on free tier availability and limits.

## ❗ Important Notes

*   **API Access:** Access to the Google Gemini API may be restricted in certain regions (e.g., **Russian Federation** at the time of writing). It is confirmed to work in regions like the **Netherlands**. OpenRouter can serve as an alternative.
*   **Data Privacy (Google):** When making requests from countries in the European Economic Area (EEA) (**including the Netherlands**), Switzerland, or the UK, Google, according to its policy, **does not use your data for model training.** Check Google's current policies for confirmation.
*   **Content Filters (Google Gemini):** Gemini models have built-in safety filters. Sometimes they can be **overly aggressive**, blocking even harmless text fragments. If you encounter frequent blocks (`"finish_reason": "SAFETY"`), try simplifying the prompt, using a different model (Flash often has less strict filtering than Pro), adjusting safety settings if available via the API, or switching to OpenRouter, where filtering policies may differ or be configurable.
*   **Google Docs Change Tracking (for DOCX):** If you want to compare the original `.docx` and the processed file using the 'Compare documents' feature in Google Docs, the standard method (uploading both) might not show changes correctly due to internal differences in how Word and Google Docs handle DOCX structures. For reliable comparison:
    1.  Upload the *original* file (`.docx`) to Google Docs.
    2.  **Download** it back from Google Docs in `.docx` format. This downloaded file will be your "base" version for comparison.
    3.  Upload the file processed by this program (`_rewritten.docx`).
    4.  Use the 'Tools' -> 'Compare documents' feature in Google Docs, selecting the file downloaded in step 2 as the base and the file uploaded in step 3 as the comparison document.

## ⚙️ Configuration

1.  Place the program's executable file (`.exe` or the script) in the same folder as `config.yaml`.
2.  Open the `config.yaml` file in a text editor and make the necessary changes:
    *   **`google.api_key` / `openrouter.api_key`:** Paste your API key for the chosen provider within quotes. Leave empty or remove if not using that provider.
    *   **`processing.provider`:** Specify `google` or `openrouter`.
    *   **`google.model` / `openrouter.model`:** Specify the desired LLM model ID (see examples above or provider documentation).
    *   **`processing.chunk_size`:** Chunk size in characters. **Recommended value: 8000.** Smaller values might improve processing quality (especially for complex prompts) but increase the number of API calls and total time. Larger values speed things up but may decrease quality or hit model context limits.
    *   **`processing.workers_amount`:** Number of concurrent requests to the API. High values **potentially increase processing speed**. The program is stable at any value, but excessively high values can lead to many errors (e.g., `429 Resource Exhausted`, `500 Internal Server Error`) in the console, especially if hitting API rate limits.
        *   For "slow" or rate-limited models (e.g., Gemini Pro free tier): **1-3** is recommended.
        *   For "fast" or higher-limit models (e.g., Gemini Flash, paid tiers): **10-20** or more might work, depending on your specific API limits. Adjust based on observed errors.
    *   **`processing.number_of_passes`:** How many times each chunk will be processed by the LLM. In the current version, a value greater than 1 has **limited practical use** unless specifically designed into the prompt or workflow. Leave it as **1** for standard rewriting.
    *   **`processing.output_dir`:** Folder for saving processed files (e.g., `"output_books"`).
    *   **`processing.retry_if_failed`:** `True` (recommended) to retry processing a chunk on recoverable API errors (like rate limits or temporary server issues), `False` to skip the chunk (leave it original) upon failure.
    *   **`processing.docx_merge_runs`:** `True` (recommended) to enable merging of adjacent identically formatted runs in DOCX files before processing, `False` to disable (process runs as they are).

    **⚠️ Warning!** This feature is **experimental**, but enabling it (`True`) is **HIGHLY RECOMMENDED** for DOCX processing.

    **What it does:** Merges adjacent text segments ( `<w:r>` or "run" elements in DOCX) if their **formatting is completely identical** (font, size, color, bold, italics, etc.).

    **Why is it important?**
    *   **🚀 Significantly improves quality and stability:** Reduces document "noise," allowing the LLM to process text more coherently. Avoids issues caused by excessive fragmentation.
    *   **💰 Reduces processing cost:** Decreases the amount of redundant formatting information and the overall text length sent to the LLM, potentially lowering token usage.

    **Potential drawback:** Being experimental, the feature could theoretically lead to the loss of *some* specific metadata (like detailed edit history or certain complex field information) tied to the original `<w:r>` boundaries. However, the main visual formatting (color, style, size, etc.) **should be preserved** during merging, as only identically formatted runs are combined.

    **Illustrative Example:**
    Suppose a document contains the line "Mary ate porridge". Due to formatting quirks, copy-pasting, or conversion, within the DOCX XML, it might be split into multiple runs:
    `<RUN1>M</RUN1><RUN2>ary</RUN2> ate porr<RUN3>idge</RUN3>`

    *   **Without merging (`False`):** The preprocessor might send something like `@M@ary@ ate porr@idge@` to the LLM (simplified representation; actual output depends on preprocessing, but the core issue is fragmentation).
        *   This **increases cost** due to extra placeholder/tag data.
        *   LLMs often **struggle** to process such fragmented text correctly. The result can be unpredictable: letters might get swapped, words distorted, text might jump paragraphs or disappear entirely.

    *   **With merging (`True`):** If all these runs have identical formatting, the function merges them:
        `<RUN>Mary ate porridge</RUN>`
        The LLM receives coherent text, which it can process **correctly, reliably, and more cheaply**.

    **Conclusion:** Despite its experimental status, it is **strongly recommended** to keep this option enabled (`True`) for most DOCX processing tasks.
    *   **`prompt`:** **A very important parameter.** This is the instruction for the LLM.
        *   Edit the prompt text for your specific tasks (e.g., fix grammar and spelling, rewrite in a different style, summarize).
        *   The prompt must contain the placeholder `{text_chunk}`, where the text fragment will be inserted.
        *   The default Russian prompt is very conservative, aiming to minimize changes to the author's style. You might want to make it more or less assertive depending on your goal.
        *   **Important:** The default prompt is in Russian. If you are processing text in another language (e.g., English), **translate the prompt into that language**, including any instructions about preserving tags (or placeholders if using heuristics) and whitespace. LLM performance heavily depends on the language and clarity of the instructions.
    *   **`heuristics`:** Settings for heuristics (see below). Enabled/disabled by setting `True` or `False`.

## ✨ Heuristics

Heuristics are optional text transformations applied *before* sending to the LLM (preprocessing) and *after* receiving the response (postprocessing), designed to **improve processing quality**. Configured in the `config.yaml` file under the `heuristics` section.

*   **`remove_commas` (Preprocessing, only 1st pass):**
    *   **What it does:** Removes all commas from the chunk *before* sending it to the LLM (only on the first pass if `number_of_passes: 1`).
    *   **When to use:** Can potentially improve results if the original text has **many unnecessary or incorrectly placed commas**, and you want the model to re-punctuate it "from scratch". **Recommended for powerful models** (like `Gemini 1.5 Pro`, `Claude 3 Opus`) that are good at restoring punctuation.
    *   **Caveats:** Weaker models might fail to reinsert commas correctly or at all. Use with caution.
*   **`replace_tags_with_placeholder` (Preprocessing + Postprocessing):**
    *   **What it does:**
        *   *Preprocessing:* Finds all tags like `<...>` (e.g., `<p>`, `</emphasis>`, `<RUN123/>`) and replaces them with unique, simple placeholder symbols (e.g., `@`, `#`, `$`, or more complex unique markers). Information about the replaced tags and their order is stored.
        *   *Postprocessing:* After receiving the response from the LLM, replaces the placeholder symbols back with the original tags in the correct order.
    *   **When to use:** **Strongly recommended for FB2 and DOCX formats.** LLMs often struggle to preserve HTML/XML-like tags correctly. This heuristic effectively "hides" the tags from the LLM. **Weaker models (especially local ones) might completely fail to process tagged formats without this heuristic.**
    *   **Caveats:** If the LLM deletes or adds one of the placeholder symbols in the text, tag restoration will fail, and the tag validation check (`validate_response`) will likely raise an error. The prompt should instruct the LLM to keep these special symbols untouched.

## 🚀 Usage

1.  Place your book files (`.fb2`, `.txt`, `.docx`) in the same folder as the program executable (`.exe` or script) and the `config.yaml` file.
2.  Run the executable (`.exe`) or script (e.g., `python main.py`).
3.  The program will find compatible files in the current directory and start processing them one by one. You will see progress logs in the console, including chunk processing status, retries, and errors.
4.  Processed files will be saved in the folder specified by `processing.output_dir` (default is `output_books`), with the suffix `_rewritten` added to the original filename (e.g., `my_book_rewritten.fb2`).
5.  **Cache:** During processing, a `book_temp` folder is created. Inside, subfolders for each book store the processed chunks (e.g., `chunk00001.txt`, `chunk00002.txt`). If the process is interrupted (e.g., Ctrl+C, system shutdown, error), on the next run for the same book, the program will read these cached files and resume processing only the remaining chunks. **Optional:** After processing, you can open the original and `_rewritten` DOCX files in Word or Google Docs (using the comparison method described in "Important Notes") to review the changes made by the LLM.
6.  **Reset Cache:** If you want to reprocess a book from scratch (e.g., after changing the prompt, model, or other settings), simply delete the corresponding subfolder inside `book_temp` (e.g., delete `book_temp/my_book_name/`). The program will then process all chunks again on the next run.

## 🔧 Troubleshooting

*   **`RESOURCE_EXHAUSTED` (Error 429 in logs):** You are sending too many requests too quickly, exceeding your API rate limit, or you have exhausted your daily/monthly free quota or account balance. Decrease the `processing.workers_amount` in `config.yaml`, wait for the rate limit period to reset (often a minute or a day), or check your account balance/quota.
*   **Google Blocking Messages (Filter/Safety):** Google Gemini's safety filter was triggered (often indicated by `"finish_reason": "SAFETY"` in logs). See the "Important Notes" section regarding Content Filters. Try modifying the prompt to be less likely to trigger filters, use a model known for less aggressive filtering (like Flash), potentially adjust safety settings if the API allows, or switch providers (OpenRouter).
*   **`ValidationFailedError` (or similar tag validation errors):** The LLM modified the number or structure of tags (or placeholders, if using the `replace_tags_with_placeholder` heuristic). This often occurs if the heuristic is disabled for FB2/DOCX, or if the LLM (despite instructions) added/deleted a placeholder symbol. Sometimes it's a transient issue, and a retry (if `retry_if_failed: True`) might succeed. Ensure the heuristic is enabled for FB2/DOCX and the prompt clearly instructs the LLM to preserve tags/placeholders.
*   **Slow Processing:** Increase `processing.workers_amount` (carefully monitor for rate limit errors!) or consider increasing `processing.chunk_size` (trade-off with potential quality decrease). Using faster models (like Gemini Flash instead of Pro, or Haiku instead of Opus) can also significantly speed up processing. Check your network connection as well.
*   **`500 Internal Server Error` (or similar 5xx errors):** This usually indicates a temporary problem on the LLM provider's side. If `retry_if_failed: True`, the program should automatically retry after a delay. If errors persist, check the provider's status page or try again later.

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for details.