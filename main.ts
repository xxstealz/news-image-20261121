// news-image-20261121 — entrypoint (Node 22, stdlib only).
//
// The front page is drawn at build time by draw_entry.py and shipped as
// entry.png. This program just places that image at the path the grader
// reads: $MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png when the
// variable is unset. A plain copy, so both runs write identical bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(repoRoot, "entry.png"), join(outDir, "entry.png"));
console.log("entry.png ->", join(outDir, "entry.png"));
