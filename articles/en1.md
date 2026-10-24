If you post AI-generated or edited photos and videos to Instagram or TikTok, the file usually carries more than the picture. Generators and editors write records into it: EXIF, XMP, IPTC and, more and more often, C2PA "content credentials". Social apps can read those records when you upload.

## What is inside the file

- EXIF: camera or app name, date, sometimes location.
- XMP and IPTC: editing history and fields like "digital source type", which some generators fill in.
- C2PA: a signed record of how the file was made. Tools like OpenAI, Adobe and Google add it to generated images.

You can see what your file contains on contentcredentials.org/verify or with any EXIF viewer.

## How to clean it in Telegram

Media Clean is a free bot that strips this metadata: [@AIMediaclean_bot](https://t.me/AIMediaclean_bot?start=article_en)

- Send a photo or video up to 20 MB.
- Choose JPEG or PNG for photos, MP4 for video.
- Download the result.

Photos are rebuilt from pixels at full resolution, videos are re-encoded to high-quality H.264/AAC. The original EXIF, XMP, IPTC and C2PA blocks are not carried over. The bot then writes new neutral device data into the result (for example, Apple iPhone), so the file looks like a normal phone export. The bot speaks 10 languages and needs no install.

## What it does not do

It changes only the file metadata. Watermarks embedded in the pixels or audio stay, and platforms can still recognise AI content in other ways. Their rules about labelling AI content still apply to you.

## Check the result

After cleaning, open the file in the same viewer you used before. The old records should be gone.

Bot: [@AIMediaclean_bot](https://t.me/AIMediaclean_bot?start=article_en)
