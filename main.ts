// news-image-20261121 entry (Node 22, standard library only).
// The program copies the drawn entry.png beside this file to
// /output/entry.png. A plain copy is deterministic by construction:
// two runs write byte-identical bytes, and nothing is fetched at
// runtime. Outside the grader, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
if (!existsSync(src)) {
  throw new Error('entry.png is missing next to main.ts; run draw_entry.py first');
}
// An empty MAKEFUN_OUTPUT_DIR falls back to /output instead of
// resolving to a relative "entry.png" in the working directory.
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
// The grader normally pre-creates /output, but a fresh directory
// must not fail the whole entry with an opaque ENOENT.
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);
// A truncated or partial copy would pass the gate as a broken PNG,
// so fail loudly here instead of shipping a corrupt entry.
if (statSync(dest).size !== statSync(src).size) {
  throw new Error(`entry.png copy incomplete: ${statSync(dest).size} of ${statSync(src).size} bytes`);
}
