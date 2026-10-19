# Ballon d'Or 2025-26: bonus-point scale and player achievements

Research date: 2026-10-19 (revised after the owner's review). Results come from web searches and the pages the owner linked (sources at the bottom).

**Status: applied to the Google Sheet on 2026-10-19.** The points table is at `U60:Y70` of the `2025-26` tab (units in `Y61:Y70`), and column `AH` holds one formula per player that references it and the competition coefficients `H61:H79`. Each player total below was checked against the sheet's value. The sheet-side rules are in `.claude/rules/ballon-dor-bonus.md`. If an achievement changes, edit the player's `AH` formula and this document together.

Confidence marks: ✔ confirmed by two or more sources · ◐ single source · ⚠ provisional (the competition is still running).

---

## 1. How the points are divided

```
Bonus = Σ ( units × H[competition] × involvement )  +  1 point per super cup / extra trophy won and played in the final
```

`H` is the Competition Type Coefficient from `H61:H79`, so there is still one place to calibrate. `units` is the single knob (the "Balanced" preset: a trophy is 8 units).

### Units

| Achievement | Units | Applies to | Example points (WC / UCL ×1.5 · Big-5 league ×1 · cup ×0.5) |
|---|---|---|---|
| Winner (trophy) | 8 | Team result, scaled by involvement | 12 · 8 · 4 |
| Finalist | 3 | Team result, scaled by involvement | 4.5 · – · 1.5 |
| Semi-finalist | 1 | Team result, scaled by involvement | 1.5 · – · 0.5 |
| Player of the tournament or season | 5 | Individual | 7.5 · 5 · – |
| Top scorer | 3 | Individual | 4.5 · 3 · – |
| **Top assister** (any competition, including the domestic league) | 1.5 | Individual | 2.25 · 1.5 · – |
| Golden Glove / best goalkeeper or defender | 3 | Individual | 4.5 · 3 · – |
| Team of the tournament or season | 1 | Individual | 1.5 · 1 · – |
| Super cup or other trophy not in the table (UEFA Super Cup, Intercontinental Cup, Trophée des Champions, Supercopa, DFL-Supercup, FA Cup) | flat **1 point** | Winner only, and only if the player took part in the final match | 1 |

Rules:
- A league title counts for the champion only (no points for the runner-up).
- The Saudi league is ×0.7, MLS ×0.8, AFCON ×1.2 and AFC Champions League Two ×0.7.
- Only one "Player of the Season" award per competition counts, the league's own official award. Other awards (PFA, FWA, media picks) are listed as extras.
- Shared awards (a tie for top assister) give full points to each player.
- **AFCON 2025 has no winner for scoring purposes.** Senegal won the final on the pitch, but CAF's Appeal Board later awarded it to Morocco. Both teams are scored as finalists (3 units × 1.2 = 3.6), so the ruling and the pending appeal do not matter.
- Team-of-the-season lists are taken from the sources the owner provided (section 2).
- Super cups: I checked line-ups to confirm that each player took part in the final match.

### Involvement multiplier (team results only)

Individual awards need no multiplier, since the award implies the player took part. The thresholds are applied **strictly, with no rounding up** (for example, Haaland's 199 minutes in the EFL Cup is half, not full). They use the minutes already in the sheet's data:

| Competition | Full (×1) | Half (×0.5) | None |
|---|---|---|---|
| Domestic league | ≥ 40% of available minutes (3,420 for 38 games, 3,060 for 34) | 20–40% | < 20% |
| Champions League | ≥ 500 min | 250–499 | < 250 |
| World Cup, AFCON | ≥ 250 min | 125–249 | < 125 |
| Domestic and other cups | ≥ 200 min | 100–199 | < 100 |

---

## 2. Competition results used (2025-26)

| Competition | Winner | Finalist / semi-finalists | Individual awards (nominee-relevant) | Conf. |
|---|---|---|---|---|
| **World Cup 2026** | Spain (1-0 a.e.t. vs Argentina, Torres 106') | Finalist Argentina · semis England (3rd), France (4th) | Golden Ball Rodri · Golden Boot Mbappé (10) · Golden Glove Unai Simón · Young Player Cubarsí · Silver Ball Messi, Bronze Ball Mbappé (media reports) · top assister Olise (7). **Team of the Tournament:** Vozinha; Cucurella, Lisandro Martínez, Upamecano, Porro; Bellingham, Rodri, Olise; Mbappé, Haaland, Messi | ✔ |
| **Champions League** | PSG (1-1 Arsenal, 4-3 pens) | Finalist Arsenal · semis Bayern, Atlético | Player of the Season Kvaratskhelia · top scorer Mbappé (15) · top assisters Olise and Vinícius (8 each, UEFA stats page; both count) · Team of the Season: Raya, Llorente, Marquinhos, Gabriel, Mendes, Olise, Rice, Vitinha, Kvaratskhelia, Dembélé, Kane · final Player of the Match Vitinha | ✔ |
| **AFCON 2025** | Disputed: Senegal won on the pitch, Morocco by CAF ruling | Both teams scored as finalists · semis Nigeria, Egypt | Player of the Tournament Mané · top scorer Brahim Díaz (5) · best goalkeeper Bounou · CAF Best XI includes Hakimi and Mané | ✔ |
| **Premier League** | Arsenal (85 pts vs City 78) | – | Player of the Season Bruno Fernandes (also PFA Players' Player and FWA) · Golden Boot Haaland (27) · Playmaker (assists) Fernandes (21, a record) · Golden Glove Raya (19 clean sheets) · PFA Team of the Year: Raya, Gabriel, Saliba, Rice, Fernandes, Haaland (+ others not on the list) | ✔ |
| **LaLiga** | Barcelona | – | **Best Player Yamal** · Team of the Season: Joan García; Mouriño, Eric García, Llorente, Romero; Pedri, Valverde, Tchouaméni; Muriqi, Mbappé, Yamal · Pichichi Mbappé (25) · most assists Yamal (11) | ✔ |
| **Bundesliga** | Bayern | – | Player of the Season Olise · top scorer Kane (36) · most assists Olise (19) · EA Sports Team of the Season: Kobel; Schlotterbeck, Tah, Upamecano, Vušković; Kimmich, Pavlović, Stiller; Díaz, Kane, Olise | ✔ |
| **Serie A** | Inter (title clinched 3 May) | – | MVP Dimarco (first defender ever) · top scorer Lautaro (17) · most assists Dimarco (17 in the dataset, 18 per Inter) · Team of the Year: Svilar, Palestra, Akanji, Bastoni, Dimarco, Çalhanoğlu, Modrić, McTominay, Lautaro, Malen, Paz | ✔ |
| **Ligue 1** | PSG | – | UNFP Player of the Year Dembélé · UNFP Team of the Year: Hakimi, Pacho, Mendes, Vitinha, Dembélé (+ others) · top scorer Lepaul (21) · top assisters Thomasson and Ajorque (8–9), none on the list | ✔ |
| **Saudi Pro League** | Al-Nassr | – | Golden Boot Quiñones (33) · Player of the Season João Félix · most assists Félix (13) | ✔ |
| **MLS 2026** | In progress (ESPN, 19 Oct 2026) | – | **Messi: 1st in goals (25) and tied 1st in assists (14)** | ⚠ provisional |
| **Liga Portugal 2** | Marítimo (not Chaves) | – | – | ✔ |
| **EFL Cup** | Manchester City (2-0 Arsenal) | Finalist Arsenal · semis Chelsea, Newcastle | – | ✔ |
| **Copa del Rey** | Real Sociedad (2-2, 4-3 pens vs Atlético) | Finalist Atlético · semis Barcelona, Athletic | – | ✔ |
| **DFB-Pokal** | Bayern (3-0 Stuttgart) | Finalist Stuttgart | – | ✔ |
| **Coppa Italia** | Inter (2-0 Lazio) | Finalist Lazio | – | ✔ |
| **King's Cup (Saudi)** | Al Hilal (2-1 Al-Kholood) | Al-Qadsiah out in the quarter-finals | – | ✔ |
| **AFC Champions League Two** | Gamba Osaka (1-0 Al-Nassr) | Finalist Al-Nassr | – | ✔ |
| **Leagues Cup 2026** | – | Inter Miami out in Phase One | – | ✔ |
| **CONCACAF Champions Cup** | – | Inter Miami exited early (2 matches, 180 min) | – | ◐ |

### Super cups and other trophies (1 point each for winners who played the final)

| Trophy | Winner | Nominees who played the final |
|---|---|---|
| UEFA Super Cup (13 Aug 2025) | PSG (2-2, 4-3 pens vs Tottenham) | Hakimi, Fabián Ruiz (sub), Kvaratskhelia, Marquinhos, Mendes, Dembélé, Vitinha, Pacho. Did not play: Zabarnyi, Neves |
| Intercontinental Cup (17 Dec 2025) | PSG (1-1, 2-1 pens vs Flamengo) | Marquinhos, Pacho, Neves, Vitinha, Fabián Ruiz, Kvaratskhelia (started); Dembélé (sub, 78'), per the final's Wikipedia page. Did not play: Hakimi (not in the squad), Zabarnyi (unused substitute) |
| Trophée des Champions (8 Jan 2026) | PSG (2-2, 4-1 pens vs Marseille) | Fabián Ruiz, Neves, Kvaratskhelia, Marquinhos, Mendes, Dembélé, Vitinha, Pacho. Did not play: Hakimi (not in the squad), Zabarnyi (unused substitute) |
| Supercopa de España (11 Jan 2026) | Barcelona (3-2 Real Madrid) | Cubarsí, Pedri, Yamal (started); Olmo, Ferran Torres (substitutes, 66') |
| DFL-Supercup (16 Aug 2025) | Bayern (2-1 Stuttgart) | Kane, Díaz, Olise, Upamecano (all started) |
| FA Cup final (16 May 2026) | Manchester City (1-0 Chelsea) | Haaland, Rodri (both started) |
| Supercoppa Italiana, Community Shield | Napoli, Crystal Palace | No nominees in the winning teams |
| Finalissima (Spain v Argentina) | Never played (cancelled in March 2026, dispute over who forfeited) | – |

---

## 3. Players (sheet order)

Format: each line gives the achievement, its points and the involvement check. "Extras" are achievements outside the table, with no points.

### GK

**David Raya** (Arsenal) — **18.0**
- Premier League champion 8.0 (3,330 min, full)
- Champions League finalist 4.5 (1,290 min, full)
- Premier League Golden Glove 3.0
- Champions League Team of the Season 1.5
- PFA Premier League Team of the Year 1.0
- EFL Cup finalist: 0 (no cup minutes in the dataset)

**Vozinha** (Chaves / Cabo Verde) — **1.5**
- World Cup Team of the Tournament 1.5 (goalkeeper)
- Chaves did not win Liga Portugal 2 (Marítimo did). No other titles or awards found.
- Extras: Cabo Verde reached the knockout stage (round of 32) at their first World Cup, drawing 0-0 with Spain and Saudi Arabia and 2-2 with Uruguay. They lost to Argentina in the round of 32 (inferred from Argentina's later run).

### CB

**Pau Cubarsí** (Barcelona) — **21.5**
- World Cup winner 12.0 (750 min, full)
- LaLiga champion 8.0 (2,708 min, full)
- Supercopa de España winner 1.0 (started the final)
- Copa del Rey semi-finalist 0.5 (347 min, full)
- Not counted: LaLiga Team of the Season. He is not in the 11 listed on the owner's source page (the press named him among the substitutes of a wider 19-man squad).
- Extras: World Cup Young Player of the Tournament

**Gabriel Magalhães** (Arsenal) — **16.5**
- Premier League champion 8.0
- Champions League finalist 4.5 (1,002 min)
- EFL Cup finalist 1.5 (309 min)
- Champions League Team of the Season 1.5
- PFA Premier League Team of the Year 1.0

**Marquinhos** (PSG) — **20.5**
- Champions League winner 12.0 (1,320 min)
- Ligue 1 champion 4.0 (1,049 min = 34%, half)
- Super cups 3.0 (UEFA Super Cup, Trophée des Champions, Intercontinental Cup)
- Champions League Team of the Season 1.5

**Willian Pacho** (PSG) — **24.0**
- Champions League winner 12.0 (1,560 min)
- Ligue 1 champion 8.0 (1,915 min)
- Super cups 3.0 (UEFA Super Cup, Trophée des Champions, Intercontinental Cup)
- UNFP Ligue 1 Team of the Year 1.0

**William Saliba** (Arsenal) — **16.5**
- Premier League champion 8.0
- Champions League finalist 4.5 (1,110 min)
- EFL Cup finalist 1.5 (450 min)
- World Cup semi-finalist (France, 4th) 1.5 (480 min)
- PFA Premier League Team of the Year 1.0

**Dayot Upamecano** (Bayern) — **18.5**
- Bundesliga champion 8.0 (1,797 min = 59%)
- DFB-Pokal winner 4.0 (450 min)
- Champions League semi-finalist 1.5 (1,013 min)
- World Cup semi-finalist (France) 1.5 (661 min)
- World Cup Team of the Tournament 1.5
- Bundesliga Team of the Season 1.0
- DFL-Supercup winner 1.0 (started the final)

**Illia Zabarnyi** (PSG) — **8.0**
- Ligue 1 champion 8.0 (2,387 min)
- Champions League winner: 0 (only 213 min, under the 250-minute threshold)
- Super cups: 0 (did not play in any of the three finals)

### LB/RB/LWB/RWB

**Marc Cucurella** (Chelsea) — **14.0**
- World Cup winner (Spain) 12.0 (750 min)
- World Cup Team of the Tournament 1.5
- EFL Cup semi-finalist 0.5 (221 min)
- Extras: FA Cup finalist (started the final, lost 0-1 to Manchester City)

**Achraf Hakimi** (PSG) — **26.8**
- Champions League winner 12.0 (1,154 min)
- Ligue 1 champion 8.0 (1,374 min = 45%)
- AFCON finalist 3.6 (446 min; Morocco scored as a finalist, see section 1)
- AFCON Best XI 1.2
- UNFP Ligue 1 Team of the Year 1.0
- UEFA Super Cup 1.0 (started). He missed the other two finals.
- Extras: 6 Champions League assists (joint 3rd)

**Nuno Mendes** (PSG) — **25.5**
- Champions League winner 12.0 (1,403 min)
- Ligue 1 champion 8.0 (1,251 min = 41%, full)
- Super cups 3.0 (all three finals)
- Champions League Team of the Season 1.5
- UNFP Ligue 1 Team of the Year 1.0
- Extras: scored the winning penalty in the UEFA Super Cup shootout

**Federico Dimarco** (Inter) — **17.5**
- Serie A champion 8.0 (2,704 min)
- Serie A MVP 5.0
- Coppa Italia winner 2.0 (150 min, half)
- Serie A top assister 1.5
- Serie A Team of the Year 1.0
- Extras: first defender ever to win Serie A MVP · single-season assist record (17 in the dataset, 18 per Inter) · lost the Supercoppa semi-final to Bologna on penalties

### DMC/MC

**João Neves** (PSG) — **22.0**
- Champions League winner 12.0 (1,144 min)
- Ligue 1 champion 8.0 (1,287 min = 42%)
- Super cups 2.0 (Intercontinental Cup, Trophée des Champions; he did not play the UEFA Super Cup)

**Declan Rice** (Arsenal) — **18.0**
- Premier League champion 8.0
- Champions League finalist 4.5 (1,069 min)
- EFL Cup finalist 1.5 (300 min)
- Champions League Team of the Season 1.5
- World Cup semi-finalist (England, 3rd) 1.5 (558 min)
- PFA Premier League Team of the Year 1.0

**Rodri** (Manchester City) — **24.0**
- World Cup winner 12.0 (726 min)
- World Cup Golden Ball 7.5
- EFL Cup winner 2.0 (137 min, half)
- World Cup Team of the Tournament 1.5
- FA Cup winner 1.0 (started the final)
- Manchester City finished runner-up in the Premier League, so no league points.

**Fabián Ruiz** (PSG) — **31.0**
- Champions League winner 12.0 (650 min)
- World Cup winner (Spain) 12.0 (331 min, full)
- Ligue 1 champion 4.0 (1,129 min = 37%, half)
- Super cups 3.0 (all three finals)

**Vitinha** (PSG) — **25.5**
- Champions League winner 12.0 (1,544 min)
- Ligue 1 champion 8.0 (2,121 min)
- Super cups 3.0 (UEFA Super Cup, Trophée des Champions, Intercontinental Cup)
- Champions League Team of the Season 1.5
- UNFP Ligue 1 Team of the Year 1.0
- Extras: Player of the Match in the Champions League final · UNFP Player of the Year nominee

### MC/AMC

**Jude Bellingham** (Real Madrid) — **3.0**
- World Cup semi-finalist (England, 3rd) 1.5 (616 min)
- World Cup Team of the Tournament 1.5
- Real Madrid won nothing: out of the Copa del Rey in the round of 16 (to Albacete), lost the Supercopa final.
- Extras: 7 World Cup goals in the dataset

**Bruno Fernandes** (Manchester United) — **7.5**
- Premier League Player of the Season 5.0
- Premier League top assister 1.5 (21, a record)
- PFA Premier League Team of the Year 1.0
- Extras: PFA Players' Player of the Year · FWA Footballer of the Year (first Manchester United winner since Rooney in 2009/10)

**Pedri** (Barcelona) — **22.25**
- World Cup winner 12.0 (499 min)
- LaLiga champion 8.0 (2,107 min)
- LaLiga Team of the Season 1.0
- Supercopa de España winner 1.0 (started the final)
- Copa del Rey semi-finalist 0.25 (127 min, half)

**Dani Olmo** (Barcelona) — **21.5**
- World Cup winner 12.0 (495 min)
- LaLiga champion 8.0 (2,077 min)
- Copa del Rey semi-finalist 0.5 (274 min)
- Supercopa de España winner 1.0 (substitute in the final, 66')

### LW/RW

**Luis Díaz** (Bayern) — **15.5**
- Bundesliga champion 8.0 (2,450 min)
- DFB-Pokal winner 4.0 (538 min)
- Champions League semi-finalist 1.5 (987 min)
- Bundesliga Team of the Season 1.0
- DFL-Supercup winner 1.0 (started and scored)
- Extras: 14 Bundesliga assists (3rd)

**Khvicha Kvaratskhelia** (PSG) — **32.0**
- Champions League winner 12.0 (1,140 min)
- Ligue 1 champion 8.0 (1,483 min = 48%)
- Champions League Player of the Season 7.5
- Super cups 3.0 (all three finals; scored in the Intercontinental Cup)
- Champions League Team of the Season 1.5
- Extras: 10 Champions League goals (joint 3rd) · 6 assists

**Sadio Mané** (Al-Nassr / Senegal) — **18.5**
- AFCON Player of the Tournament 6.0
- Saudi Pro League champion 5.6 (2,132 min = 70%)
- AFCON finalist 3.6 (646 min)
- AFC Champions League Two finalist 2.1 (438 min)
- AFCON Best XI 1.2

**Lionel Messi** (Inter Miami / Argentina) — **9.6** (provisional: MLS 2026 is still running)
- World Cup finalist 4.5 (740 min)
- MLS 2026 top scorer 2.4 (25 goals, 1st) ⚠
- MLS 2026 top assister 1.2 (14 assists, tied 1st with five others including teammate De Paul) ⚠
- World Cup Team of the Tournament 1.5
- Leagues Cup (out in Phase One) and CONCACAF Champions Cup (early exit): none.
- Extras, no points (2025 MLS season, not the sheet's 2026 data): **MLS Cup 2025 winner** (6 Dec 2025, 3-1 vs Vancouver) · **2025 MLS MVP** (his second in a row) · 2025 Golden Boot (29 goals) · selected in the MLS Best XI 2025 (per the owner; I could not confirm it on the page I could read) · World Cup Silver Ball ◐
- If you decide the 2025 items count: MLS Cup winner 6.4 + MVP 4.0 + Best XI 0.8 would add 11.2.

**Michael Olise** (Bayern) — **31.0**
- Bundesliga champion 8.0 (2,317 min)
- Bundesliga Player of the Season 5.0
- DFB-Pokal winner 4.0 (522 min)
- World Cup top assister 2.25 (7, a single-tournament record) ◐
- Champions League top assister 2.25 (8, shared with Vinícius)
- Bundesliga top assister 1.5 (19)
- Champions League semi-finalist 1.5 (1,081 min)
- Champions League Team of the Season 1.5
- World Cup semi-finalist (France, 4th) 1.5 (650 min)
- World Cup Team of the Tournament 1.5
- Bundesliga Team of the Season 1.0
- DFL-Supercup winner 1.0 (started the final)

**Vinícius Júnior** (Real Madrid) — **2.25**
- Champions League top assister 2.25 (8, shared with Olise; the dataset shows 5)
- Real Madrid won nothing. Brazil went out of the World Cup before the semis. He is not in the LaLiga Team of the Season on the owner's source page.

**Lamine Yamal** (Barcelona) — **29.0**
- World Cup winner 12.0 (615 min)
- LaLiga champion 8.0 (2,268 min)
- LaLiga Best Player 5.0
- LaLiga top assister 1.5 (11)
- LaLiga Team of the Season 1.0
- Supercopa de España winner 1.0 (started the final)
- Copa del Rey semi-finalist 0.5 (450 min)

### CF/SS

**Ousmane Dembélé** (PSG) — **28.0**
- Champions League winner 12.0 (827 min)
- UNFP Ligue 1 Player of the Year 5.0
- Ligue 1 champion 4.0 (1,062 min = 35%, half)
- Super cups 3.0 (all three finals)
- Champions League Team of the Season 1.5
- World Cup semi-finalist (France, 4th) 1.5 (597 min)
- UNFP Ligue 1 Team of the Year 1.0
- Extras: Ligue 1 Goal of the Season · equalising penalty in the Champions League final · Man of the Match in the UEFA Super Cup

**Erling Haaland** (Manchester City) — **8.5**
- Premier League Golden Boot 3.0 (27)
- EFL Cup winner 2.0 (199 min: half, because the threshold is strict)
- World Cup Team of the Tournament 1.5
- PFA Premier League Team of the Year 1.0
- FA Cup winner 1.0 (started the final)
- Extras: European Golden Shoe runner-up (54 pts) · Norway did not reach the World Cup semi-finals (7 goals in the dataset)

**Harry Kane** (Bayern) — **21.5**
- Bundesliga champion 8.0 (2,382 min)
- DFB-Pokal winner 4.0 (537 min)
- Bundesliga top scorer 3.0 (36)
- Champions League semi-finalist 1.5 (1,039 min)
- Champions League Team of the Season 1.5
- World Cup semi-finalist (England, 3rd) 1.5 (653 min)
- Bundesliga Team of the Season 1.0
- DFL-Supercup winner 1.0 (started and scored)
- Extras: **European Golden Shoe winner** (72 pts, second time) · 14 Champions League goals (2nd to Mbappé)

**Lautaro Martínez** (Inter) — **18.5**
- Serie A champion 8.0 (2,178 min)
- World Cup finalist 4.5 (311 min, full)
- Serie A top scorer 3.0 (17)
- Coppa Italia winner 2.0 (111 min, half)
- Serie A Team of the Year 1.0
- Extras: Serie A Best Striker · scored in Argentina's 2-1 semi-final win over England (assist from Messi)

**Kylian Mbappé** (Real Madrid) — **16.0**
- Champions League top scorer 4.5 (15)
- World Cup Golden Boot 4.5 (10)
- LaLiga top scorer 3.0 (Pichichi, 25)
- World Cup semi-finalist (France, 4th) 1.5 (698 min)
- World Cup Team of the Tournament 1.5
- LaLiga Team of the Season 1.0
- Extras: first player to win the World Cup Golden Boot twice · World Cup Bronze Ball ◐ · European Golden Shoe 3rd (50 pts)

**Julián Quiñones** (Al-Qadsiah) — **2.1**
- Saudi Pro League top scorer 2.1 (33, ×0.7)
- King's Cup: Al-Qadsiah went out in the quarter-finals. Mexico did not reach the World Cup semis.
- Extras: Saudi Player of the Season nominee

**Ferran Torres** (Barcelona) — **21.5**
- World Cup winner 12.0 (283 min, full)
- LaLiga champion 8.0 (1,984 min)
- Supercopa de España winner 1.0 (substitute in the final, 66')
- Copa del Rey semi-finalist 0.5 (246 min)
- Extras: **scored the winning goal in the World Cup final** (106', as a substitute)

**Mikel Oyarzabal** (Real Sociedad) — **16.0**
- World Cup winner 12.0 (605 min)
- Copa del Rey winner 4.0 (479 min)
- Extras: scored in the World Cup semi-final win over France · 5 World Cup goals in the dataset

---

## 4. Summary table

| # | Player | Bonus | | # | Player | Bonus |
|---|---|---|---|---|---|---|
| 1 | Kvaratskhelia | 32.0 | | 20 | Upamecano | 18.5 |
| 2 | Fabián Ruiz | 31.0 | | 21 | Raya | 18.0 |
| 3 | Olise | 31.0 | | 22 | Rice | 18.0 |
| 4 | Yamal | 29.0 | | 23 | Dimarco | 17.5 |
| 5 | Dembélé | 28.0 | | 24 | Gabriel | 16.5 |
| 6 | Hakimi | 26.8 | | 25 | Saliba | 16.5 |
| 7 | Mendes | 25.5 | | 26 | Mbappé | 16.0 |
| 8 | Vitinha | 25.5 | | 27 | Oyarzabal | 16.0 |
| 9 | Pacho | 24.0 | | 28 | Luis Díaz | 15.5 |
| 10 | Rodri | 24.0 | | 29 | Cucurella | 14.0 |
| 11 | Pedri | 22.25 | | 30 | Messi (provisional) | 9.6 |
| 12 | Neves | 22.0 | | 31 | Haaland | 8.5 |
| 13 | Cubarsí | 21.5 | | 32 | Zabarnyi | 8.0 |
| 14 | Olmo | 21.5 | | 33 | Bruno Fernandes | 7.5 |
| 15 | Kane | 21.5 | | 34 | Bellingham | 3.0 |
| 16 | Ferran Torres | 21.5 | | 35 | Vinícius | 2.25 |
| 17 | Marquinhos | 20.5 | | 36 | Quiñones | 2.1 |
| 18 | Mané | 18.5 | | 37 | Vozinha | 1.5 |
| 19 | Lautaro Martínez | 18.5 | | | | |

The highest bonus is 32.0 and the median is about 18.5, so the scale stays close to the ≈30 target.

---

## 5. Decisions applied and what is still open

Applied from the owner's review:
1. **AFCON:** both teams are scored as finalists (3.6 each). No dependence on the CAF ruling or on the CAS appeal.
2. **MLS:** Messi's points come from the 2026 season (top scorer and top assister). His 2025 MVP, Best XI and MLS Cup title are mentioned as extras with no points.
3. **Champions League top assister:** Olise and Vinícius both count.
4. **LaLiga:** Best Player (Yamal) and Team of the Season come from the La Liga Awards page.
5. **Teams of the season:** the World Cup and Serie A lists come from the owner's links. For the Bundesliga I use the EA Sports Team of the Season on the Wikipedia Bundesliga page (Upamecano, Díaz, Kane and Olise are in it).
6. **Dataset vs. press figures** (Dimarco 17 vs 18 assists, Bruno 21 vs 20): no effect on any award.
7. **Thresholds:** applied strictly.
8. **Super cups and other trophies:** 1 point each, winners only, and only for players who played the final.
9. **Cup-final involvement for the table cups:** not researched further (the minutes rule is used).

Still open:
- **MLS 2026 is not finished.** Messi's 3.6 points depend on him finishing first in goals and tied first in assists (six players are tied on 14 assists). Re-check after MLS Cup (December).
- **Cubarsí and the LaLiga Team of the Season:** he gets 0, as decided (he is not among the 11 on the La Liga Awards page).
- **FA Cup and Finalissima:** the FA Cup is not in the sheet's data but counts as a 1-point trophy. The Finalissima was never played.

---

## Sources

- World Cup: [ESPN, Mbappé Golden Boot](https://www.espn.com/soccer/story/_/id/49397919/kylian-mbappe-wins-golden-boot-2026-world-cup-lionel-messi-goalless-final) · [Football360 awards list](https://football360.com.au/2026-fifa-world-cup-awards-winners/) · [Irish Times, Golden Ball](https://www.irishtimes.com/sport/soccer/2026/07/20/rodri-wins-world-cup-golden-ball-as-kylian-mbappe-wins-second-golden-boot/) · [Wikipedia](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup) · [Team of the Tournament template](https://en.wikipedia.org/wiki/Template:2026_FIFA_World_Cup_Team_of_the_Tournament) · [Planet Football stats leaders](https://www.planetfootball.com/stats-tables/2026-world-cup-stats-leaders-goals-assists-chances-created-dribbles)
- Champions League: [UEFA, 2025/26 winners](https://www.uefa.com/uefachampionsleague/news/02a5-20901454177c-738c0ac757df-1000--paris-win-champions-league-meet-the-2025-26-victors/) · [Team of the Season](https://www.uefa.com/uefachampionsleague/news/02a5-20c1d7d33d69-be4f6ab11b0a-1000--2025-26-uefa-champions-league-team-of-the-season/) · [season stats](https://www.uefa.com/uefachampionsleague/history/seasons/2026/statistics/) · [final Player of the Match](https://www.uefa.com/uefachampionsleague/news/02a5-20c0324a93c4-a269d65f5aeb-1000--vitinha-named-official-2026-uefa-champions-league-final-play/)
- AFCON: [Wikipedia](https://en.wikipedia.org/wiki/2025_Africa_Cup_of_Nations) · [CAF Best XI](https://www.cafonline.com/afcon2025/news/senegal-and-morocco-dominate-the-totalenergies-caf-afcon-morocco-2025-best-xi/)
- Premier League: [Squawka awards](https://www.squawka.com/en/features/2025-26-premier-league-awards-golden-boot-golden-glove-playmaker/) · [Premier League, Fernandes](https://www.premierleague.com/en/news/4662427/fernandes-wins-ea-sports-player-of-the-season-award) · [PFA Awards 2026](https://www.thepfa.com/news/2026/8/25/pfa-awards-2026-premier-league-winners)
- LaLiga: [La Liga Awards (Wikipedia)](https://en.wikipedia.org/wiki/La_Liga_Awards) · [Real Madrid, Pichichi](https://www.realmadrid.com/en-US/news/football/first-team/latest-news/mbappe-gana-el-trofeo-pichichi-2025-26-23-05-2026) · [Yahoo, 19-man Team of the Season](https://sports.yahoo.com/articles/official-six-barcelona-stars-named-152500214.html)
- Bundesliga: [Bundesliga.com, Olise Player of the Season](https://www.bundesliga.com/en/bundesliga/news/player-of-the-month-2025-26-vote-winners-ea-sports-olise-34233) · [Kane top scorer](https://www.bundesliga.com/en/bundesliga/news/top-scorers-2025-26-harry-kane-guirassy-schick-burkardt-kleindienst-32768) · [Golden Shoe](https://www.bundesliga.com/en/bundesliga/news/harry-kane-wins-golden-shoe-2025-26-bayern-munich-england-37552) · [Bundesliga Team of the Season (Wikipedia)](https://en.wikipedia.org/wiki/2025%E2%80%9326_Bundesliga#Team_of_the_Season)
- Serie A: [Inter, Dimarco MVP](https://www.inter.it/en/news/federico-dimarco-serie-a-mvp-2025-26) · [Serie A Team of the Year (Wikipedia)](https://en.wikipedia.org/wiki/Serie_A_Team_of_the_Year)
- Ligue 1: [PSG, UNFP Awards 2026](https://www.psg.fr/en/content/paris-saint-germain-shine-at-unfp-awards-2026-psg-news) · [Wikipedia](https://en.wikipedia.org/wiki/2025%E2%80%9326_Ligue_1)
- Saudi: [SPL Awards 2025-26](https://www.spl.com.sa/en/news/1069886/2025-26-rsl-awards-winners-felix-jesus-al-juwayr-al-elewa-celebrated) · [King's Cup](https://en.wikipedia.org/wiki/2025%E2%80%9326_King's_Cup_(Saudi_Arabia)) · [AFC Champions League Two final](https://en.wikipedia.org/wiki/2026_AFC_Champions_League_Two_final)
- Cups and super cups: [Copa del Rey](https://en.wikipedia.org/wiki/2025%E2%80%9326_Copa_del_Rey) · [DFB-Pokal final](https://en.wikipedia.org/wiki/2026_DFB-Pokal_final) · [Coppa Italia final](https://en.wikipedia.org/wiki/2026_Coppa_Italia_final) · [EFL Cup final](https://en.wikipedia.org/wiki/2026_EFL_Cup_final) · [FA Cup final](https://en.wikipedia.org/wiki/2026_FA_Cup_final) · [Supercopa 2026 final](https://en.wikipedia.org/wiki/2026_Supercopa_de_Espa%C3%B1a_final) · [UEFA Super Cup](https://en.wikipedia.org/wiki/2025_UEFA_Super_Cup) · [Intercontinental Cup](https://en.wikipedia.org/wiki/2025_FIFA_Intercontinental_Cup) · [Intercontinental Cup final details](https://en.wikipedia.org/wiki/2025_FIFA_Intercontinental_Cup_final#Details) · [Trophée des Champions](https://en.wikipedia.org/wiki/2025_Troph%C3%A9e_des_Champions) · [DFL-Supercup](https://en.wikipedia.org/wiki/2025_DFL-Supercup) · [Supercoppa](https://en.wikipedia.org/wiki/2025_Supercoppa_Italiana_final_(December)) · [Finalissima](https://www.football-espana.net/2026/03/28/conmebol-argentina-winners-2026-finalissima)
- MLS: [ESPN 2026 scoring table](https://www.espn.com/soccer/stats/_/league/USA.1/season/2026/view/scoring) · [2025 MLS season (Wikipedia)](https://en.wikipedia.org/wiki/2025_Major_League_Soccer_season) · [MLS, 2025 MVP](https://www.mlssoccer.com/news/inter-miami-s-lionel-messi-repeats-as-landon-donovan-mls-mvp)
- Cabo Verde at the World Cup: [Foot Africa](https://foot-africa.com/en/news/world-cup-2026-after-a-0-0-draw-against-saudi-arabia-cape-verde-makes-history-and-advances-to-the-round-of-32-1259137/)
