# Research note — intraday downside risk

## Protocol

This study asks how two simple one-step risk estimates respond to changing volatility. Before building the results, `config.json` fixed ETHUSDT,1–14January2024, five-minute bins,864 warm-up/history returns, EWMA decay0.94 and95%/99% levels. No settings were tuned after inspecting exceedances. This is a locally recorded protocol, not an externally registered experiment.

Trade records come from the official Binance Vision spot aggregate-trade archive. Each of the14 archives is verified against the pinned publisher checksum from TickLab. The loader checks ordering, duplicates, nonpositive/nonfinite quantities and prices, day boundaries and schema. For this sample there are no aggregate-ID gaps or empty bins; all last-trade ages at bar endpoints are at most30seconds.

Each five-minute bar contains trades before its exclusive endpoint. A trade exactly on the endpoint belongs to the next interval. The last trade in each bin defines its close. Returns are10000×log(next_close/current_close), continuous across midnight. There are4032 closes and4031 returns. The first864 returns seed the estimators, leaving3167 evaluated returns. Prediction starts4January00:05UTC, first target ends00:10UTC; the final target ends15January00:00UTC. For daily display, a boundary endpoint belongs to the date immediately preceding it, so the final observation is assigned to14January.

## Risk estimates

Let r_t be the target five-minute log return in bps and L_t=−r_t the loss. Forecasts for t use returns strictly before t.

**Historical:** VaR_t(c) is the empirical c quantile of the previous864 losses, using NumPy's linear interpolation. The window slides one return at a time. It contains three days of continuous five-minute history.

**Adaptive Gaussian:** initial variance is the mean squared training return, consistent with a zero-mean specification. Forecast VaR_t(c)=Phi_inverse(c)×sqrt(v_t). After observing r_t, set v_next=0.94×v_t+0.06×r_t². The target never enters its own variance or empirical quantile.

The EWMA structure is inspired by the [RiskMetrics Technical Document](https://www.msci.com/documents/10199/5915b101-4206-4ba0-aee2-3449d5c7e95a). The fixed0.94 decay here applies to five-minute steps and has an approximate half-life of11.2 intervals (56minutes). It is an illustrative choice, not an application of an optimized daily parameter to an equivalent horizon. Gaussian quantiles use Python's standard-library NormalDist. [SciPy's normal distribution reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html) provides the equivalent inverse-CDF definition.

## Scoring and interpretation

A breach is L_t>VaR_t(c). The target long-run breach rate is1−c. Exceedance counts, rates, longest consecutive breach streaks and largest excesses are descriptive, not statistical certification. The sample is too small and concentrated to establish stable tail behavior; no independent-coverage hypothesis-test claim is made.

Quantile loss uses u=L_t−VaR_t(c) and rho_c(u)=max(cu,(c−1)u). It evaluates the size and direction of quantile errors, rather than merely counting exceedances. It is reported in basis points and lower is better, compared at the same confidence level and on identical observations.

At95%, EWMA's quantile loss is2.096bps versus2.414 for historical; exceedance rates are5.05% and5.21%. At99%, EWMA scores0.659bps versus0.836, but exceeds its threshold1.55% of the time versus1.17% for historical. Thus a method can score better overall while recording more threshold breaches. These are empirical results without uncertainty intervals or a claim of statistical significance.

Full-period sampled-price drawdown reaches−11.99%. This context statistic uses the running maximum of all4032 closes and includes the warm-up segment; it is not an evaluation metric or realized strategy P&L. Daily realized volatility is sqrt(sum(r²)) over the evaluated intervals, with no annualization. The first evaluated day is partial; comparisons should account for its287 observations versus288 on later days.

## Limits

The data cover one cryptocurrency pair, one venue and two weeks. Last-trade prices are not midquotes or attainable execution prices. Discrete five-minute sampling misses intrabin extrema and can understate true peak-to-trough drawdown. Fees, spread, slippage, liquidity, latency, funding and market impact are absent. Normal tails omit skewness and fat-tail behavior; the empirical method has limited tail observations and can react slowly to regime shifts. There is no expected-shortfall estimate, portfolio diversification model or allocation recommendation.

Forecasts assume completed exchange-time bars are immediately available. Real feed delays and clock errors are not modeled. Ranking worst events is retrospective. The study does not assert that its parameters will remain calibrated or that a trading strategy is profitable.

## Reproducibility

The source manifest and protocol SHA256 digests are embedded in the report. `verify.py` compares every CSV row with the report, recalculates all model summaries and daily realized volatility, and verifies those digests. Unit tests independently check analytical formulas and future-data invariance. They do not constitute independent confirmation of data-provider correctness. Full reconstruction requires the pinned raw archives; CI instead checks saved results and application logic.
