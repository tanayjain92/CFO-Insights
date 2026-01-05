# Apple Financial Glossary (For 2009–2024 Dataset)

This glossary explains the key financial metrics used in the Apple 2009–2024 annual dataset.  
It’s written in CFO-friendly language and meant to support RAG lookups and natural-language explanations.

> **Units:**  
> - Any column ending in `_millions` is in **millions of USD**.  
> - Ratios like `gross_margin`, `net_profit_margin`, `current_ratio`, `debt_to_assets_ratio` are **unitless** (fractions).  
> - The model can convert them to percentages when explaining them.

---

## Year (`year`)

**What it is:**  
The fiscal year of Apple’s financial results (e.g., 2010, 2015, 2024). Each row in the dataset is one fiscal year.

**How to think about it:**  
Use `year` as the time axis when looking at long-term trends, growth, or cyclic patterns in Apple’s performance.

---

## Revenue (`revenue_millions`)

**What it is:**  
Apple’s total sales for the year, in millions of dollars. This includes all products and services sold.

**Why it matters:**  
- Top-line indicator of business scale and demand for Apple’s ecosystem (iPhone, Mac, Services, etc.).  
- Strong, consistent revenue growth usually signals healthy product–market fit and pricing power.

**How to interpret trends:**  
- **Rising revenue** → Apple is selling more or charging more (or both).  
- **Flat or declining revenue** → possible saturation, competitive pressure, or macro headwinds.

---

## Gross Profit (`gross_profit_millions`)

**What it is:**  
Revenue **minus** the direct costs of making and delivering products/services (cost of goods sold). Reported in millions.

**Why it matters:**  
- Shows how much money is left after paying for production and delivery, before operating expenses.  
- A higher gross profit gives Apple more room to invest in R&D, marketing, and ecosystem expansion.

**How to interpret trends:**  
- If **revenue grows faster than gross profit**, Apple’s cost structure may be worsening.  
- If **gross profit grows faster than revenue**, margins are improving (better pricing, mix, or cost efficiency).

---

## Gross Margin (`gross_margin`)

**What it is:**  
Gross profit divided by revenue. Stored as a **decimal fraction** in the cleaned data (e.g., 0.38 for 38%).

**Why it matters:**  
- Captures Apple’s pricing power and cost efficiency at the product level.  
- High/stable gross margins are a hallmark of Apple’s premium positioning.

**How to interpret trends:**  
- **Rising gross margin** → more profitable mix (e.g., Services share up, premium devices, cost improvements).  
- **Falling gross margin** → more promotional activity, higher costs, or weaker pricing.

---

## Operating Income (`op_income_millions`)

**What it is:**  
Profit from Apple’s core operations:  
> Gross profit − operating expenses (R&D, SG&A, etc.).  

Reported in millions of dollars.

**Why it matters:**  
- Reflects how efficiently Apple turns gross profit into operating profit after funding its operating structure.  
- Sits between gross profit and net income in the P&L.

**How to interpret trends:**  
- Compare operating income growth to revenue growth.  
- If operating income grows faster than revenue, Apple is gaining operating leverage.

---

## EBITDA (`ebitda_millions`)

**What it is:**  
Earnings **before** interest, taxes, depreciation, and amortization, in millions.

**Why it matters:**  
- Approximation of cash-like operating earnings, before capital structure and accounting adjustments.  
- Useful for comparing profitability across companies or time periods.

**How to interpret trends:**  
- Rising EBITDA with stable capex can indicate strong underlying cash generation.  
- Watch EBITDA margin (EBITDA / revenue) to see how efficient the business is becoming.

---

## Net Income (`net_income_millions`)

**What it is:**  
Apple’s **bottom-line** profit after all expenses: operating costs, interest, taxes, and other items. In millions.

**Why it matters:**  
- The ultimate profit metric—this is what feeds retained earnings and supports dividends and buybacks.  
- Often compared to revenue via **net profit margin**.

**How to interpret trends:**  
- Net income can move differently from revenue due to tax, interest, or one-offs.  
- Sustained net income growth is a strong indicator of long-term value creation.

---

## Earnings Per Share (`eps`)

**What it is:**  
Net income divided by the weighted average number of shares outstanding. EPS is per share, in dollars.

**Why it matters:**  
- Connects company-wide profit to the **individual shareholder level**.  
- Buybacks can increase EPS even if net income is flat (fewer shares).

**How to interpret trends:**  
- Compare EPS growth to net income growth.
  - If **EPS grows faster** than net income → share count is shrinking via buybacks.  
  - If **EPS lags** net income → share count is growing or dilution is happening.

---

## Shares Outstanding (`shares_outstanding`)

**What it is:**  
Approximate number of Apple shares currently held by investors, in units (not millions).

**Why it matters:**  
- Used to convert company-level metrics into per-share metrics (EPS, market cap per share).  
- Buybacks **reduce** shares outstanding, boosting EPS and equity value per share.

**How to interpret trends:**  
- **Declining shares outstanding** → Apple is actively repurchasing stock.  
- **Flat or rising** → little buyback activity or share issuance.

---

## Total Assets (`total_assets_millions`)

**What it is:**  
The total value of everything Apple owns or controls—cash, receivables, inventory, PPE, intangibles—reported in millions.

**Why it matters:**  
- Gives a sense of scale and capital intensity.  
- Used in leverage and efficiency ratios like **debt_to_assets_ratio**.

**How to interpret trends:**  
- Faster asset growth than revenue may suggest heavier capital investment or acquisitions.  
- Asset-light growth (revenue growing faster than assets) can be attractive to investors.

---

## Cash on Hand (`cash_on_hand_millions`)

**What it is:**  
Cash and cash-equivalents (and sometimes marketable securities, depending on the source), in millions.

**Why it matters:**  
- Indicates liquidity and financial flexibility.  
- A strong cash position gives Apple room for:
  - R&D and capex  
  - M&A  
  - Buybacks and dividends

**How to interpret trends:**  
- High or rising cash can be a buffer against downturns and fuel for shareholder returns.  
- Persistent large cash balances can also raise “capital allocation” questions.

---

## Total Liabilities (`total_liabilities_millions`)

**What it is:**  
All obligations Apple owes: current liabilities + long-term liabilities, in millions.

**Why it matters:**  
- Part of the capital structure; used to assess leverage and risk.  
- Combined with assets to compute metrics like **current_ratio** and **debt_to_assets_ratio** (when using debt subset).

**How to interpret trends:**  
- Rising liabilities need to be understood in context: funding growth vs. rising risk.

---

## Long-Term Debt (`long_term_debt_millions`)

**What it is:**  
Borrowings and debt obligations that are due in more than one year, in millions.

**Why it matters:**  
- Indicates how much leverage Apple uses over the long term.  
- Debt can be used to fund buybacks and investments, especially when interest rates are favorable.

**How to interpret trends:**  
- Higher long-term debt increases financial risk but can be accretive if used wisely.  
- Compare long-term debt to total assets and cash.

---

## Net Profit Margin (`net_profit_margin`)

**What it is:**  
Net income divided by revenue, stored as a decimal (e.g., 0.25 for 25%).

**Why it matters:**  
- Shows how much of each dollar of revenue ultimately becomes profit.  
- Combines both operating efficiency and non-operating effects (taxes, interest).

**How to interpret trends:**  
- Rising net profit margin → Apple is keeping more of every revenue dollar.  
- Falling net profit margin → higher costs, tax drag, or other headwinds.

---

## Current Ratio (`current_ratio`)

**What it is:**  
Total assets divided by total liabilities (in this dataset’s engineered feature).  
> Note: In classical finance, “current ratio” is usually current assets / current liabilities; here it’s a broader proxy for solvency.

**Why it matters:**  
- Indicates how comfortably Apple’s asset base covers its liabilities.  
- A higher ratio means more headroom.

**How to interpret trends:**  
- Rising ratio → balance sheet is strengthening relative to obligations.  
- Very low ratio for a long period could be a red flag in other businesses; for Apple, needs broader context (cash, cash flow, etc.).

---

## Debt-to-Assets Ratio (`debt_to_assets_ratio`)

**What it is:**  
Long-term debt divided by total assets (both in millions).  
Represents the share of Apple’s assets financed by long-term debt.

**Why it matters:**  
- Classic leverage indicator.  
- Higher values mean more financial risk but also potentially more return on equity if used effectively.

**How to interpret trends:**  
- Rising ratio → Apple is relying more on debt financing.  
- Falling ratio → deleveraging or asset growth outpacing debt growth.

---

## P/E Ratio (`pe_ratio`)

**What it is:**  
Price-to-earnings ratio:  
> Share price / earnings per share (EPS).

**Why it matters:**  
- Rough gauge of how richly the market is valuing Apple’s earnings.  
- High P/E can signal strong growth expectations; low P/E can signal skepticism or a value opportunity.

**How to interpret trends:**  
- Rising P/E with rising earnings → strong confidence from investors.  
- Rising P/E with flat or falling earnings → valuation stretch, more risk if expectations reset.

---

## Using These Metrics Together

When interpreting Apple’s performance over time, it’s usually best to look at **several metrics together**, for example:

- **Growth story:** revenue_millions, net_income_millions, eps  
- **Profitability quality:** gross_margin, net_profit_margin  
- **Balance sheet strength:** cash_on_hand_millions, debt_to_assets_ratio, current_ratio  
- **Shareholder value:** eps, shares_outstanding, pe_ratio

For explanations, you can combine:

- A **definition** (what the metric is)  
- A **CFO lens** (why it matters strategically)  
- A **trend view** (how it changed from year A to year B and why that’s important)
