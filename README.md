# FairyJoke

FairyJoke is a rhythm games database project with a public API.

The long term goal is to serve as a repository for static data such as lists of
songs, difficulties, a list of different rhythm games and their accompanying
release dates and platforms, and as many useful things relating to rhythm games
that someone could want to access.

Think https://remywiki.com/ but more developer-friendly to be incorporated and
used into other projects such as bots, web tools, game servers, without having
to resort to scraping wikis or parsing the game files yourself.

## Where is the data from

The plan is to allow sourcing the data either from game dumps or trustable
sources (such as a wiki or official songs list). It will mostly depend on what's
available for each game, and what's easier to import.

However one of the most appreciated features of FairyJoke is to be able to get
song information from an in-game ID, this is often something that can not be
obtained from wiki websites. This either requires parsing the game files, or the
official application / website of the game, which in some cases expose this
information.

## Zoom on features

### Plugins

Plugins come in two varieties. Internal and external. Internal plugins are
stored in `src/fairyjoke/plugins`, and core features CAN depend on those
plugins. For example, the concept of what a "game" is is defined in the internal
plugin called "Series", which creates the "Game", "Series", "Release", objects
in the database and their relations. External plugins, such as the "SOUND
VOLTEX" plugin, are stored directly in the `plugins` folder in the working
directory. These plugins can depend on internal plugins such as the "Series"
one. However the app should not depend on these plugins.

Plugins can handle the following things:

- Database objects
- API routes
- Web UI routes
- Init scripts, see "The application lifecycle"

### The application lifecycle

When starting the application, even with plugins installed, no data should be
created in the database. To populate the database, the "init" entrypoint should
be called. As this data can become very big, initializing only once ensures a
short start time for the application. The init entrypoint will run the init
scripts of every plugins. These scripts should limit themselves to loading
static data from the `data` folders.

This static data itself could be generated from scripts, that would parse game
files, official websites, trustable wikis, or other sources, and generate the
YAML/JSON to be then used by the init scripts. Seperating this process from the
init scripts avoids repetitively executing these expensive actions, especially
if they imply scraping existing websites.

Once the init scripts are run and the databases are populated, the application
can start and will load data directly from the database, allowing for efficient
querying of the data.

## Contributing

PRs and discussions are welcome. I am especially looking for contributions to
add support for more games. If you want a game to be added and have programming
knowledge, I'd be more than happy to guide you into the process of adding it.
If you are the maintainer of a project that uses FairyJoke as a data source and
need some features to be added, please reach out to me too.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

- Reach me on Twitter [@Tina_otoge](https://twitter.com/Tina_otoge) or on Discord as `@tina.moe`.

## Acknowledgments

The illegal distribution of copyrighted works should not be enabled by this
project. I believe this project has its place on the Internet and should be
treated the same as wiki or other encyclopedia projects as providing public
information about existing and past works, and as an initiative for information
preservation. Hosting of in-game assets should be restricted to what is
necessary to properly document works, in the same vein as wiki websites.

Other projects that either inspired, made possible, or share a smilar goal to
FairyJoke, that you could check out too:

- https://remywiki.com/
- https://silentblue.remywiki.com/
- https://bemaniwiki.com/
- https://arcade-songs.zetaraku.dev/
- https://ddr.stepcharts.com/
- https://sdvx.in/
- https://zenius-i-vanisher.com/
- https://github.com/TNG-dev/Tachi/

Notable official resources:

- Official song list for maimai: https://maimai.sega.com/song/
  - Probably other games too, haven't looked yet
- Official e-AMUSEMENT website and application
