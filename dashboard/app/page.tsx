'use client';

import { useState, useEffect } from 'react';
import { computeStats, type Stats, type TrackerRow } from '@/lib/data';

const TRACKER_URL = '/data/tracker.csv';

async function loadData(): Promise<{ rows: TrackerRow[]; stats: Stats }> {
  try {
    const res = await fetch(TRACKER_URL);
    const csv = await res.text();
    const lines = csv.trim().split('\n');
    const headers = lines[0].split(',');
    const rows: TrackerRow[] = lines.slice(1).map(line => {
      const values = line.split(',');
      const obj: any = {};
      headers.forEach((h, i) => { obj[h.trim()] = (values[i] || '').trim(); });
      return obj;
    });
    const stats = computeStats(rows);
    return { rows, stats };
  } catch {
    return { rows: [], stats: computeStats([]) };
  }
}

export default function Home() {
  const [data, setData] = useState<{ rows: TrackerRow[]; stats: Stats } | null>(null);

  useEffect(() => { loadData().then(setData); }, []);

  if (!data) return <div style={{ padding: '2rem', textAlign: 'center', color: '#6b6b80' }}>Loading...</div>;

  const { rows, stats } = data;
  const settled = rows.filter(r => r.status !== 'open' && r.stake !== '0');
  const open = rows.filter(r => r.status === 'open' && r.stake !== '0');

  const total = settled.length + open.length;
  const winPct = settled.length > 0 ? Math.round(stats.won / (stats.won + stats.lost) * 1000) / 10 : 0;

  return (
    <div>
      {/* Header */}
      <header className="header">
        <div>
          <h1>⚽ <span>Football Betting Model</span></h1>
          <div style={{ fontSize: '0.75rem', color: '#6b6b80', marginTop: 4 }}>
            15 leagues • Poisson analysis • Value betting
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          {open.length > 0 && <span className="badge badge-live">● {open.length} Live</span>}
          <span className="badge badge-paper">📋 Paper Only</span>
        </div>
      </header>

      <div className="container" style={{ padding: '0 1.5rem' }}>
        {/* Key Stats */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="label">Current Bankroll</div>
            <div className={`value ${stats.pnl >= 0 ? 'value-green' : 'value-red'}`}>
              ${stats.current_bankroll.toFixed(2)}
            </div>
            <div className="sub">Started: $100.00</div>
          </div>

          <div className="stat-card">
            <div className="label">Total P&L</div>
            <div className={`value ${stats.pnl >= 0 ? 'value-green' : 'value-red'}`}>
              {stats.pnl >= 0 ? '+' : ''}{stats.pnl.toFixed(2)}
            </div>
            <div className="sub">ROI: {stats.roi}%</div>
          </div>

          <div className="stat-card">
            <div className="label">Hit Rate</div>
            <div className="value">{winPct}%</div>
            <div className="sub">{stats.won}W • {stats.lost}L • {stats.push}Push</div>
          </div>

          <div className="stat-card">
            <div className="label">Total Bets</div>
            <div className="value">{total}</div>
            <div className="sub">{settled.length} settled • {open.length} open</div>
          </div>

          <div className="stat-card">
            <div className="label">Total Staked</div>
            <div className="value">${stats.total_staked.toFixed(2)}</div>
            <div className="sub">Returned: ${stats.total_returned.toFixed(2)}</div>
          </div>
        </div>

        {/* Progress Bar */}
        <div style={{ margin: '1.5rem 0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, fontSize: '0.78rem', color: '#6b6b80' }}>
            <span>{settled.length} settled</span>
            <span>{total} total</span>
          </div>
          <div className="progress-bar">
            {stats.won > 0 && (
              <span className="progress-fill progress-won" style={{
                width: `${(stats.won / total) * 100}%`,
                display: 'inline-block',
              }} />
            )}
            {stats.lost > 0 && (
              <span className="progress-fill progress-lost" style={{
                width: `${(stats.lost / total) * 100}%`,
                display: 'inline-block',
              }} />
            )}
            {stats.push > 0 && (
              <span className="progress-fill progress-push" style={{
                width: `${(stats.push / total) * 100}%`,
                display: 'inline-block',
              }} />
            )}
            {open.length > 0 && (
              <span className="progress-fill progress-open" style={{
                width: `${(open.length / total) * 100}%`,
                display: 'inline-block',
              }} />
            )}
          </div>
          <div style={{ display: 'flex', gap: 16, marginTop: 8, fontSize: '0.75rem', color: '#6b6b80' }}>
            <span>🟢 Won: {stats.won}</span>
            <span>🔴 Lost: {stats.lost}</span>
            <span>🟡 Push: {stats.push}</span>
            <span>🔵 Open: {open.length}</span>
          </div>
        </div>

        {/* Two Column: League + Market */}
        <div className="two-col">
          {/* League Breakdown */}
          <div className="section-card">
            <h2>🏆 By League</h2>
            {Object.entries(stats.league_stats)
              .sort(([, a], [, b]) => b.bets - a.bets)
              .map(([league, ls]) => {
                const lPnl = ls.returned - (ls.bets * 0.01); // rough
                return (
                  <div key={league} className="league-row">
                    <span className="league-name">{league}</span>
                    <div className="league-stats">
                      <span>{ls.won}/{ls.bets} won</span>
                      <span className={`league-pnl ${ls.returned - ls.bets >= 0 ? 'value-green' : 'value-red'}`}>
                        {Math.round(ls.returned * 100) / 100}
                      </span>
                    </div>
                  </div>
                );
              })}
            {Object.keys(stats.league_stats).length === 0 && (
              <div style={{ color: '#6b6b80', fontSize: '0.85rem' }}>No bets placed yet</div>
            )}
          </div>

          {/* Market Breakdown */}
          <div className="section-card">
            <h2>📊 By Market</h2>
            {Object.entries(stats.market_stats)
              .sort(([, a], [, b]) => b.bets - a.bets)
              .map(([market, ms]) => (
                <div key={market} className="league-row">
                  <span className="league-name">{market}</span>
                  <div className="league-stats">
                    <span>{ms.won}/{ms.bets} won</span>
                    <span className={`league-pnl ${ms.returned - ms.bets >= 0 ? 'value-green' : 'value-red'}`}>
                      {Math.round(ms.returned * 100) / 100}
                    </span>
                  </div>
                </div>
              ))}
            {Object.keys(stats.market_stats).length === 0 && (
              <div style={{ color: '#6b6b80', fontSize: '0.85rem' }}>No bets placed yet</div>
            )}
          </div>
        </div>

        {/* Cumulative P&L Chart (text-based) */}
        {stats.daily_pnl.length > 0 && (
          <div className="section-card" style={{ marginTop: '1.5rem' }}>
            <h2>📈 Cumulative P&L</h2>
            <div style={{ display: 'flex', gap: 4, alignItems: 'flex-end', height: 120, paddingTop: 8 }}>
              {stats.daily_pnl.map((day, i) => {
                const minBR = Math.min(80, ...stats.daily_pnl.map(d => d.cumulative));
                const maxBR = Math.max(120, ...stats.daily_pnl.map(d => d.cumulative));
                const range = maxBR - minBR;
                const height = range > 0 ? ((day.cumulative - minBR) / range) * 100 : 50;
                return (
                  <div key={i} style={{
                    flex: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'flex-end',
                    height: '100%',
                  }}>
                    <div style={{
                      width: '100%',
                      maxWidth: 30,
                      height: `${Math.max(4, height)}%`,
                      background: day.cumulative >= 100 ? '#22c55e' : '#ef4444',
                      borderRadius: '3px 3px 0 0',
                      opacity: 0.8,
                    }} />
                    <span style={{ fontSize: '0.55rem', color: '#6b6b80', marginTop: 4, transform: 'rotate(-45deg)', transformOrigin: 'top left', whiteSpace: 'nowrap' }}>
                      {day.date.slice(5)}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Recent Bets Table */}
        <div className="section-card" style={{ marginTop: '1.5rem' }}>
          <h2>📝 Recent Bets</h2>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>League</th>
                  <th>Match</th>
                  <th>Market</th>
                  <th>Pick</th>
                  <th>Odds</th>
                  <th>Stake</th>
                  <th>Result</th>
                </tr>
              </thead>
              <tbody>
                {[...rows].reverse().slice(0, 20).map((row, i) => (
                  <tr key={i}>
                    <td>{row.date}</td>
                    <td style={{ fontSize: '0.75rem', color: '#6b6b80' }}>{row.league}</td>
                    <td>{row.home} vs {row.away}</td>
                    <td>{row.market}</td>
                    <td>{row.selection}</td>
                    <td>{row.best_odds}</td>
                    <td>${row.stake}</td>
                    <td>
                      <span className={`status-badge status-${row.status}`}>
                        {row.status.toUpperCase()}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="disclaimer">
          ⚠️ <strong>Paper trading only.</strong> This is a research model for educational purposes.
          Historical performance does not guarantee future results. Gamble responsibly.
          If you or someone you know has a gambling problem, call 1-800-GAMBLER.
        </div>
      </div>

      {/* Footer */}
      <div className="footer">
        <p>Automated daily at 06:00 UTC (picks) & 22:00 UTC (results) • <a href="https://github.com">View on GitHub</a></p>
        <p style={{ marginTop: 4 }}>15 European leagues • Poisson model • Value betting • 30-day paper test</p>
      </div>
    </div>
  );
}
