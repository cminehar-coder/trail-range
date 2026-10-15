# Trail / Range

Off-road geometry vs fuel economy for 40 stock U.S. vehicle configurations (2010-2027). Pick weights for ground clearance, approach/departure/breakover angles, tire diameter and wheelbase, and see the Pareto frontier against EPA combined MPG (or miles per dollar of energy once EVs are included).

Writeup: Hobbies → "Trading mpg for clearance" on my site.

- `public/model.js`: scoring, filters, frontier
- `public/data.js` / `vehicles.json`: vehicle specs with source links
- `public/epa-extract.json`: matched EPA records
- `build-data.py`, `build.cjs`: data build
- `test-model.cjs`: `node test-model.cjs`

Static site, no build step needed to view: open `public/index.html`.
