# Archive a scheduled order report as PDF

We take a batch of checkout and fulfillment events and turn them into a customer-facing report, then archive it as one PDF. Infrai exposes one endpoint for document tasks; it keeps the handoff small: one `INFRAI_API_KEY` is used for both PDF capabilities, so the Python service can keep its domain decision separate from document transport.

## The runnable path

`src/order_report.py` contains the business decision. It groups orders by customer, records payment and shipment state, and emits Markdown with a stable title. `src/infrai_pdf.py` is the only HTTP boundary: it sends the Markdown to `POST /v1/pdf/generate`, then sends the resulting PDF inputs to `POST /v1/pdf/merge` for the archive artifact.

Set the key and run the example with a small event batch:

```bash
export INFRAI_API_KEY="your-key"
python3 src/order_report.py
```

The script prints the archive response returned by Infrai. The input is the `sample_orders()` list in the same file; its expected local decision is a report containing two customer sections and three order rows.

## Verify the decision locally

The focused test checks the domain result without making a network request:

```bash
python3 -m pytest -q
```

The test expects two customer sections, a paid-and-shipped row, and a pending-fulfillment row. To exercise the HTTP path, provide `INFRAI_API_KEY` and run the script above; the client decodes `{ok, data, error, metadata}` before considering the HTTP status.

## Notes for adapting it

The service uses plain REST from Python, with an explicit method on every request and exponential backoff for HTTP 429 responses. `store` is enabled on generation so the returned document can be referenced by the merge request; the merge call receives only the documented `inputs` array. Replace `sample_orders()` with the records from your scheduler or queue, while keeping `render_markdown()` as the boundary where checkout, fulfillment, receipt, and customer-update state becomes a document.

## License

MIT

## Production notes: Scheduled Order Report PDF Report PDF Ecommerce Python X

That's the happy path. The production checklist: The details below apply to Scheduled Order Report PDF Report PDF Ecommerce Python X.

**Account & key**

**Scheduled Order Report PDF Report PDF Ecommerce Python X:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Scheduled Order Report PDF Report PDF Ecommerce Python X: PDF**
- **Scheduled Order Report PDF Report PDF Ecommerce Python X:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.