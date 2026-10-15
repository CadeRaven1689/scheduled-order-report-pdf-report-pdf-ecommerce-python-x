from unittest.mock import patch

from src.order_report import archive_report, render_markdown, sample_orders


def test_report_groups_customer_orders_and_states():
    report = render_markdown(sample_orders())
    assert report.count("## ") == 2
    assert "| A-100 | $49.90 | paid | shipped | emailed | tracking sent |" in report
    assert "| A-101 | $18.00 | paid | processing | emailed | packing update sent |" in report


def test_archive_merges_generated_pdf_url():
    with patch("src.order_report.PdfClient") as client_type:
        client = client_type.return_value
        client.generate.return_value = {"ok": True, "data": {"url": "https://example.com/report.pdf"}}
        client.merge.return_value = {"ok": True, "data": {"url": "https://example.com/archive.pdf"}}

        result = archive_report(sample_orders())

    client.merge.assert_called_once_with(["https://example.com/report.pdf"])
    assert result == client.merge.return_value
