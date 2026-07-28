export interface TrackerRow {
  date: string;
  league: string;
  home: string;
  away: string;
  market: string;
  selection: string;
  best_odds: string;
  book: string;
  model_prob: string;
  true_implied: string;
  edge: string;
  ev: string;
  stake: string;
  bankroll_before: string;
  status: string;
  clv: string;
}

export interface Stats {
  total_bets: number;
  won: number;
  lost: number;
  push: number;
  open: number;
  hit_rate: number;
  total_staked: number;
  total_returned: number;
  pnl: number;
  roi: number;
  current_bankroll: number;
  // By league
  league_stats: Record<string, { bets: number; won: number; returned: number }>;
  // By market
  market_stats: Record<string, { bets: number; won: number; returned: number }>;
  // Daily P&L
  daily_pnl: Array<{ date: string; pnl: number; cumulative: number }>;
}

function parseCSV(csv: string): TrackerRow[] {
  const lines = csv.trim().split('\n');
  if (lines.length < 2) return [];
  const headers = lines[0].split(',');
  return lines.slice(1).map(line => {
    const values = line.split(',');
    const obj: any = {};
    headers.forEach((h, i) => { obj[h.trim()] = (values[i] || '').trim(); });
    return obj as TrackerRow;
  });
}

export function computeStats(rows: TrackerRow[], startBankroll = 100): Stats {
  const settled = rows.filter(r => r.status !== 'open' && r.stake !== '0');
  const openBets = rows.filter(r => r.status === 'open' && r.stake !== '0');

  const won = settled.filter(r => r.status === 'won').length;
  const lost = settled.filter(r => r.status === 'lost').length;
  const push = settled.filter(r => r.status === 'push').length;

  let totalStaked = 0;
  let totalReturned = 0;
  const leagueStats: Record<string, any> = {};
  const marketStats: Record<string, any> = {};
  const dailyPnlMap: Record<string, number> = {};

  for (const row of settled) {
    const stake = parseFloat(row.stake) || 0;
    const odds = parseFloat(row.best_odds) || 0;
    totalStaked += stake;

    let returned = 0;
    if (row.status === 'won') returned = stake * odds;
    else if (row.status === 'push') returned = stake;
    totalReturned += returned;

    // League stats
    const lg = row.league || 'Unknown';
    if (!leagueStats[lg]) leagueStats[lg] = { bets: 0, won: 0, returned: 0 };
    leagueStats[lg].bets++;
    if (row.status === 'won') leagueStats[lg].won++;
    leagueStats[lg].returned += returned;

    // Market stats
    const mk = row.market || 'Unknown';
    if (!marketStats[mk]) marketStats[mk] = { bets: 0, won: 0, returned: 0 };
    marketStats[mk].bets++;
    if (row.status === 'won') marketStats[mk].won++;
    marketStats[mk].returned += returned;

    // Daily P&L
    const date = row.date || '';
    if (!dailyPnlMap[date]) dailyPnlMap[date] = 0;
    dailyPnlMap[date] += (returned - stake);
  }

  const pnl = totalReturned - totalStaked;
  const currentBR = startBankroll + pnl;
  const total = settled.length;

  // Build cumulative P&L
  let cum = startBankroll;
  const dailyPnl = Object.entries(dailyPnlMap)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([date, pnl]) => {
      cum += pnl;
      return { date, pnl: Math.round(pnl * 100) / 100, cumulative: Math.round(cum * 100) / 100 };
    });

  return {
    total_bets: settled.length,
    won,
    lost,
    push,
    open: openBets.length,
    hit_rate: total > 0 ? Math.round((won / (won + lost)) * 1000) / 10 : 0,
    total_staked: Math.round(totalStaked * 100) / 100,
    total_returned: Math.round(totalReturned * 100) / 100,
    pnl: Math.round(pnl * 100) / 100,
    roi: totalStaked > 0 ? Math.round((pnl / totalStaked) * 1000) / 10 : 0,
    current_bankroll: Math.round(currentBR * 100) / 100,
    league_stats: leagueStats,
    market_stats: marketStats,
    daily_pnl: dailyPnl,
  };
}
