import aiofile
from babel import Locale
from babel.messages import Catalog
from babel.messages.pofile import PoFileParser, _NormalizedString


async def parse(self, fileobj: aiofile.FileIOWrapperBase) -> None:
    """
    Reads from the file-like object `fileobj` and adds any po file
    units found in it to the `Catalog` supplied to the constructor.
    """

    lineno = 0
    while True:
        line = await fileobj.readline()
        if not line:
            break

        line = line.strip()
        if not isinstance(line, str):
            line = line.decode(self.catalog.charset)
        if not line:
            continue
        if line.startswith('#'):
            if line[1:].startswith('~'):
                self._process_message_line(lineno, line[2:].lstrip(), obsolete=True)
            else:
                self._process_comment(line)
        else:
            self._process_message_line(lineno, line)

        lineno += 1

    self._finish_current_message()

    # No actual messages found, but there was some info in comments, from which
    # we'll construct an empty header message
    if not self.counter and (self.flags or self.user_comments or self.auto_comments):
        self.messages.append(_NormalizedString('""'))
        self.translations.append([0, _NormalizedString('""')])
        self._add_message()


async def read_po_async(
    fileobj: aiofile.FileIOWrapperBase,
    locale: str | Locale | None = None,
    domain: str | None = None,
    ignore_obsolete: bool = False,
    charset: str | None = None,
    abort_invalid: bool = False,
) -> Catalog:
    catalog = Catalog(locale=locale, domain=domain, charset=charset)
    parser = PoFileParser(catalog, ignore_obsolete, abort_invalid=abort_invalid)
    await parse(parser, fileobj)
    return catalog
