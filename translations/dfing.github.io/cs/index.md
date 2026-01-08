---
title: "Translation of Dwarf Fortress to 'your language'"
description: "Localization for 50.* and newer versions of Dwarf Fortress"
lang: "en" # replace it with your language code
permalink: /en/
additional_links: false
layout: download_page
downloads:
    windows_description: "Windows version:"
    linux_description: "Linux version:"
---

The localization installer supports version of DF 50.10 and newer, including versions 51, 52 and 53.
Steam, itch.io, classic versions for both Windows and Linux platforms are supported.

Brief instructions on how to install the translation:

- Download the installer, unpack it, execute the `dfint-installer` file.
- Select ("Open") the game's executable file (`Dwarf Fortress.exe` or `dwarfort`). Alternatively, you can put the `dfint-installer` file into the game's directory, then it will find the game's executable by itself.
- Choose the translation language, then press "Update".
- Run the game.
- To update translation or configuration for a newer version of the game, run the installer again (while the game is shut down) then press "Update".

If you have some troubles with the installer (e.g. you are useing Windows 7 or 8), you can use the [package-builder](https://dfint-package-build.streamlit.app){:target="_blank"} instead.

![screenshot](screenshot.png){:.centered}

### Links

- [Translation project on transifex](https://app.transifex.com/dwarf-fortress-translation/dwarf-fortress-steam) - here you can participate in translation of the game to your language
- [The project on github](https://github.com/dfint) - this is a place where we develop tools for the localization
- [The official Dwarf Fortress site](https://bay12games.com/dwarves/), [steam](https://store.steampowered.com/app/975370/Dwarf_Fortress/), [itch.io](https://kitfoxgames.itch.io/dwarf-fortress)
{% if page.additional_links %}{% include_relative _additional_links.md %}{% endif %}
