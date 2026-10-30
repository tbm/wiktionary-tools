
# Download Wiktionary locally

Sometimes it's useful to have a local copy of Wiktionary for a given language, for example to search files easily with `grep`.

## Extract from Wiktionary dump file

Wikimedia provides dump files of the latest [Wiktionary information](https://dumps.wikimedia.org/enwiktionary/latest/) from which entries can be extracted.  Specifically, the [dump "pages-articles" file](https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2) is required.  It contains the latest revisions of all pages.

The tool `download/extract_dump` can be used to extract all entries for a given language.  For example, the following command will write all Swahili (lang code `sw`) entries to the directory `out`.  Each entry will be stored as a separate file, using the page title from Wiktionary as the file name.

    download/extract_dump enwiktionary-latest-pages-articles.xml.bz2  --lang sw --out swahili

## Sync from Wiktionary

An alternative method to obtain Wiktionary entries is to download them directly from Wiktionary.  The advantage is that the contents is fresher since dump files are only done from time to time (usually monthly).  The disadvantage, of course, is that it puts more load on the Wiktionary servers.

The download script `download/download` stores each page in a separate file.  This command can be used to download Swahili entries:

    download/download --lang sw --out swahili

If the script is run multiple times, only entries are downloaded where the revision time is later than the revision time from the last download.

However, the revision time is per Wiktionary page and one page can contain multiple entries if different languages.  So if, for example, the English entry changed while the Swahili entry stayed the same, the Swahili entry would be downloaded again.  There would of course be no change but the time stamp on the file would change.

## Initial extraction from dump file plus sync from Wiktionary

The approaches can of course be combined.  You can extract the entries from the dump file and subsequently keep them up-to-date by syncing from Wiktionary itself:

    download/extract_dump enwiktionary-latest-pages-articles.xml.bz2  --lang sw --out swahili
    download/download --lang sw --out swahili

## Revision control

Since Wiktionary entries are stored as regular plain-text files, they can be added to a revision control system, such as [Git](https://git-scm.com/).  This allows makes it easy to review all changes for a language.

Download all initial entries (you can also use `extract_dump` but see the limitation below):

    download/download --lang sw --out swahili
    cd swahili
    git init
    git add .
    git commit . -m "Initial import"

Subsequently, sync the entries, add them to Git and review the changes:

    ../../download/download --lang sw --out .
    git add .
    git commit . -m "Update"
    git show

## Limitations

* Currently, `extract_dump` extracts all entries for a language while `download` specifically downloads lemmas only.  We should add config options to define what should be extracted or downloaded.
* Stale files (i.e. Wiktionary entries that were deleted) are not deleted automatically.

