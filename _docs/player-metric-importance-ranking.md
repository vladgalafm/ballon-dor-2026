# **Quantitative Evaluation and Importance Ranking of Position-Specific Football Metrics**

The quantitative assessment of player effectiveness in modern football analytics requires disentangling individual technical proficiency from surrounding tactical structures, team possession dominance, and short-term statistical noise. Outcome-based metrics, such as unadjusted goals conceded or raw clean sheets, frequently conflate collective defensive quality with individual performance. Modern empirical analytics addresses these analytical biases through expected value models, rate-based metrics, and context-isolated efficiency percentages.  
To establish an analytical hierarchy for the five position-specific metrics across seven positional groupings, each metric is evaluated against three core quantitative criteria:

> 1. Signal-to-noise ratio and multi-season repeatability, which measures how reliably a metric reflects underlying skill rather than transient variance.  
> 2. Tactical context independence, which isolates individual output from team possession share, match state, and defensive line height.  
> 3. Functional alignment with core positional objectives within contemporary tactical systems.

## **Goalkeeper Metric Evaluation and Importance Hierarchy**

Evaluating goalkeepers requires separating individual shot-stopping mechanics from the collective defensive performance of the backline. Goalkeepers operating behind permeable defenses face high shot volumes and higher-value opportunities, whereas those behind elite defensive units encounter minimal threat, distorting traditional counting statistics.  
The metric ranked highest for goalkeepers is Goals Prevented (+/-), which represents the definitive standard in shot-stopping evaluation. Calculated by subtracting actual goals conceded from post-shot expected goals (PSxG), this metric evaluates the placement, velocity, and trajectory of on-target shots faced. By isolating shot difficulty, Goals Prevented (+/-) measures pure shot-stopping quality independently of defensive volume. Saves (%) is ranked second; while it provides a useful measure of overall save efficiency, it treats central, low-velocity attempts identically to top-corner strikes, introducing variance. Accurate Long Balls (%) is ranked third, reflecting the modern goalkeeper’s essential role in bypassing high-pressing schemes and initiating first-phase build-up play.  
Conversely, Goals Against per 90 and Clean Sheets (%) are ranked fourth and fifth due to their heavy systemic confounding. Both metrics depend directly on team defensive structure, pressing intensity, and overall team quality. An elite goalkeeper behind a chaotic defense will concede a high rate of goals per 90 minutes, whereas a passive goalkeeper behind a dominant team can accumulate clean sheets without contributing positive shot-stopping value.

| Rank | Metric Name | Primary Analytical Utility |
| :---- | :---- | :---- |
| 1 | Goals Prevented, \+/- | Isolates shot-stopping proficiency from shot volume and defensive system strength. |
| 2 | Saves, % | Measures basic shot-stopping efficiency, unadjusted for shot trajectory or placement. |
| 3 | Accurate Long Balls, % | Evaluates long-range distribution capability and build-up contribution under pressure. |
| 4 | Goals Against, per 90 | Measures total defensive concessions; heavily confounded by team defensive line strength. |
| 5 | Clean Sheets, % | Team-level outcome statistic; exhibits low predictive signal for individual performance. |

## **Central Defender Metric Evaluation and Importance Hierarchy**

Central defenders must balance physical dominance in central defensive zones with composure and distribution range during initial build-up phases. Raw defensive action counts correlate inversely with team possession, making efficiency percentages far superior to raw volume totals.  
Aerial Duels Won (%) is ranked first for central defenders. Dominance in aerial contests is a highly stable, physical skill essential for defending cross delivery, open-play long balls, and defensive set pieces. Accurate Passes (%) is ranked second due to the critical nature of ball retention during primary build-up phases. A misplaced pass by a central defender carries an exceptionally high turnover cost, exposing the team to immediate central counter-attacks. Tackles Won (%) ranks third as an efficiency indicator, capturing 1v1 ground duel capabilities without rewarding unnecessary sliding attempts.  
Accurate Long Balls (%) ranks fourth, reflecting a central defender's capacity to switch play, break low blocks, or reach wide outlets under high structural pressure. Defensive Actions per 90 is ranked fifth. In quantitative analytics, high defensive action volume (combining tackles, interceptions, blocks, and clearances) primarily reflects that a player's team lacks possession or sustains persistent opposition pressure, rather than serving as an indicator of individual defensive quality.

| Rank | Metric Name | Primary Analytical Utility |
| :---- | :---- | :---- |
| 1 | Aerial Duels Won, % | Measures physical dominance in open-play box defending and set-piece situations. |
| 2 | Accurate Passes, % | Quantifies build-up stability and ball security during primary possession phases. |
| 3 | Tackles Won, % | Measures 1v1 ground defending efficiency without penalizing disciplined positioning. |
| 4 | Accurate Long Balls, % | Assesses long-range distribution, line-breaking capability, and play-switching ability. |
| 5 | Defensive Actions, per 90 | Quantifies total defensive volume; heavily distorted by team possession share. |

## **Full-Back and Wing-Back Metric Evaluation and Importance Hierarchy**

Modern full-backs and wing-backs operate as dual-function players, required to generate high offensive output along wide corridors while defending wide 1v1 engagements. Evaluating full-backs requires balancing high-value offensive chance creation with 1v1 defensive robustness.  
The top-ranked metric for full-backs and wing-backs is xG \+ xA per 90\. Because contemporary tactics rely heavily on full-backs for width, overlaps, and underlaps, measuring the underlying expected goal and assist value generated per 90 provides the clearest indicator of elite contribution to threat creation. Accurate Final Third Passes per 90 ranks second, quantifying territorial penetration and the ability to feed controlled passes into high-danger central areas. Ground Duels Won (%) ranks third as the essential wide defensive benchmark, assessing a full-back's ability to isolate opposing wingers during 1v1 wide transitions.  
Attacking Actions per 90 ranks fourth, serving as a broad volume metric that aggregates goals, assists, shots on target, dribbles, key passes, and crosses minus dispossessions. While useful for assessing involvement, it carries slight structural noise. Defensive Actions per 90 ranks fifth, as raw defensive interventions remain heavily confounded by team tactics, match state, and possession splits.

| Rank | Metric Name | Primary Analytical Utility |
| :---- | :---- | :---- |
| 1 | xG \+ xA, per 90 | Quantifies direct individual contribution to goal generation and chance creation. |
| 2 | Accurate Final Third Passes, per 90 | Measures territorial penetration and ability to sustain attack in advanced wide zones. |
| 3 | Ground Duels Won, % | Measures defensive efficiency in wide 1v1 isolations against opposing wingers. |
| 4 | Attacking Actions, per 90 | Aggregates general offensive involvement across dribbling, passing, and shooting. |
| 5 | Defensive Actions, per 90 | Measures defensive workload; biased by match state and opponent possession share. |

## **Defensive and Central Midfielder Metric Evaluation and Importance Hierarchy**

Defensive and central midfielders serve as the structural anchor of team play, responsible for possession recycling, press resistance, and central transition defense. Metrics for this role must prioritize ball security under physical pressure and ground duel control.  
Press Resistance x Ground Engagement Win Rate (%) is ranked first for holding midfielders. This composite interaction evaluates ball retention under pressure alongside physical ground duel winning percentage. It effectively captures central midfield dominance by balancing possession security with defensive duel execution. Accurate Passes (%) ranks second, capturing pass reliability and tempo control during build-up play. Midfielders operating in deep central zones cannot afford possession losses, making high passing efficiency essential.  
Accurate Final Third Passes per 90 ranks third, evaluating a midfielder's capacity to break lines and transition play into intermediate attacking zones. Defensive Actions per 90 ranks fourth. While defensive volume carries greater contextual validity for a screening holding midfielder than for a central defender, it remains subject to possession variance. Attacking Actions per 90 ranks fifth, as direct final-third execution represents a secondary functional responsibility for deep-lying midfielders.

| Rank | Metric Name | Primary Analytical Utility |
| :---- | :---- | :---- |
| 1 | Press Resistance x Ground Engagement Win Rate, % | Synthesizes ball retention under intense pressure with ground duel dominance. |
| 2 | Accurate Passes, % | Measures overall pass reliability, possession recycling, and tempo control. |
| 3 | Accurate Final Third Passes, per 90 | Measures line-breaking vision and progressive distribution into attacking zones. |
| 4 | Defensive Actions, per 90 | Measures central screening volume, interceptions, and transition defense. |
| 5 | Attacking Actions, per 90 | Evaluates total offensive involvement; lower tactical relevance for holding profiles. |

## **Central and Attacking Midfielder Metric Evaluation and Importance Hierarchy**

Central and attacking midfielders are tasked with unbalancing organized defenses through creative pass selection, half-space navigation, and central goal threat. Evaluating these playmakers requires prioritizing creative chance generation over raw pass volume.  
The paramount metric for central and attacking midfielders is xA per 90\. Expected Assists measures the quality of chances generated based on pass location, trajectory, and end-point, isolating true creative vision independently of teammate finishing skill. Press Resistance x Ground Engagement Win Rate (%) is ranked second, capturing an attacking midfielder's ability to maintain possession and win ground duels within densely populated half-spaces under heavy pressing intensity.  
Accurate Final Third Passes per 90 ranks third, capturing high-frequency territorial dominance and pass delivery into the penalty box. Goals per 90 ranks fourth; direct goal scoring from midfield provides elite strategic value, but goal totals carry higher variance than expected assist generation. Attacking Actions per 90 ranks fifth as a broad composite volume measure.

| Rank | Metric Name | Primary Analytical Utility |
| :---- | :---- | :---- |
| 1 | xA, per 90 | Highly stable measure of underlying chance creation, independent of teammate finishing. |
| 2 | Press Resistance x Ground Engagement Win Rate, % | Evaluates ball control and physical duel winning in tight half-space zones. |
| 3 | Accurate Final Third Passes, per 90 | Measures volume and accuracy of high-zone penetrative passing. |
| 4 | Goals, per 90 | Direct measure of central scoring threat; secondary to creative chance generation. |
| 5 | Attacking Actions, per 90 | Composite volume metric of total attacking involvement; carries secondary noise. |

## **Winger Metric Evaluation and Importance Hierarchy**

Modern wingers operate as wide inverted forwards and primary creators. Their evaluation rests on direct goal scoring, expected chance creation, and 1v1 takeover efficiency to unbalance opposition defensive blocks.  
Goals per 90 is ranked first for wingers, reflecting their modern primary role as inverted goal scorers attacking central box zones from wide starting positions. xA per 90 ranks second, capturing chance creation from wide corridors, including cutbacks, low crosses, and through-balls. Dribbles Success (%) ranks third. High 1v1 dribble efficiency measures a winger's capacity to eliminate wide defenders, generate numerical overloads, and break low blocks without incurring frequent turnovers.  
Attacking Actions per 90 ranks fourth, measuring high-volume involvement across offensive phases. Goals per Shot is ranked fifth. Unadjusted shot conversion efficiency is an extremely volatile metric driven by short-term variance. Shot conversion rates over small samples regress rapidly to historical league averages, making raw goal output per 90 and expected goal models significantly more predictive of elite winger quality.

| Rank | Metric Name | Primary Analytical Utility |
| :---- | :---- | :---- |
| 1 | Goals, per 90 | Primary output metric for modern wide inverted forwards and goal threats. |
| 2 | xA, per 90 | Measures underlying creative output, cutback quality, and crossing threat. |
| 3 | Dribbles Success, % | Measures 1v1 isolation efficiency and ability to unbalance set defenses. |
| 4 | Attacking Actions, per 90 | Aggregates general offensive activity and transition involvement. |
| 5 | Goals, per Shot | Unadjusted conversion rate; highly volatile and subject to regression to the mean. |

## **Centre Forward and Second Striker Metric Evaluation and Importance Hierarchy**

Centre forwards and second strikers are evaluated primarily on goal scoring output, box presence, and creative link-up play. Secondary traits include physical target capability and holistic involvement in attacking sequences.  
Goals per 90 is the top-ranked metric for strikers, representing the fundamental objective of converting team chance creation into actual goals. xA per 90 ranks second, measuring link-up lay-offs, hold-up distribution, and chance creation for surrounding inverted wingers or attacking midfielders. Attacking Actions per 90 ranks third, capturing total box presence, shot generation, key passing, and pressing retention while penalizing dispossessions.  
Aerial Duels Won (%) ranks fourth, evaluating target-man utility, long-ball hold-up capability, and aerial conversion from wide crosses. Goals per Shot ranks fifth. Unadjusted conversion efficiency contains substantial seasonal noise. Strikers who maintain high shot volume and high underlying expected goals per 90 consistently outperform those relying on temporary finishing spikes over small shot samples.

| Rank | Metric Name | Primary Analytical Utility |
| :---- | :---- | :---- |
| 1 | Goals, per 90 | Primary measure of striker effectiveness and net scoring output. |
| 2 | xA, per 90 | Evaluates link-up play, hold-up capability, and creative passing to teammates. |
| 3 | Attacking Actions, per 90 | Captures total box presence, shot involvement, and overall offensive engagement. |
| 4 | Aerial Duels Won, % | Evaluates target-man aerial dominance, long-ball outlet success, and set-piece threat. |
| 5 | Goals, per Shot | Raw conversion rate; high variance and heavily influenced by short-term luck. |

## **Synthesis of Positional Metric Importance Ranks**

Synthesizing all positional rankings reveals overarching statistical patterns across quantitative evaluation models. Expected value metrics (Goals Prevented, xG \+ xA, xA) and context-isolated efficiency percentages consistently rank highest across all positional groups, whereas raw defensive volume counts and unadjusted conversion ratios rank lowest.

| Positional Group | Rank 1 (Most Critical) | Rank 2 | Rank 3 | Rank 4 | Rank 5 (Least Critical) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **GK** | Goals Prevented, \+/- | Saves, % | Accurate Long Balls, % | Goals Against, per 90 | Clean Sheets, % |
| **CB** | Aerial Duels Won, % | Accurate Passes, % | Tackles Won, % | Accurate Long Balls, % | Defensive Actions, per 90 |
| **LB/RB/LWB/RWB** | xG \+ xA, per 90 | Accurate Final 3rd Passes, per 90 | Ground Duels Won, % | Attacking Actions, per 90 | Defensive Actions, per 90 |
| **DMC/MC** | Press Resistance x Ground Engagement, % | Accurate Passes, % | Accurate Final 3rd Passes, per 90 | Defensive Actions, per 90 | Attacking Actions, per 90 |
| **MC/AMC** | xA, per 90 | Press Resistance x Ground Engagement, % | Accurate Final 3rd Passes, per 90 | Goals, per 90 | Attacking Actions, per 90 |
| **LW/RW** | Goals, per 90 | xA, per 90 | Dribbles Success, % | Attacking Actions, per 90 | Goals, per Shot |
| **CF/SS** | Goals, per 90 | xA, per 90 | Attacking Actions, per 90 | Aerial Duels Won, % | Goals, per Shot |

## **Conclusions and Analytical Implications**

The relative importance rankings established across all seven tactical positions illustrate three primary principles for modern player evaluation:  
Isolation of individual performance from team noise remains the most critical requirement in talent assessment. Metrics such as Goals Prevented (+/-) for goalkeepers and Expected Assists (xA) for playmakers effectively remove team-level bias, providing highly stable indicators of true skill.  
Rate-based efficiency metrics and interaction formulas demonstrate far greater signal than raw volume counts. Raw action totals, particularly Defensive Actions per 90, reflect match state and team possession percentages rather than individual defensive capability.  
Unadjusted conversion rates, such as Goals per Shot, are dominated by short-term variance and exhibit rapid regression to the mean. Predictive frameworks should prioritize underlying shot volume, xG generation, and per-90 scoring rates over short-term conversion spikes.