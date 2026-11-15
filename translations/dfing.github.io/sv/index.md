---
title: "Översättning av Dwarf Fortress till svenska"
description: "Lokalisering för Dwarf Fortress 50.* och senare versioner"
lang: "sv" # replace it with your language code
permalink: /sv/
layout: download_page
downloads:
    windows_description: "Windows-version:"
    linux_description: "Linux-version:"
---

Installationsprogrammet för lokaliseringen stöder DF 50.10 och senare, inklusive versionerna 51, 52 och 53.
Steam-, itch.io- och klassiska versioner för både Windows och Linux stöds.

Kortfattade instruktioner för hur du installerar översättningen:

- Hämta installationsprogrammet, packa upp det och kör filen `dfint-installer`.
- Välj spelets körbara fil (”Öppna”, `Dwarf Fortress.exe` eller `dwarfort`). Du kan också lägga filen `dfint-installer` i spelets katalog, då hittar den spelets körbara fil själv.
- Välj översättningsspråk och tryck sedan på ”Uppdatera”.
- Starta spelet.
- Om du vill uppdatera översättningen eller konfigurationen för en nyare spelversion kör du installationsprogrammet igen, medan spelet är avstängt, och trycker sedan på ”Uppdatera”.

Om du får problem med installationsprogrammet, till exempel om du använder Windows 7 eller 8, kan du använda [package-builder](https://dfint-package-build.streamlit.app){:target="_blank"} i stället.

![screenshot](screenshot.png){:.centered}

### Länkar

- [Översättningsprojektet på Transifex](https://app.transifex.com/dwarf-fortress-translation/dwarf-fortress-steam) - här kan du bidra till översättningen av spelet till ditt språk
- [Projektet på GitHub](https://github.com/dfint) - här utvecklar vi verktyg för lokalisering
- [Dwarf Fortress officiella webbplats](https://bay12games.com/dwarves/), [Steam](https://store.steampowered.com/app/975370/Dwarf_Fortress/), [itch.io](https://kitfoxgames.itch.io/dwarf-fortress)
{% if site.data.additional_links_enabled[page.lang] %}{% include_relative _additional_links.md %}{% endif %}
