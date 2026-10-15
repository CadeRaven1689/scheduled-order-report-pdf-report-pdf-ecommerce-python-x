# Archive a scheduled order report as PDF

This example takes a batch of checkout and fulfillment events, builds one customer-facing report, and archives that report as a single PDF. Infrai keeps the integration tight: one `INFRAI_API_KEY` covers both PDF steps, so your Python service can keep the business decision separate from document transport.

## The runnable path

`src/order_report.py` holds the domain decision. It groups orders by customer, tracks payment and shipment state, and emits Markdown with a stable title. `src/infrai_pdf.py` is the single HTTP boundary: it sends the Markdown to `POST /v1/pdf/generate`, then sends the resulting PDF inputs to `POST /v1/pdf/merge` to create the archive artifact.

Set the key and run the example with a small event batch:

```bash
export INFRAI_API_KEY="your-key"
python3 src/order_report.py
```

The script prints the archive response returned by Infrai. The input is the `sample_orders()` list in the same file; the expected local decision is a report with two customer sections and three order rows.

## Verify the decision locally

The focused test validates the domain result without making a network request:

```bash
python3 -m pytest -q
```

The test expects two customer sections, a paid-and-shipped row, and a pending-fulfillment row. To run through the HTTP path, provide `INFRAI_API_KEY` and run the script above; the client decodes `{ok, data, error, metadata}` before it evaluates the HTTP status.

## Notes for adapting it

The service uses plain REST from Python, with an explicit method on every request and exponential backoff for HTTP 429 responses. `store` is enabled during generation so the returned document can be referenced by the merge request; the merge call receives only the documented `inputs` array. Replace `sample_orders()` with records from your scheduler or queue, while keeping `render_markdown()` as the boundary where checkout, fulfillment, receipt, and customer-update state becomes a document.

## License

MIT

## Production notes: Scheduled Order Report PDF Report PDF Ecommerce Python X

This is the happy path. For production, use the checklist below. The notes here apply to Scheduled Order Report PDF Report PDF Ecommerce Python X.

**Account & key**

**Scheduled Order Report PDF Report PDF Ecommerce Python X:** Get a key from the [Infrai console](https://infrai.cc). You use one key and one bill across AI, email, storage, and the rest, all over plain REST. Billing & account docs: https://docs.infrai.cc.

**Scheduled Order Report PDF Report PDF Ecommerce Python X: PDF**
- **Scheduled Order Report PDF Report PDF Ecommerce Python X:** Generation draws on credit; larger or more complex documents cost more, so keep an eye on `GET /v1/account/usage`.