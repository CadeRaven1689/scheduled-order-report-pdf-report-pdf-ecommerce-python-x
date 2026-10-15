"""Render order events and archive the resulting PDF."""

from dataclasses import dataclass
from typing import List

try:
    from .infrai_pdf import PdfClient
except ImportError:
    from infrai_pdf import PdfClient


@dataclass
class Order:
    order_id: str
    customer: str
    total: float
    payment: str
    fulfillment: str
    receipt: str
    update: str


def sample_orders() -> List[Order]:
    return [
        Order("A-100", "Mina", 49.90, "paid", "shipped", "emailed", "tracking sent"),
        Order("A-101", "Mina", 18.00, "paid", "processing", "emailed", "packing update sent"),
        Order("B-200", "Jon", 72.50, "paid", "shipped", "emailed", "delivered update sent"),
    ]


def render_markdown(orders: List[Order]) -> str:
    customers = {}
    for order in orders:
        customers.setdefault(order.customer, []).append(order)
    lines = ["# Periodic e-commerce order report", "", f"Orders: {len(orders)}", ""]
    for customer, rows in customers.items():
        lines.extend([f"## {customer}", "", "| Order | Total | Payment | Fulfillment | Receipt | Update |", "|---|---:|---|---|---|---|"])
        for row in rows:
            lines.append(f"| {row.order_id} | ${row.total:.2f} | {row.payment} | {row.fulfillment} | {row.receipt} | {row.update} |")
        lines.append("")
    return "\n".join(lines)


def archive_report(orders: List[Order]) -> dict:
    client = PdfClient()
    generated = client.generate(render_markdown(orders))
    source = generated["data"]["url"]
    return client.merge([source])


if __name__ == "__main__":
    print(archive_report(sample_orders()))
