<a name="Русский"></a>

# LLM Book Rewriter (Переписчик Книг с Помощью LLM)

[Go to English](#english)

## 📖 Описание

Эта программа предназначена для помощи авторам, редакторам или **читателям** в пакетной обработке текстов книг с использованием больших языковых моделей (LLM). Она автоматизирует процесс применения изменений (например, исправление ошибок, стилизация, перефразирование) к большим текстовым файлам, разбивая их на управляемые фрагменты, обрабатывая каждый фрагмент через LLM и собирая результат обратно. Например, читатель может скачать купленную книгу в FB2, исправить в ней ошибки с помощью программы и комфортно читать.

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
5.  **Кеш:** Во время обработки создается папка `book_temp`, содержащая подпапки для каждой книги с обработанными фрагментами (`chunkXXXXX.txt`). Если процесс прервется, при следующем запуске программа прочитает эти файлы и продолжит с того места, где остановилась.
6.  **Сброс кеша:** Если вы хотите начать обработку книги заново (например, после изменения промпта или настроек), удалите соответствующую подпапку внутри `book_temp` (например, `book_temp/my_book_name/`).

## 🔧 Устранение Неполадок

*   **`RESOURCE_EXHAUSTED` (Ошибка 429 в логах):** Слишком много одновременных запросов к API, **или** исчерпан дневной лимит бесплатных запросов (или закончились средства на балансе при платном использовании). Уменьшите значение `processing.workers_amount` в `config.yaml` или подождите следующего дня/пополните баланс.
*   **Сообщения о блокировке от Google (Filter):** Сработал фильтр безопасности Google Gemini. См. раздел "Важные Замечания". Попробуйте изменить промпт, использовать другую модель или провайдера (OpenRouter).
*   **`ValidationFailedError`:** LLM изменила количество тегов `<` или `>`. Часто случается, если эвристика `replace_tags_with_placeholder` отключена для FB2/DOCX, или если LLM добавила/удалила символ-плейсхолдер при включенной эвристике. Иногда случается, обычно со второй попытки модель справляется. Убедитесь, что эвристика включена для FB2/DOCX и промпт содержит четкую инструкцию сохранять теги/плейсхолдеры.
*   **Медленная обработка:** Увеличьте `processing.workers_amount` (осторожно!) или `processing.chunk_size`. Используйте более быстрые модели (Flash вместо Pro).

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле `LICENSE`.

---

<a name="english"></a>

# LLM Book Rewriter

[Go to Русский](#русский)

## 📖 Description

This program is designed to assist authors, editors, or **readers** in batch processing book texts using large language models (LLMs). It automates the process of applying changes (e.g., error correction, stylization, paraphrasing) to large text files by splitting them into manageable chunks, processing each chunk via an LLM, and reassembling the result. For instance, a reader can download a purchased book in FB2 format, fix errors using this program, and then read it comfortably.

**Key Features:**

*   **Chunking:** Splits large texts into chunks of a specified size, attempting to respect sentence or tag boundaries.
*   **LLM Integration:** Supports Google Gemini and OpenRouter as LLM providers.
*   **Asynchronous Processing:** Uses `asyncio` for parallel chunk processing, significantly speeding up the workflow.
*   **Customizable Prompt:** Allows the user to precisely instruct the LLM on the changes needed in the text.
*   **Format Support:** Works with `.fb2`, `.txt`, and `.docx` files.
*   **Heuristics:** Applies optional pre- and post-processing heuristics to improve processing quality.
*   **State Persistence:** Caches processed chunks, allowing work to be resumed after interruption without losing progress.
*   **Error Handling & Retries:** Can handle API errors (like rate limits) and automatically retry failed chunk processing attempts.
*   **Tag Validation:** Checks that the LLM hasn't added or removed tags in formats where they are critical (`fb2`, `docx`).
*   **Formatting Preservation:** Attempts to preserve original whitespace around text and tags when formatting the LLM's response.

## 📦 Supported Formats

*   **FB2:** Extracts the content of the `<body>` tag, processes it, and replaces the original body with the processed text. (Uses the `lxml` library for XML parsing).
*   **TXT:** Reads the entire file as plain text, processes it, and writes the result to a new file.
*   **DOCX:** Processes text run-by-run, inserting temporary `<RUN/>` tags for tracking. After LLM processing, it replaces the text in the corresponding runs. (Uses the `python-docx` library).

*(Note: Library mentions are for information; users don't need to install them separately if using the compiled version).*

## 🔑 API Keys and LLM Providers

The program supports two LLM providers:

1.  **Google Gemini:**
    *   **Getting a Key:**
        1.  Go to: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
        2.  Follow Google's instructions to create and obtain your API key.
    *   **Models (examples):** `models/gemini-2.0-flash`, `models/gemini-2.5-pro-exp-03-25`.
    *   **Free Limits (approximate):**
        *   `models/gemini-2.0-flash`: ~1500 requests per day.
        *   `models/gemini-2.5-pro-exp-03-25`: ~25 requests per day.
2.  **OpenRouter:**
    *   **Getting a Key:** Sign up at [OpenRouter.ai](https://openrouter.ai/) and get an API key.
    *   **Models (examples):** `deepseek/deepseek-chat-v3-0324:free`, `google/gemini-flash-1.5`. OpenRouter provides access to numerous models, including free tiers.
    *   **Free Limits (approximate):** ~50 requests per day for models in the "Free" category.

## ❗ Important Notes

*   **API Access:** Access to the Google Gemini API is currently **blocked in the Russian Federation**. Stable operation might require connecting from other regions (e.g., **the Netherlands** works well). OpenRouter can serve as an alternative.
*   **Data Privacy (Google):** When making requests from countries in the European Economic Area (EEA), Switzerland, or the United Kingdom, Google, in accordance with its policy, **does not use your data to train models.**
*   **Content Filters (Google Gemini):** Gemini models have built-in safety filters. Sometimes they can be **overly aggressive**, blocking harmless text chunks. If you encounter frequent blocks, try simplifying the prompt, using a less strict model (Flash), or switching to OpenRouter, where filtering policies might differ.
*   **Google Docs Change Tracking (for DOCX):** If you want to compare the original `.docx` and the processed file using Google Docs' "Compare documents" feature, the standard method (uploading both) might not show changes correctly. For reliable comparison:
    1.  Upload the *original* file (`.docx`) to Google Docs.
    2.  **Download** it back from Google Docs as a `.docx` file. This downloaded file will be your "base" version for comparison.
    3.  Upload the file processed by the script (`_rewritten.docx`).
    4.  Use "Tools" -> "Compare documents", selecting the file downloaded in step 2 as the base and the file uploaded in step 3 as the comparison document.

## ⚙️ Configuration

1.  Run the program's executable file (`.exe`). On the first run (or if `config.yaml` is missing), it will be created next to the program with default settings.
2.  Open the `config.yaml` file in a text editor and make the necessary changes:
    *   **`google.api_key` / `openrouter.api_key`:** Paste your API key for the chosen provider within the quotes.
    *   **`processing.provider`:** Specify `google` or `openrouter`.
    *   **`google.model` / `openrouter.model`:** Specify the desired LLM model (see examples above).
    *   **`processing.chunk_size`:** Chunk size in characters. **Recommended: 8000.** Smaller values might improve quality but increase requests and time. Larger values are faster but may reduce quality.
    *   **`processing.workers_amount`:** Number of concurrent API requests. Higher values **potentially increase processing speed**. The program is stable at any value, but very high settings can lead to many errors (429 - rate limit) in the console.
        *   For "slow" models (e.g., `gemini-2.5-pro-exp-03-25`): recommend **1**.
        *   For "fast" models (e.g., `gemini-2.0-flash`): recommend **10-20**.
    *   **`processing.number_of_passes`:** How many times each chunk is processed. In the current version, values greater than 1 are **practically useless**. Keep it at **1**.
    *   **`processing.output_dir`:** Folder for saving processed files (e.g., `"output_books"`).
    *   **`processing.retry_if_failed`:** `True` (recommended) to retry processing a chunk on error, `False` to skip the chunk (keep original content).
    *   **`prompt`:** **A crucial parameter.** This is the instruction given to the LLM.
        *   Edit the prompt text to match your specific task (error correction, rewriting, stylization, etc.).
        *   The prompt must include the placeholder `{text_chunk}`, which will be replaced with the text fragment.
        *   **Important:** The default prompt is in Russian. If you are processing text in another language, **translate the entire prompt into that language**, including the instructions about preserving tags and whitespace. LLM quality heavily depends on the language and clarity of the instructions.
    *   **`heuristics`:** Heuristic settings (see below). Enable/disable by setting `True` or `False`.

## ✨ Heuristics

Heuristics are optional text transformations applied *before* sending to the LLM (preprocessing) and *after* receiving the response (postprocessing), designed to **improve processing quality**. Configure them in the `config.yaml` file under the `heuristics` section.

*   **`remove_commas` (Preprocessing, 1st pass only):**
    *   **What it does:** Removes all commas from the chunk *before* sending it to the LLM (only on the first pass if `number_of_passes: 1`).
    *   **When to use:** Can improve results if the original text has **many unnecessary or misplaced commas**, and you want the model to repunctuate from scratch. **Recommended for strong models** (e.g., `gemini-2.5-pro-exp-03-25`) that are better at restoring punctuation.
    *   **Caveats:** Weaker models might fail to reinsert commas correctly or at all.
*   **`replace_tags_with_placeholder` (Preprocessing + Postprocessing):**
    *   **What it does:**
        *   *Preprocessing:* Finds all tags like `<...>` (e.g., `<p>`, `</emphasis>`, `<RUN123/>`) and replaces them with special placeholder symbols (e.g., `@`, `#`, `$`). Information about the replaced tags is stored.
        *   *Postprocessing:* After getting the response from the LLM, replaces the placeholders back with the original tags in the correct order.
    *   **When to use:** **Strongly recommended for FB2 and DOCX formats.** LLMs often struggle with preserving HTML/XML-like tags. This heuristic "hides" the tags from the LLM. **Weak models (especially local ones, not used here) might not function correctly with tagged formats without this heuristic.**
    *   **Caveats:** If the LLM deletes or adds a placeholder symbol in the text, tag restoration will fail, and validation (`validate_response`) will likely fail.

## 🚀 Running

1.  Place your books (`.fb2`, `.txt`, `.docx`) in the same folder as the program executable (`.exe`) and the `config.yaml` file.
2.  Run the `.exe` file.
3.  The program will start processing the found files one by one. You'll see logs in the console.
4.  Processed files will be saved in the folder specified by `processing.output_dir` (default `output_books`), with the suffix `_rewritten` (e.g., `my_book_rewritten.fb2`).
5.  **Cache:** During processing, a `book_temp` directory is created, containing subdirectories for each book with processed chunks (`chunkXXXXX.txt`). If the process is interrupted, the next run will read these files and resume from where it left off.
6.  **Clearing the Cache:** If you want to reprocess a book from scratch (e.g., after changing the prompt or settings), delete the corresponding subdirectory within `book_temp` (e.g., `book_temp/my_book_name/`).

## 🔧 Troubleshooting

*   **`RESOURCE_EXHAUSTED` (Error 429 in logs):** Too many concurrent API requests, **or** the daily free request limit is exhausted (or funds ran out if using a paid plan). Decrease `processing.workers_amount` in `config.yaml`, wait for the next day, or top up your balance.
*   **Messages about blocking from Google (Filter):** Google Gemini's safety filter was triggered. See the "Important Notes" section. Try modifying the prompt, using a different model, or switching providers (OpenRouter).
*   **`ValidationFailedError`:** The LLM changed the number of `<` or `>` tags. Often happens if the `replace_tags_with_placeholder` heuristic is disabled for FB2/DOCX, or if the LLM added/removed a placeholder symbol when the heuristic was enabled. Ensure the heuristic is enabled for FB2/DOCX and the prompt clearly instructs to preserve tags/placeholders.
*   **Slow Processing:** Increase `processing.workers_amount` (cautiously!) or `processing.chunk_size`. Use faster models (Flash instead of Pro).

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.