<a name="Русский"></a>

# LLM Book Rewriter

[Go to English](#english)

**Точно работает на Windows 10**

**При запуске может показываться предупреждение от Windows Defender, это нормально: он реагирует на всё, что не имеет(платного) сертификата. Нажимайте "Подробнее" -> "Выполнить в любом случае". Программа чиста, вы можете убедиться в этом сами, проверив открытый исходный код.**

## Описание

Эта программа предназначена для помощи авторам, редакторам или читателям в пакетной обработке текстов книг с использованием больших языковых моделей (LLM). Она автоматизирует процесс применения изменений (например, исправление ошибок, стилизация, перефразирование) к большим текстовым файлам, разбивая их на управляемые фрагменты, обрабатывая каждый фрагмент через LLM и собирая результат обратно. Например, читатель может скачать купленную книгу в FB2, исправить в ней ошибки с помощью программы и комфортно читать.

**Ключевые возможности:**

*   **Обработка фрагментами (Chunking):** Разбивает большие тексты на фрагменты заданного размера, стараясь учитывать границы предложений или тегов.
*   **Интеграция с LLM:** Поддерживает Gemini, OpenRouter, YandexGPT, GigaChat (для использования могут потребоваться сертификаты Минцифры), LM Studio (для локальных моделей) и Custom (любой OpenAI-совместимый провайдер с возможностью указания `base_url`) в качестве провайдеров LLM.
*   **Асинхронная обработка:** Использует `asyncio` для параллельной обработки фрагментов, значительно ускоряя процесс.
*   **Настраиваемый промпт:** Позволяет пользователю точно указать LLM, какие изменения необходимо внести в текст.
*   **Поддержка форматов:** Работает с файлами `.fb2`, `.txt` и `.docx`.
*   **Эвристики:** Применяет опциональные эвристики до и после обработки LLM для улучшения качества обработки.
*   **Сохранение состояния:** Кеширует обработанные фрагменты, позволяя возобновить работу после прерывания без потери прогресса.
*   **Обработка ошибок и повторы:** Умеет обрабатывать ошибки API (например, лимиты запросов) и автоматически повторять неудачные попытки обработки фрагмента.
*   **Валидация тегов:** Проверяет, что LLM не добавила и не удалила теги в форматах, где они важны (`fb2`, `docx`).
*   **Сохранение форматирования:** Старается сохранить исходные пробельные символы вокруг текста и тегов при форматировании ответа LLM.

## Краткая инструкция по установке и использованию
1. Перейдите на https://github.com/VaniusK/llm-book-rewriter/releases и скачайте .exe-файл последней версии.
2.  
* Вернитесь на эту страницу и нажмите на зелёную кнопку Code в верхней части страницы, выберите "Download ZIP". Скачайте архив, распакуйте его и файл config.yaml положите в одну папку с .exe. Остальные файлы не понадобятся.
<br/> ИЛИ 
* Перейдите по ссылке https://github.com/VaniusK/llm-book-rewriter/blob/main/config.yaml, скопируйте содержание файла, в одной папке с .exe создайте текстовый документ, вставьте скопированное туда, сохраните. Переименуйте файл в config.yaml.
<br/><br/>**Если есть доступ через ЕЭС, Швейцарию или Великобританию (для Gemini):**
* Перейдите на https://aistudio.google.com/apikey, нажмите на синюю кнопку "Create API key", следуйте инструкциям. Полученный ключ скопируйте в файл config.yaml(открывайте его с помощью, например, блокнота) в поле "gemini: api_key" вместо "YOUR_KEY"(результат должен быть api_key: "XXX"), сохраните изменения.
<br/><br/>**Если доступа к Gemini нет или хотите использовать других провайдеров:**
* **OpenRouter:** Перейдите на https://openrouter.ai/settings/keys, зарегистрируйтесь, нажмите на кнопку "Create key", следуйте инструкциям. Полученный ключ скопируйте в файл config.yaml в поле "openrouter: api_key" вместо "YOUR_KEY".
    * Перейдите на https://openrouter.ai/settings/privacy и включите возможность обучения на ваших данных (без этого бесплатные модели могут не работать).
    * **ВАЖНО (OpenRouter Free):** Как видно из пункта выше, Openrouter в бесплатном режиме собирает данные для обучения моделей. Используйте только для теста. **НЕ ИСПОЛЬЗУЙТЕ НА ВАШИХ КНИГАХ, если конфиденциальность важна.** Рассмотрите Gemini или платные опции OpenRouter.
* **YandexGPT, GigaChat, LM Studio, Custom:** Настройте соответствующие поля в `config.yaml` согласно инструкциям в разделе "API Ключи и Провайдеры LLM" и "Настройка".
3. Положите книгу в одну папку с .exe-файлом, запустите файл. Появится консоль с прогрессом, по окончании обработки консоль закроется, а результат будет лежать в папке output_books. При запуске вычитываются сразу все книги в папке, так что можно обрабатывать несколько за раз.

## Видеоинструкция
**Youtube**
* Общая установка и использование(требует доступ через ЕЭС, ...): https://youtu.be/GadFStZuOmw
* Настройка Openrouter(тоже требует): https://youtu.be/pRmSRbGraZw

**ВК Видео(почему-то не работает)**
* Общая установка и использование(требует доступ через ЕЭС, ...): https://vkvideo.ru/video-182995355_456239017
* Настройка Openrouter(тоже требует): https://vkvideo.ru/video-182995355_456239019

**Гугл диск**
* Общая установка и использование(требует доступ через ЕЭС, ...): https://drive.google.com/file/d/1zsb3cH4vZY4tiW6qOyINpBmlIh8R542U/view?usp=sharing
* Настройка Openrouter(тоже требует): https://drive.google.com/file/d/1st2QqKw-8Vmp3yzVHW3FdtH3zKOhIXo6/view?usp=sharing

## Поддерживаемые форматы

*   **FB2:** Извлекает содержимое тега `<body>`, обрабатывает его и заменяет исходное тело обработанным текстом.
*   **TXT:** Читает весь файл как простой текст, обрабатывает и записывает результат в новый файл.
*   **DOCX:** Обрабатывает текст по частям (`run`), вставляя временные теги `<RUN/>` для отслеживания. После обработки LLM заменяет текст в соответствующих `run`. (Использует библиотеку `python-docx`).

## API Ключи и Провайдеры LLM

Программа поддерживает следующие провайдеры LLM:

1.  **Google Gemini:**
    *   **Получение ключа:**
        1.  Перейдите по ссылке: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
        2.  Следуйте инструкциям для создания и получения вашего API-ключа.
    *   **Модели (примеры):** `gemini-3.1-pro-preview`, `gemma-4-31b-it`.
2.  **OpenRouter:**
    *   **Получение ключа:** Зарегистрируйтесь на [OpenRouter.ai](https://openrouter.ai/) и получите API-ключ.
    *   **Модели (примеры):** `tencent/hy3`, `https://openrouter.ai/google/gemma-4-31b-it:free`. OpenRouter предоставляет доступ к множеству моделей, включая бесплатные.
    *   **Бесплатные лимиты (примерные):** ~50 запросов в день на модели из категории "Free".
3.  **YandexGPT:**
    *   Использует API от Yandex. Потребуется API-ключ.
    *   *Детали по моделям и получению ключа см. в официальной документации Yandex Cloud.*
4.  **GigaChat:**
    *   Использует API от Сбера. Потребуется API-ключ.
    *   **Важно:** Для использования требуются сертификаты Минцифры России.
    *   *Детали по моделям и получению ключа см. в официальной документации GigaChat.*
5.  **LM Studio (Локальные модели):**
    *   Позволяет использовать LLM, запущенные локально через приложение LM Studio.
    *   Обычно требует указания URL локального сервера (например, `http://localhost:1234/v1`) в конфигурации при выборе провайдера `lmstudio` или `custom`.
6.  **Custom (Пользовательский OpenAI-совместимый провайдер):**
    *   Предназначен для подключения к любому LLM-провайдеру, который предоставляет OpenAI-совместимый API.
    *   Требует указания `base_url` (адрес API, например, `https://llm.chutes.ai/v1/`) и, возможно, `api_key` в файле конфигурации.

## Важные Замечания

*   **Доступ к API:** В **Российской Федерации** доступ к API Google Gemini и OpenRouter на данный момент **заблокирован**. В **Нидерландах**, впрочем, всё работает. YandexGPT, GigaChat могут служить альтернативой.
*   **Конфиденциальность данных (Google):** Ознакомьтесь в политикой конфиденциальности используемого провайдера. У Gemini, например, бесплатные запросы из некоторых стран используются для обучения моделей. В Openrouter можно в настройках приватности можно включить только провайдеров, которые не используют ваши данные.
*   **Отслеживание изменений в Google Docs (для DOCX):** Если вы хотите сравнить оригинальный `.docx` и обработанный файл с помощью функции "Сравнить документы" в Gemini Docs, стандартный способ (загрузить оба) может не показать изменения корректно. Чтобы сравнение работало надежно:
    1.  Загрузите *оригинальный* файл (`.docx`) в Google Docs.
    2.  **Скачайте** его обратно из Google Docs в формате `.docx`. Этот скачанный файл будет вашей "базовой" версией для сравнения.
    3.  Загрузите обработанный программой файл (`_rewritten.docx`).
    4.  Используйте функцию "Инструменты" -> "Сравнить документы", выбрав скачанный на шаге 2 файл в качестве базового и загруженный на шаге 3 файл в качестве сравниваемого.

## Настройка

1.  Положите исполняемый файл программы (`.exe`) в одну папку с config.yaml
2.  Откройте файл `config.yaml` в текстовом редакторе и внесите необходимые изменения:
    *   **Ключи API и специфичные параметры провайдеров:**
        *   **`google.api_key`, `openrouter.api_key`, `yandexgpt.api_key`, `gigachat.api_key`, `custom.api_key`:** Вставьте ваш API-ключ для соответствующего провайдера в кавычках. Для некоторых провайдеров (например, LM Studio, если используется без ключа) ключ может не требоваться.
        *   **`custom.base_url`:** Если `processing.provider` установлен в `custom`, укажите здесь базовый URL API вашего провайдера (например, `"https://api.example.com/v1/"`).
        *   **`lmstudio.base_url` (или аналогичный параметр, если `lmstudio` выбран как провайдер):** Если `processing.provider` установлен в `lmstudio`, здесь может указываться URL вашего локального сервера LM Studio (например, `"http://localhost:1234/v1"`). LM Studio также можно использовать через провайдер `custom`, указав его `base_url`.
    *   **`processing.provider`:** Укажите одного из поддерживаемых провайдеров: `google`, `openrouter`, `yandexgpt`, `gigachat`, `lmstudio` или `custom`.
    *   **Модели LLM для провайдеров:**
        *   **`google.model`, `openrouter.model`, `yandexgpt.model`, `gigachat.model`, `custom.model`, `lmstudio.model`:** Укажите желаемую модель LLM для выбранного провайдера (см. документацию провайдера или примеры выше для Gemini/OpenRouter). Для LM Studio это может быть имя модели, загруженной на локальном сервере.
    *   **`processing.chunk_size`:** Размер фрагмента в символах. **Рекомендуемое значение: 8000.** Меньшие значения могут улучшить качество обработки, но увеличат количество запросов и время. Большие значения ускоряют, но могут ухудшить качество.
    *   **`processing.workers_amount`:** Количество одновременных запросов к API. Высокие значения **потенциально увеличивают скорость** обработки. Программа работает стабильно при любых значениях, но слишком высокие могут привести к большему количеству ошибок (Resourse Exhausted) в консоли. Смотрите максимальное количество параллельных запросов у провайдера.
    *   **`processing.number_of_passes`:** Сколько раз каждый фрагмент будет обработан LLM. В текущей версии значение больше 1 **практически бесполезно**. Оставьте **1**.
    *   **`processing.output_dir`:** Папка для сохранения обработанных файлов (например, `"output_books"`).
    *   **`processing.number_of_retries`:** Сколько раз пытаться обработать чанк при ошибке. Ошибки иногда случаются(отвалился интернет, ошибка на стороне провайдера, превышен лимит параллельных запросов и так далее), так что рекомендуется значение 3-5. Если чанк не удалось обработать, используется оригинальный текст
    *   **`processing.docx_merge_runs`:** `True` (рекомендуется), чтобы включить слияние одинаковых 'run'-ов (единица текста в формате docx), `False` - чтобы выключить (оставить исходные).

    **Внимание!** Эта функция является **экспериментальной**, но её включение (`True`) **КРАЙНЕ РЕКОМЕНДУЕТСЯ**.

    **Что она делает?** Объединяет соседние участки текста (элементы `<run>` в DOCX), если у них **полностью совпадает форматирование** (шрифт, размер, цвет, стиль и т.д.).

    **Почему это так важно?**
    *   **Значительно повышает качество и стабильность:** Убирает "шум" из документа, позволяя моделям обрабатывать текст как единое целое.
    *   **Снижает стоимость обработки:** Уменьшает количество служебной информации и общую длину текста, передаваемого модели.

    **Потенциальный недостаток:** Будучи экспериментальной, функция теоретически может привести к потере *некоторых* специфических метаданных(история правок, источник), связанных с границами исходных `<run>`. Однако основное форматирование (цвет, стиль, размер и т.д.) при слиянии **должно сохраняться**, так как объединяются только идентично отформатированные участки.

    **Наглядный пример:**
    Допустим, в документе есть строка "Маша ела кашу". Из-за особенностей форматирования, копирования или конвертации, внутри DOCX она может быть разбита на множество `<run>` (технически это элементы `<w:r>`, но для простоты используем `<RUN>`):
    `<RUN1/>М<RUN2/>АШ</RUN3/>А ЕЛА КА<RUN4/>ШУ`

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
        *   Промпт по умолчанию очень консервативный и стремится привести все результаты к одному виду для удобства проверки. Возможно, вы захотите поменять его.
        *   **Важно:** Стандартный промпт на русском языке. Если вы обрабатываете текст на другом языке, **переведите промпт на этот язык**, включая инструкции по сохранению тегов и пробельных символов. Качество работы LLM сильно зависит от языка и четкости инструкций.
    *   **`heuristics`:** Настройки эвристик (см. ниже). Включаются/выключаются установкой `True` или `False`.

## Эвристики

Эвристики - это опциональные преобразования текста *до* отправки в LLM (preprocessing) и *после* получения ответа (postprocessing), предназначенные для **улучшения качества обработки**. Настраиваются в файле `config.yaml` в секции `heuristics`.

*   **`remove_commas` (Preprocessing, только 1-й проход):**
    *   **Что делает:** Удаляет все запятые из фрагмента *перед* отправкой в LLM.
    *   **Когда использовать:** Когда в книге много неправильных запятых, а вам нужно быстро получить удовлетворительный результат.
    *   **Предостережения:** В некоторых случаях("Казнить нельзя помиловать") после удаления запятых модель не может восстановить изначальный смысл. Если для вас это важно, рекомендуется проверять изменения. 
*   **`replace_tags_with_placeholder` (Preprocessing + Postprocessing):**
    *   **Что делает:**
        *   *Preprocessing:* Находит все теги вида `<...>` (например, `<p>`, `</emphasis>`, `<RUN123/>`) и заменяет их на специальные символы-плейсхолдеры (например, `@`, `#`, `$`). Информация о замененных тегах сохраняется.
        *   *Postprocessing:* После получения ответа от LLM, заменяет плейсхолдеры обратно на оригинальные теги в том же порядке.
    *   **Когда использовать:** **Настоятельно рекомендуется для форматов FB2 и DOCX.** LLM часто плохо справляются с сохранением HTML/XML-подобных тегов(например, пытаются закрыть открытый тег, хотя он должен закрываться в другом чанке). Эта эвристика "прячет" теги от LLM.
    *   **Предостережения:** Если LLM удалит или добавит символ-плейсхолдер в тексте, восстановление тегов не удастся, и валидация (`validate_response`) скорее всего провалится.
*   **`remove_thinking` (Postprocessing):**
    *   **Что делает:** Вырезает из ответа LLM специальные теги `<think>` и `</think>` вместе с их содержимым. Некоторые модели (особенно те, что следуют техникам Chain-of-Thought или аналогичным) могут включать свои "рассуждения" или промежуточные шаги в вывод, оборачивая их в такие теги.
    *   **Когда использовать:** Включите эту эвристику, если ваша LLM добавляет в ответ текст вида `<think>...рассуждения...</think>`, который не должен попадать в финальный обработанный текст книги. Это помогает очистить вывод модели от служебной информации.
    *   **Предостережения:** Убедитесь, что теги `<think>` и `</think>` используются моделью именно для обозначения удаляемых рассуждений, а не для чего-то другого, что должно остаться в тексте.

## Запуск

1.  Поместите ваши книги (`.fb2`, `.txt`, `.docx`) в одну папку с исполняемым файлом программы (`.exe`) и файлом `config.yaml`.
2.  Запустите `.exe` файл.
3.  Программа начнет обрабатывать найденные файлы один за другим. Вы будете видеть логи процесса в консоли.
4.  Обработанные файлы будут сохранены в папке, указанной в `processing.output_dir` (по умолчанию `output_books`), с суффиксом `_rewritten` (например, `my_book_rewritten.fb2`).
5.  **Кеш:** Во время обработки создается папка `book_temp`, содержащая подпапки для каждой книги с обработанными фрагментами (`chunkXXXXX.txt`). Если процесс прервется, при следующем запуске программа прочитает эти файлы и продолжит с того места, где остановилась. **Опционально**: Откройте в режиме просмотра изменений в Word/Google Docs и проверьте предложенные правки.
6.  **Сброс кеша:** Если вы хотите начать обработку книги заново (например, после изменения промпта или настроек), удалите соответствующую подпапку внутри `book_temp` (например, `book_temp/my_book_name/`).

## Устранение Неполадок

*   **`RESOURCE_EXHAUSTED` (Ошибка 429 в логах):** Слишком много одновременных запросов к API, или исчерпан дневной лимит бесплатных запросов, или закончились средства на балансе при платном использовании. Уменьшите значение `processing.workers_amount` в `config.yaml` или подождите следующего дня/пополните баланс.
*   **Сообщения о блокировке от Google (Filter):** Сработал фильтр безопасности Google Gemini. См. раздел "Важные Замечания". Попробуйте изменить промпт, использовать другую модель или провайдера (OpenRouter, YandexGPT, GigaChat и т.д.).
*   **`ValidationFailedError`:** LLM изменила количество тегов `<` или `>`. Часто случается, если эвристика `replace_tags_with_placeholder` отключена для FB2/DOCX, или если LLM добавила/удалила символ-плейсхолдер при включенной эвристике. Иногда случается, обычно со второй попытки модель справляется. Убедитесь, что эвристика включена для FB2/DOCX и промпт содержит четкую инструкцию сохранять теги/плейсхолдеры.
*   **Медленная обработка:** Увеличьте `processing.workers_amount` (осторожно!) или `processing.chunk_size`. Используйте более быстрые модели (Flash вместо Pro).

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле `LICENSE`.

---

<a name="english"></a>

# LLM Book Rewriter

[Go to Russian](#Русский)

**Guaranteed to work on Windows 10**

**Windows Defender might show a warning when you run the program, this is normal: it reacts to anything that doesn't have a (paid) certificate. Click "More info" -> "Run anyway". The program is clean, you can verify this yourself by checking the open-source code.**

## Description

This program is designed to help authors, editors, or readers with batch processing of book texts using large language models (LLMs). It automates the process of applying changes (e.g., error correction, stylization, paraphrasing) to large text files by breaking them into manageable chunks, processing each chunk through an LLM, and reassembling the result. For example, a reader can download a purchased book in FB2 format, fix errors in it using the program, and read it comfortably.

**Key Features:**

*   **Chunking:** Splits large texts into chunks of a specified size, trying to respect sentence or tag boundaries.
*   **LLM Integration:** Supports Gemini, OpenRouter, YandexGPT, GigaChat (may require certificates from the Russian Ministry of Digital Development for use), LM Studio (for local models), and Custom (any OpenAI-compatible provider with the ability to specify `base_url`) as LLM providers.
*   **Asynchronous Processing:** Uses `asyncio` for parallel processing of chunks, significantly speeding up the process.
*   **Customizable Prompt:** Allows the user to specify exactly what changes the LLM should make to the text.
*   **Format Support:** Works with `.fb2`, `.txt`, and `.docx` files.
*   **Heuristics:** Applies optional heuristics before and after LLM processing to improve the quality of the output.
*   **State Preservation:** Caches processed chunks, allowing work to be resumed after interruption without losing progress.
*   **Error Handling and Retries:** Can handle API errors (e.g., request limits) and automatically retry failed chunk processing attempts.
*   **Tag Validation:** Verifies that the LLM has not added or removed tags in formats where they are important (`fb2`, `docx`).
*   **Formatting Preservation:** Tries to preserve original whitespace characters around text and tags when formatting the LLM's response.

## Quick Installation and Usage Guide
1. Go to https://github.com/VaniusK/llm-book-rewriter/releases and download the latest version's .exe file.
2.  
* Return to this page and click the green "Code" button at the top of the page, then select "Download ZIP". Download the archive, unzip it, and place the `config.yaml` file in the same folder as the .exe file. The other files will not be needed.
<br/> OR 
* Go to https://github.com/VaniusK/llm-book-rewriter/blob/main/config.yaml, copy the file's content, create a text document in the same folder as the .exe, paste the copied content there, and save it. Rename the file to `config.yaml`.
<br/><br/>**If you have access via the EEA, Switzerland, or the UK (for Gemini):**
* Go to https://aistudio.google.com/apikey, click the blue "Create API key" button, and follow the instructions. Copy the obtained key into the `config.yaml` file (open it with Notepad, for example) in the "gemini: api_key" field, replacing "YOUR_KEY" (the result should be api_key: "XXX"), and save the changes.
<br/><br/>**If you don't have access to Gemini or want to use other providers:**
* **OpenRouter:** Go to https://openrouter.ai/settings/keys, register, click the "Create key" button, and follow the instructions. Copy the obtained key into the `config.yaml` file in the "openrouter: api_key" field, replacing "YOUR_KEY".
    * Go to https://openrouter.ai/settings/privacy and enable data training (free models may not work without this).
    * **IMPORTANT (OpenRouter Free):** As seen in the point above, OpenRouter collects data for model training in its free mode. Use it for testing purposes only. **DO NOT USE IT ON YOUR BOOKS if confidentiality is important.** Consider Gemini or paid OpenRouter options.
* **YandexGPT, GigaChat, LM Studio, Custom:** Configure the respective fields in `config.yaml` according to the instructions in the "API Keys and LLM Providers" and "Configuration" sections.
3. Place your book(s) in the same folder as the .exe file and run the file. A console window will appear showing the progress. Once processing is complete, the console will close, and the result will be in the `output_books` folder. The program reads all books in the folder upon launch, so you can process multiple books at once.

## Video Tutorial
**YouTube**
* General installation and usage (requires access via EEA, ...): https://youtu.be/GadFStZuOmw
* OpenRouter setup (no access restrictions): https://youtu.be/pRmSRbGraZw

**VK Video (doesn't seem to work for some reason)**
* General installation and usage (requires access via EEA, ...): https://vkvideo.ru/video-182995355_456239017
* OpenRouter setup (no access restrictions): https://vkvideo.ru/video-182995355_456239019

**Google Drive**
* General installation and usage (requires access via EEA, ...): https://drive.google.com/file/d/1zsb3cH4vZY4tiW6qOyINpBmlIh8R542U/view?usp=sharing
* OpenRouter setup (no access restrictions): https://drive.google.com/file/d/1st2QqKw-8Vmp3yzVHW3FdtH3zKOhIXo6/view?usp=sharing

## Supported Formats

*   **FB2:** Extracts the content of the `<body>` tag, processes it, and replaces the original body with the processed text.
*   **TXT:** Reads the entire file as plain text, processes it, and writes the result to a new file.
*   **DOCX:** Processes text in parts (`run`), inserting temporary `<RUN/>` tags for tracking. After LLM processing, it replaces the text in the corresponding `run`s. (Uses the `python-docx` library).

## API Keys and LLM Providers

The program supports the following LLM providers:

1.  **Google Gemini:**
    *   **Obtaining a key:**
        1.  Go to the link: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
        2.  Follow the instructions to create and obtain your API key.
    *   **Models (examples):** `models/gemini-2.0-flash`, `models/gemini-2.5-pro-exp-03-25`.
    *   **Free limits (approximate):**
        *   `models/gemini-2.0-flash`: ~1500 requests per day.
        *   `models/gemini-2.5-pro-exp-03-25`: ~25 requests per day.
2.  **OpenRouter:**
    *   **Obtaining a key:** Register on [OpenRouter.ai](https://openrouter.ai/) and get an API key.
    *   **Models (examples):** `deepseek/deepseek-chat-v3-0324:free`, `google/gemini-flash-1.5`. OpenRouter provides access to many models, including free ones.
    *   **Free limits (approximate):** ~50 requests per day for models in the "Free" category.
3.  **YandexGPT:**
    *   Uses the API from Yandex. An API key will be required.
    *   *For details on models and obtaining a key, see the official Yandex Cloud documentation.*
4.  **GigaChat:**
    *   Uses the API from Sber. An API key will be required.
    *   **Important:** Requires certificates from the Russian Ministry of Digital Development for use.
    *   *For details on models and obtaining a key, see the official GigaChat documentation.*
5.  **LM Studio (Local Models):**
    *   Allows using LLMs run locally via the LM Studio application.
    *   Usually requires specifying the local server URL (e.g., `http://localhost:1234/v1`) in the configuration when selecting the `lmstudio` or `custom` provider.
6.  **Custom (User-defined OpenAI-compatible provider):**
    *   Designed for connecting to any LLM provider that offers an OpenAI-compatible API.
    *   Requires specifying `base_url` (API address, e.g., `https://llm.chutes.ai/v1/`) and, optionally, `api_key` in the configuration file.

## Important Notes

*   **API Access:** In the **Russian Federation**, access to the Google Gemini API is currently **blocked**. However, in the **Netherlands**, everything works. OpenRouter, YandexGPT, GigaChat can serve as alternatives.
*   **Data Privacy (Google):** When making requests from European Economic Area (EEA) countries (**including the Netherlands**), Switzerland, or the United Kingdom, Gemini, according to its policy, **does not use your data for model training.** For other providers, please review their privacy policies.
*   **Content Filters (Google Gemini):** Gemini models have built-in safety filters. Sometimes they can be **overly aggressive**, blocking even harmless text fragments. If you encounter frequent blocks, try simplifying the prompt, using a less strict model (Flash), or switching to another provider where the filtering policy may differ.
*   **Tracking Changes in Google Docs (for DOCX):** If you want to compare the original `.docx` and the processed file using the "Compare documents" feature in Google Docs, the standard method (uploading both) might not show changes correctly. For reliable comparison:
    1.  Upload the *original* file (`.docx`) to Google Docs.
    2.  **Download** it back from Google Docs in `.docx` format. This downloaded file will be your "base" version for comparison.
    3.  Upload the file processed by the program (`_rewritten.docx`).
    4.  Use the "Tools" -> "Compare documents" function, selecting the file downloaded in step 2 as the base and the file uploaded in step 3 as the one to compare.

## Configuration

1.  Place the program's executable file (`.exe`) in the same folder as `config.yaml`.
2.  Open the `config.yaml` file in a text editor and make the necessary changes:
    *   **API Keys and provider-specific parameters:**
        *   **`google.api_key`, `openrouter.api_key`, `yandexgpt.api_key`, `gigachat.api_key`, `custom.api_key`:** Insert your API key for the respective provider in quotes. For some providers (e.g., LM Studio, if used without a key), a key may not be required.
        *   **`custom.base_url`:** If `processing.provider` is set to `custom`, specify your provider's API base URL here (e.g., `"https://api.example.com/v1/"`).
        *   **`lmstudio.base_url` (or a similar parameter if `lmstudio` is selected as the provider):** If `processing.provider` is set to `lmstudio`, this is where you might specify your local LM Studio server URL (e.g., `"http://localhost:1234/v1"`). LM Studio can also be used via the `custom` provider by specifying its `base_url`.
    *   **`processing.provider`:** Specify one of the supported providers: `google`, `openrouter`, `yandexgpt`, `gigachat`, `lmstudio`, or `custom`.
    *   **LLM Models for providers:**
        *   **`google.model`, `openrouter.model`, `yandexgpt.model`, `gigachat.model`, `custom.model`, `lmstudio.model`:** Specify the desired LLM model for the selected provider (see provider documentation or examples above for Gemini/OpenRouter). For LM Studio, this could be the name of the model loaded on the local server.
    *   **`processing.chunk_size`:** Chunk size in characters. **Recommended value: 8000.** Smaller values may improve processing quality but will increase the number of requests and time. Larger values speed things up but may degrade quality.
    *   **`processing.workers_amount`:** Number of concurrent API requests. High values **can potentially increase processing speed**. The program is stable at any value, but excessively high values can lead to a large number of errors (Resource Exhausted) in the console.
        *   For "slow" models (e.g., `gemini-2.5-pro-exp-03-25`): **1-3** is recommended.
        *   For "fast" models (e.g., `gemini-2.0-flash`): **3-5** is recommended.
    *   **`processing.number_of_passes`:** How many times each chunk will be processed by the LLM. In the current version, a value greater than 1 is **practically useless**. Leave it at **1**.
    *   **`processing.output_dir`:** Folder for saving processed files (e.g., `"output_books"`).
    *   **`processing.retry_if_failed`:** `True` (recommended) to retry processing a chunk on error, `False` to skip the chunk (leave it original).
    *   **`processing.docx_merge_runs`:** `True` (recommended) to enable merging of identical 'runs' (a unit of text in docx format), `False` to disable (keep original).

    **Attention!** This feature is **experimental**, but enabling it (`True`) is **HIGHLY RECOMMENDED**.

    **What it does:** Merges adjacent text sections ( `<run>` elements in DOCX) if they have **completely identical formatting** (font, size, color, style, etc.).

    **Why is this so important?**
    *   **Significantly improves quality and stability:** Removes "noise" from the document, allowing models to process text as a single unit.
    *   **Reduces processing cost:** Decreases the amount of auxiliary information and the total length of text sent to the model.

    **Potential drawback:** Being experimental, the function could theoretically lead to the loss of *some* specific metadata (revision history, source) associated with the boundaries of the original `<run>`s. However, basic formatting (color, style, size, etc.) **should be preserved** during merging, as only identically formatted sections are combined.

    **Illustrative example:**
    Suppose a document contains the line "Mary ate porridge." Due to formatting peculiarities, copying, or conversion, within the DOCX it might be split into multiple `<run>`s (technically these are `<w:r>` elements, but we use `<RUN>` for simplicity):
    `<RUN1/>M<RUN2/>AR</RUN3/>Y ATE POR<RUN4/>RIDGE`

    *   **Without merging (`False`):** The model will receive something like `@M@AR@Y ATE POR@RIDGE` (simplified, the actual representation depends on preprocessing, but the point is fragmentation).
        *   This **increases cost** due to redundant data/tokens.
        *   Models find it **extremely difficult** to adequately process such "torn" text. The result can be unpredictable: letters might be rearranged, words distorted, text might "jump" to another paragraph, or even disappear entirely.

    *   **With merging (`True`):** If all these `<RUN>`s have identical formatting, the function will merge them:
        `<RUN/>Mary ate porridge`
        Such text is processed by the model **correctly, reliably, and more cheaply**.

    **Conclusion:** Despite its experimental status, it is **strongly recommended** to keep this option enabled (`True`) for most DOCX file processing tasks.
    *   **`prompt`:** **A very important parameter.** This is the instruction for the LLM.
        *   Edit the prompt text for your specific tasks (error correction, rewriting, stylization, etc.).
        *   The prompt must contain the placeholder `{text_chunk}`, where the text chunk will be inserted.
        *   The default prompt is very conservative and aims to minimize changes to the author's style, even with idiomatic phrases that might imply reluctance (the original Russian "скрипя сердцем" translates to something like "creaking with heart," meaning reluctantly or "gritting one's teeth"). You might want to change it.
        *   **Important:** The default prompt is in Russian. If you are processing text in another language, **translate the prompt into that language**, including instructions for preserving tags and whitespace characters. The LLM's performance heavily depends on the language and clarity of instructions.
    *   **`heuristics`:** Heuristics settings (see below). Enabled/disabled by setting to `True` or `False`.

## Heuristics

Heuristics are optional text transformations applied *before* sending to the LLM (preprocessing) and *after* receiving the response (postprocessing), designed to **improve processing quality**. They are configured in the `config.yaml` file in the `heuristics` section.

*   **`remove_commas` (Preprocessing, only 1st pass):**
    *   **What it does:** Removes all commas from the chunk *before* sending it to the LLM (only on the first pass if `number_of_passes: 1`).
    *   **When to use:** Can improve results if the original text has **many unnecessary or incorrectly placed commas**, and you want the model to reinsert them "from scratch." **Recommended for powerful models** (e.g., `gemini-2.5-pro-exp-03-25`) that are better at restoring punctuation.
    *   **Caveats:** Weaker models might not reinsert commas correctly or at all.
*   **`replace_tags_with_placeholder` (Preprocessing + Postprocessing):**
    *   **What it does:**
        *   *Preprocessing:* Finds all tags like `<...>` (e.g., `<p>`, `</emphasis>`, `<RUN123/>`) and replaces them with special placeholder characters (e.g., `@`, `#`, `$`). Information about the replaced tags is saved.
        *   *Postprocessing:* After receiving the LLM's response, replaces the placeholders back with the original tags in the same order.
    *   **When to use:** **Strongly recommended for FB2 and DOCX formats.** LLMs often struggle to preserve HTML/XML-like tags. This heuristic "hides" tags from the LLM. **Weaker models (usually local ones) might not be able to process tagged formats at all without this heuristic.**
    *   **Caveats:** If the LLM deletes or adds a placeholder character in the text, tag restoration will fail, and validation (`validate_response`) will likely fail.
*   **`remove_thinking` (Postprocessing):**
    *   **What it does:** Removes special tags `<think>` and `</think>` along with their content from the LLM's response. Some models (especially those following Chain-of-Thought or similar techniques) may include their "reasoning" or intermediate steps in the output, wrapping them in such tags.
    *   **When to use:** Enable this heuristic if your LLM adds text like `<think>...reasoning...</think>` to the response, which should not be part of the final processed book text. This helps clean up the model's output from auxiliary information.
    *   **Caveats:** Ensure that the `<think>` and `</think>` tags are used by the model specifically to denote removable reasoning and not for something else that should remain in the text.

## Running the Program

1.  Place your books (`.fb2`, `.txt`, `.docx`) in the same folder as the program's executable file (`.exe`) and the `config.yaml` file.
2.  Run the `.exe` file.
3.  The program will start processing the found files one by one. You will see process logs in the console.
4.  Processed files will be saved in the folder specified in `processing.output_dir` (default `output_books`), with the suffix `_rewritten` (e.g., `my_book_rewritten.fb2`).
5.  **Cache:** During processing, a `book_temp` folder is created, containing subfolders for each book with processed chunks (`chunkXXXXX.txt`). If the process is interrupted, the program will read these files on the next run and resume from where it left off. **Optional:** Open in "Track Changes" mode in Word/Google Docs and review the suggested edits.
6.  **Resetting Cache:** If you want to reprocess a book from scratch (e.g., after changing the prompt or settings), delete the corresponding subfolder inside `book_temp` (e.g., `book_temp/my_book_name/`).

## Troubleshooting

*   **`RESOURCE_EXHAUSTED` (Error 429 in logs):** Too many concurrent API requests, or the daily free request limit has been reached, or funds have run out on the balance for paid usage. Reduce the `processing.workers_amount` value in `config.yaml`, wait for the next day, or top up your balance.
*   **Blocking messages from Google (Filter):** Google Gemini's safety filter has been triggered. See the "Important Notes" section. Try changing the prompt, using a different model, or another provider (OpenRouter, YandexGPT, GigaChat, etc.).
*   **`ValidationFailedError`:** The LLM changed the number of `<` or `>`. This often happens if the `replace_tags_with_placeholder` heuristic is disabled for FB2/DOCX, or if the LLM added/removed a placeholder character when the heuristic was enabled. It sometimes occurs; usually, the model succeeds on the second attempt. Ensure the heuristic is enabled for FB2/DOCX and the prompt clearly instructs to preserve tags/placeholders.
*   **Slow processing:** Increase `processing.workers_amount` (carefully!) or `processing.chunk_size`. Use faster models (Flash instead of Pro).

## License

This project is distributed under the MIT License. See the `LICENSE` file for details.