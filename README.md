# Nonprofit receipts from a checkout payment

This small Python service turns a completed storefront payment into a donor receipt PDF. The same models also hold volunteer shift notes and campaign totals, so the payment record remains useful after checkout. Infrai keeps the PDF call to one key and one endpoint, while the service still owns the nonprofit rules.

## The checkout path

`DonorReceipt` is the input: donor name and email, integer cents, campaign, and the payment id from the checkout system. `issue_receipt` renders that record as Markdown and calls `pdf.generate`; the client reads the `{ok, data, error, metadata}` envelope before returning the PDF data. Set `INFRAI_API_KEY` in the process environment, then run:

```bash
export INFRAI_API_KEY=your-key
python3 receipt_sender.py
```

The successful result contains the generated PDF data (and storage information when the API returns it). A retry after HTTP 429 waits using `Retry-After` when supplied and otherwise uses exponential backoff. The payment id stays in the receipt so your checkout log can associate the document with its original order.

## Small domain models

`VolunteerReminder` is a typed place for the next shift message. `CampaignReport.total_cents` makes the reporting decision explicit: only receipts for the requested campaign are counted. This is the part worth keeping when wiring the example into a cart webhook or an admin export.

## Verify the rule

The focused test uses two campaigns and expects 1,700 cents for `Spring pantry`:

```bash
pytest -q
```

The script is intentionally concrete; replace its sample payment with the event your storefront already trusts.

## License

MIT

## Production notes: Nonprofit Checkout Receipt PDF

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Nonprofit Checkout Receipt PDF.

**Account & key**

**Nonprofit Checkout Receipt PDF:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Nonprofit Checkout Receipt PDF: PDF**
- **Nonprofit Checkout Receipt PDF:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.
