[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/xxstealz/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/xxstealz/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# news-image-20261121 — "The Daily Globe"

Sums up the world's news of **Saturday 21 November 2026** in one image:
`entry.png` (1024×1024 PNG), drawn from scratch with code
(`draw_entry.py`, Python + PIL, no network, no external assets).

Six stories, verified 21 Nov 2026 from Reuters, AP, CNN, Xinhua and Cboe:

1. **Iran hits US bases in Bahrain** — IRGC says missiles and drones
   hit US positions at two bases; Bahrain reports a civilian site hit,
   a fire, no injuries
2. **"El Chapo Isidro" caught** — FBI Top 10 cartel boss Fausto Isidro
   Meza Flores seized in Sinaloa; 11 dead in the backlash
3. **Missile hits Zelenskyy's hometown** — Russian strike on Kryvyi Rih
   kills 2, wounds 60 in a double-tap attack
4. **COP31: no deal, overtime** — Antalya talks run past deadline; the
   draft drops fossil fuels and a $120bn aid target
5. **Nasdaq −5.3%, S&P in correction** — Wall Street's worst week since
   March 2020; Nvidia falls 14% in a day
6. **"Friend" vs "killer"** — Trump defends calling Putin "my friend"
   after Shenzhen; Zelenskyy: "For us, he is an enemy, and of course,
   for us, he is a killer"

Footer: Wolbachia mosquitoes cut dengue ~69% in a Brazil trial of
5,700 children; magnitude 6.7 quake shakes Peru's Andes, felt in Lima;
Anthropic slides 8.5% to $88.91 a day after its $2 trillion debut.

`main.ts` (Node 22, stdlib only) copies `entry.png` to
`/output/entry.png` — deterministic, two runs byte-identical.
