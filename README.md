<a name="Русский"></a>

# LLM Book Rewriter

![Alt text](https://imgur.com/a/FT73VWY "Пример 1")

[Go to English](#english)

## 📖 Описание

Эта программа предназначена для помощи авторам и редакторам в вычитке и переписывании текста книг с использованием больших языковых моделей (LLM). Она позволяет:

*   **Улучшить стиль и грамматику:** LLM может предложить варианты улучшения текста, исправить орфографические и пунктуационные ошибки.
*   **Перефразировать текст:** Если нужно изменить формулировку, LLM может предложить альтернативные варианты, сохраняя смысл.
*   **Адаптировать текст под разные аудитории:** LLM может упростить или усложнить текст в зависимости от целевой аудитории.

**Важное замечание:**

*   В связи с ограничениями, использование программы на территории Российской Федерации может быть затруднено. *(Возможно, вам потребуется использовать альтернативные методы подключения к сети).*
*   При выполнении запросов из стран Европейской экономической зоны (EEA), Швейцарии или Великобритании(Нидерланды подходят), Google в соответствии со своей политикой, **не использует ваши данные для обучения моделей.** Это означает, что ваши тексты не будут использованы для дальнейшего улучшения LLM.

## 🔑 Получение API-ключа

Для работы программы необходим API-ключ Google AI Studio.  Вот как его получить:

1.  Перейдите по ссылке: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2.  Следуйте инструкциям Google для создания и получения вашего API-ключа.

## ⚙️ Настройка

1.  После получения API-ключа, создайте файл `config.json` в корневой директории проекта (если его еще нет).
2.  Внесите в файл `config.json` ваш API-ключ в следующем формате:
3.  (Опционально) Измените chunk_size, он отвечает за размер текста, который единовременно будет передан в модель. Низкие значения(около 1000) улучшают качество, но ведут к увеличению числа запросов(бесплатный лимит - 1500 запросов в день)
4.  (Опционально) Измените main_prompt - инструкцию нейросети. По умолчанию он вычитывает текст, но можно задать любую цель: Переписать в другом стиле, заменить всех котов на собак и тому подобное

```json
{
    "gemini_api_key": "СЮДА",
    "model_name": "models/gemini-2.0-flash",
    "chunk_size": 8000,
    "output_dir": "output_books",
    "main_prompt": "You are a professional rewriter. Rewrite the following text fragment according to the client's instructions below.\n\nClient's instructions:\n1. Correct any spelling mistakes and typos.\n2. Correct punctuation.\n3. Do not change any names/words you aren't sure about\n4. Do not change anything else."
}
```

## 🚀 Запуск

*   Положите книги(пока поддерживает только fb2) в одну директорию с кодом, запустите
*   Результат будет лежать в папке output_books, обработка одной средней книги(400к символов) занимает около десяти минут
*   Если хотите начать обработку заново, очистите файлы processed_chunks.txt и processed_chunks_count.txt
---

<a name="english"></a>

# LLM Book Rewriter

[Go to Русский](#русский)

## 📖 Description

This program is designed to assist authors and editors in proofreading and rewriting book texts using large language models (LLM). It allows you to:

*   **Improve style and grammar:** LLM can suggest text improvements and correct spelling and punctuation errors.
*   **Paraphrase text:** If you need to change the wording, LLM can offer alternative options while preserving the meaning.
*   **Adapt the text for different audiences:** LLM can simplify or complicate the text depending on the target audience.

**Important Note:**

*   Due to restrictions, the use of the program in the Russian Federation may be difficult. *(You may need to use alternative methods of connecting to the network).*
*   When making requests from countries in the European Economic Area (EEA), Switzerland, or the United Kingdom, Google, in accordance with its policy, **does not use your data to train models.** This means that your texts will not be used to further improve the LLM.

## 🔑 Obtaining an API Key

To run the program, you need a Google AI Studio API key. Here's how to get it:

1.  Go to: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2.  Follow Google's instructions to create and obtain your API key.

## ⚙️ Configuration

1.  After obtaining the API key, create a `config.json` file in the root directory of the project (if it doesn't already exist).
2.  Enter your API key into the `config.json` file in the following format:
3.  (Optional) As you can see, in both config.json and main.py prompts are in Russian. From my tests, it can drastically affect output quality, so you should translate it to the language of your book

```json
{
    "gemini_api_key": "abcde1234",
    "model_name": "models/gemini-2.0-flash",
    "chunk_size": 8000,
    "output_dir": "output_books",
    "main_prompt": "You are a professional rewriter. Rewrite the following text fragment according to the client's instructions below.\n\nClient's instructions:\n1. Correct any spelling mistakes and typos.\n2. Correct punctuation.\n3. Do not change any names/words you aren't sure about\n4. Do not change anything else."
}
```

## 🚀 Running

*   Put the books (currently only supports fb2 format) in the same directory as the code, then run it.
*   The output will be in the "output_books" folder. Processing one average book (400k characters) takes about ten minutes.
*   If you want to start processing from scratch, clear the processed_chunks.txt and processed_chunks_count.txt files.
