# All Release Types

Prep all release type related tags. Info mainly extracted from `title` tag.

This plugin will accept Chinese versions of the wordings.

- [x] Put (live), (live版) or (现场版) and similar things into `releasetype` tag, if `releasetype` was not previously set.
- [x] If `releasetype` was set but not `secondaryreleasetype`, `secondaryreleasetype` will be used to set 'live'. `releasetype` tag then will become a list.
- [ ] ~~Stuff like (live清晰版), (男声完美版), (电影「魔兽世界」主题曲) will be also considered to be a part of the `releasetype` and appended.~~_(Not sure what the correct way is yet)_