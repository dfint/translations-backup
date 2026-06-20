---
title: "Перевод игры Dwarf Fortress на русский язык"
description: "Русификатор для 50.* и более новых версий Dwarf Fortress"
lang: "ru-RU" # replace it with your language code
permalink: /russian/
layout: download_page
downloads:
    windows_description: "Версия для Windows:"
    linux_description: "Версия для Linux:"
---

Установщик локализации поддерживает версии DF от 50.10 и новее, включая 51, 52 и 53 версии.
Поддерживаются варианты steam, itch.io, classic для Windows и Linux.

Краткая инструкция по установке:

- Скачайте архив, распакуйте, запустите файл `dfint-installer`.
- Выберите ("Откройте") исполняемый файл игры (`Dwarf Fortress.exe` или `dwarfort`). Можно положить файл `dfint-installer` в папку игры, тогда не нужно будет при первом запуске указывать путь к исполняемому файлу.
- Выберите язык перевода, нажать "Обновить" ("Update").
- Запустите игру.
- Для обновления перевода/конфигурации для более новых версий игры — запустите инсталлятор снова (при закрытой игре), нажать "Обновить".

Если инсталлер по какой-то причине не работает (например, у вас Windows 7 или 8), как альтернативу можно использовать [package-builder](https://dfint-package-build.streamlit.app){:target="_blank"}.

![screenshot](screenshot.png){:.centered}

### Ссылки

- [Проект перевода на transifex](https://app.transifex.com/dwarf-fortress-translation/dwarf-fortress-steam) - здесь вы можете принять участие в доработке перевода игры на русский язык
- [Проект на github](https://github.com/dfint) - здесь ведется разработка инструментов для локализации
- [Официальный сайт Dwarf Fortress](https://bay12games.com/dwarves/), [steam](https://store.steampowered.com/app/975370/Dwarf_Fortress/), [itch.io](https://kitfoxgames.itch.io/dwarf-fortress)
{% if site.data.additional_links_enabled[page.lang] %}{% include_relative _additional_links.md %}{% endif %}
