# Media Clean — remove AI metadata from photos and videos

Telegram bot: **[@AIMediaclean_bot](https://t.me/AIMediaclean_bot)**

Send a photo or video → choose a format → download a clean file (up to 20 MB).

- **Photos** are rebuilt from pixels.
- **Videos** are re-encoded without the original generation records.
- Works inside Telegram, nothing to install.

> Media Clean cleans file metadata only. Platforms can still detect or label AI-generated content by other means, and their rules about disclosing AI content still apply.

## Links

- Bot: https://t.me/AIMediaclean_bot
- Landing (EN / RU): this repo, `public/` — deployed on Railway

## Русский

Telegram-бот **[@AIMediaclean_bot](https://t.me/AIMediaclean_bot)** удаляет ИИ-метаданные из фото и видео перед публикацией в Instagram, TikTok и других соцсетях.

Отправь фото или видео → выбери формат → скачай чистый файл (до 20 МБ). Фото пересобираются из пикселей, видео перекодируются без исходных записей о генерации.

Бот чистит только метаданные файла: платформы могут распознавать ИИ-контент другими способами, а их правила о его раскрытии продолжают действовать.

## Keywords

remove AI metadata, strip metadata from photo, strip metadata from video, clean EXIF, remove generation records, Telegram bot, metadata cleaner, Instagram, TikTok, удалить метаданные, очистить метаданные фото, ИИ-метаданные, бот Telegram.

## Landing development

```bash
npm start   # zero-dependency static server, PORT from env
```

`__SITE__` in HTML/XML is replaced with the request host at serve time (or `SITE_URL` env if set).
