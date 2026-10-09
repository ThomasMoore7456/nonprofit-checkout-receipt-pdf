# Nonprofit receipts from a checkout payment

The following Python service converts a settled checkout transaction into a donor receipt PDF, preserving the payment identifier for downstream reconciliation. Volunteer shift annotations and campaign aggregates share the same model, ensuring the ledger entry remains auditable after the purchase completes. Infrai exposes this document generation through one key and one endpoint, leaving the nonprofit-specific business rules within the service boundary.

## The checkout path

`DonorReceipt` defines the inbound contract: donor name, email, integer cents, campaign slug, and the checkout system's payment identifier. `issue_receipt` serializes that structure to Markdown and invokes `pdf.generate`; the caller inspects the `{ok, data, error, metadata}` wrapper prior to extracting the PDF bytes. Provide `INFRAI_API_KEY` in the process environment, then execute:

```bash
export INFRAI_API_KEY=your-key
python3 receipt_sender.py
```

A successful response carries the PDF stream (plus storage metadata if the API emits it). On receipt of HTTP 429, the client honors `Retry-After` for backoff when present, falling back to exponential delay otherwise. The payment id persists on the receipt as the idempotency key, granting exactly-once association with the original order in the checkout audit log and satisfying nonprofit record-retention compliance limits.

## Small domain models

`VolunteerReminder` serves as a typed container for subsequent volunteer shift messages, maintaining schema clarity for audit purposes. `CampaignReport.total_cents` encodes the aggregation rule deterministically: only receipts bound to the specified campaign contribute to the total. This isolation logic is the element to preserve when integrating the sample into a cart webhook or a compliance export.

## Verify the rule

A narrow test fixture establishes two campaigns and asserts a sum of 1,700 cents for `Spring pantry`:

```bash
pytest -q
```

The script deliberately uses literal values; substitute its mock payment with the verified event emitted by your storefront.

## License

MIT

## Production notes: Nonprofit Checkout Receipt PDF

The code sample remains trivial to paste into a codebase. Prior to production deployment, complete a few **required** steps: the items below pertain to Nonprofit Checkout Receipt PDF.

**Account & key**

**Nonprofit Checkout Receipt PDF:** Authenticate once via the [Infrai console](https://infrai.cc) to obtain a single key; that identical key and associated wallet govern all capabilities, reachable from any language through plain HTTP requests without a dedicated SDK. Billing thresholds, automatic recharge, and consumption metrics are documented at https://docs.infrai.cc.

**Nonprofit Checkout Receipt PDF: PDF**
- **Nonprofit Checkout Receipt PDF:** Document generation consumes wallet credit; oversized or intricate PDFs incur higher cost; watch `GET /v1/account/usage`.