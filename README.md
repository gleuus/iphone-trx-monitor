# iPhone Duo TRX monitoring — experimental

This experimental GitHub Actions checker looks for **512GB or 1TB iPhone Duo in Star White or Night Sky**, specifically on the public InStock Radar page for **Apple The Exchange TRX**. **256GB is excluded.** It is not an Apple inventory API and **does not confirm Apple's live checkout pickup eligibility**. Its Telegram alerts are labelled *possible / unverified* and you must verify with Apple before travelling or purchasing.

The parser requires a clearly labelled in-stock status beside an exact configuration. Unknown or contradictory formats trigger no alert. If the source page changes its layout, stops publishing free stock status, or blocks automated access, monitoring will not be reliable. GitHub's free scheduled jobs can be delayed and five-minute sampling can miss brief restocks. The workflow may send repeated alerts while inventory remains reported in stock.

## Setup from iPhone
1. Create a public GitHub repository.
2. Add `check_stock.py` in the root and `.github/workflows/stock.yml` at the exact path. On mobile, GitHub's web editor can create files by path.
3. In repository **Settings → Secrets and variables → Actions → New repository secret**, add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`. Never paste credentials into code or chats.
4. Under **Actions → TRX iPhone Duo Stock Watch**, select **Run workflow** and inspect logs.
5. Disable the workflow if you no longer want it to run.

**Coverage:** Star White 512GB, Star White 1TB, Night Sky 512GB, Night Sky 1TB. This tool is separate from any hourly ChatGPT stock availability notification.
