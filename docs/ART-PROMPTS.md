# Art prompts

Generated with OpenAI image models (`gpt-image-2.5`) through OpenCode. Save each result under the name shown, in one folder, then run:

```sh
python3 scripts/build-art.py <that folder> ~/.config/herdr-app/mods
```

The script keys out the green, cuts sheets into frames, shrinks the characters to 36×48 pixel art and writes the GIFs, portraits, icons and backgrounds into the mods. `python3 scripts/build-art.py <folder> <mods> dwarf orc` rebuilds only those.

Herdr caches images by filename. After replacing art in place, restart Herdr, or use new filenames.

## Characters: `sheet-<name>.png`

Every sheet starts with this, then the character's line:

```
Pixel art sprite sheet, exactly four frames side by side in one horizontal row, equal width cells with wide gaps between them, same small chibi full-body character in every frame, facing forward, simple retro 16-bit RPG sprite, thick dark outline, flat colors, few large visible square pixels, gritty grounded medieval fantasy, serious expression, no anime, no big cute eyes. The background must be one flat solid pure green color (#00FF00) everywhere, no gradient, no vignette, no glow, no ground, no shadow, no text, no grid lines, no border.
```

The four frames are always: 1 at rest, 2 and 3 the working motion, 4 one hand raised calling for attention.

```
ranger: a weathered northern ranger, dark hair, stubble, dark green hooded travel cloak over brown leather, longsword. 2 sword raised high, 3 sword swung down diagonally.
archer: an original male elven sentinel archer, stern face, short cropped dark auburn hair, pointed ears, dark grey hooded cloak over silver ring mail, deep blue tunic, leather bracers, quiver, dark wooden longbow. 2 arrow nocked, 3 string pulled fully back.
dwarf: a stout dwarf warrior, long braided copper-red beard with gold rings, iron helmet, chainmail, dark blue hood, short battle axe. 2 axe raised, 3 axe swung down.
halfling: a cheerful halfling, curly chestnut hair, bare hairy feet, yellow waistcoat, green cloak, small red leather book and quill. 2 and 3 writing in the open book.
wizard: a young wandering wizard in deep sea-blue robes and hood, short dark beard, gnarled staff with a white crystal. 2 crystal glowing, 3 crystal blazing with sparkles.
loremaster: a middle-aged male human scholar of a great stone city, long grey-streaked beard, black and silver long coat, parchment scroll. 2 scroll unrolled, 3 pointing at the text.
healer: an old male human healer, bald, short grey beard, plain grey-brown robe with rope belt, satchel of herbs, stone mortar and pestle. 2 and 3 grinding, green sparkles.
smith: a burly male human blacksmith, short black beard, rolled-up sleeves, leather apron, heavy hammer, tiny glowing white gem in tongs. 2 hammer raised, 3 striking with white sparks.
darklord: an original towering dark lord in heavy black plate armor with jagged iron shoulder spikes, closed horned black helm with a narrow ember-orange slit, dark red cape, a single gold ring on one gauntlet, massive spiked black mace. 2 mace raised, 3 mace slammed down in orange sparks.
sorcerer: an original fallen sorcerer, old man with a long iron-grey beard and cold sneering face, deep crimson and black robes with a high collar, tall black iron staff topped with a dark red orb. 2 orb glowing, 3 red lightning.
wraith: a spectral wraith knight, tattered pitch-black hooded robe, no face, two faint pale blue eye glints, pale ghostly gauntlets, long thin pale sword. 2 sword raised in pale mist, 3 slashing with a ghostly trail.
berserker: a huge muscular dark-skinned brute orc berserker, long black hair, white hand-print war paint, black iron shoulder plate, heavy two-handed cleaver. 2 cleaver raised, 3 smashing down.
orc: a snarling orc soldier, grey-brown scarred skin, tusks, yellow eyes, scraps of black iron armor and dirty red cloth, jagged scimitar. 2 scimitar raised, 3 slashing down.
goblin: a small wiry cave goblin, pale grey skin, big pointed ears, sharp grin, ragged dark leather, bone-tipped spear. 2 spear drawn back, 3 thrust.
troll: a hulking cave troll, rough grey stone-like skin, tiny dull face, huge arms, loincloth, iron shackle, massive wooden club. 2 club raised, 3 smashing down.
spy: a shifty male human spy and traitor, pale sallow face, greasy black hair, charcoal hooded cloak, black leather, curved dagger. 2 dagger raised, 3 stabbing.
```

## Buildings: `place-<name>.png`

```
Pixel art game icon of a single building, 32-bit JRPG style, visible square pixels, limited palette, silver-white highlights and deep twilight blue shadows, bold simple silhouette, large and centered, filling most of the frame, few details, plain solid pure green background (#00FF00), no ground, no scenery, no characters, no text, no border.
```

```
valley: an elegant elven house with slender pale stone pillars, graceful curved arches, a sweeping leaf-shaped roof and a small waterfall beside it, warm lit windows.
gate: a great dwarven gate carved into a small grey mountain peak, tall square stone doorway with angular runic carvings, two carved stone guardian pillars, warm forge glow inside.
burrow: a cozy round burrow home dug into a small grassy hill, perfectly round painted door with a brass knob in the middle, round glowing window, little chimney with smoke, flowers.
tower: a tall slender white stone citadel tower with a pointed silver spire, a long pennant banner, small battlements, a few glowing windows.
```

## Panel icons: `icon-<name>.png`

```
files: Pixel art game icon of one closed thick old book, red leather cover with gold corner trim and a small gold clasp, bold simple silhouette, large and centered, few details, visible square pixels, plain solid pure green background (#00FF00), no text, no border.
changes: Pixel art game icon of one small elegant elven sailing ship seen from the side, white hull with a swan-shaped curved prow, single pale silver sail, bold simple silhouette, large and centered, few details, visible square pixels, no water, plain solid pure green background (#00FF00), no text, no border.
inbox: Pixel art game icon of one round dark crystal seeing-stone orb on a small carved stone stand, swirling glowing blue and silver light inside, bold simple silhouette, large and centered, few details, visible square pixels, plain solid pure green background (#00FF00), no text, no border.
```

## Backgrounds

`sidebar.png`:

```
Tall narrow vertical pixel art scene, 1:4 portrait aspect ratio, modern HD-2D JRPG background style. A hidden elven valley at deep twilight seen from above: at the top a night sky full of bright stars and a crescent moon, below it tall pale cliffs with slender silver waterfalls, then graceful elven houses with curved roofs and warm lantern windows in dark pine and birch trees, and at the bottom a misty river with an arched stone bridge. Deep navy, indigo and silver palette with small warm lantern lights, dark and low contrast overall so text stays readable on top, no characters, no text, no logo, no border.
```

`map.png`:

```
Flat top-down antique fantasy map in the style of a hand-drawn 1930s storybook map, black and red ink line work on aged parchment, extremely dense detail. An invented continent unlike any real place, filling most of the page and running off the edges: a long chain of jagged mountains drawn as rows of little ink peaks running north to south, a great forest drawn as hundreds of tiny round trees, wide winding rivers, marshes drawn as tufts, rolling hills drawn as bumps, a lonely single mountain, a ragged western coastline with a deep gulf, sea with fine hatching and a tiny ship. Small tower and castle symbols. Muted sepia, ink black, a few faded red accents, no text, no letters, no labels, no compass, no border.
```

## Tips

- If a sheet comes back without the green background, ask again; the script also accepts a transparent background.
- If two figures touch (a blade crossing into the next frame), the script cuts at the thinnest column between them.
- Check designs for an unintended likeness to a known character, and regenerate with different hair and clothing if one appears.
