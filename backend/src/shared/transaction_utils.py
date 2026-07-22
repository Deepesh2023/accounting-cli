import uuid
from uuid import UUID
from decimal import Decimal, ROUND_HALF_UP


def resolve_gst_split(tax_amt: Decimal, is_interstate: bool) -> tuple[Decimal, Decimal, Decimal]:
    if is_interstate:
        return Decimal("0"), Decimal("0"), tax_amt
    half = tax_amt / 2
    return half, half, Decimal("0")


def quantize(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def compute_row(
    price: Decimal,
    quantity: int,
    gst_rate: Decimal,
    discount_perc: Decimal | None,
    discount_amt: Decimal | None,
    is_interstate: bool,
    tax_inclusive: bool,
) -> dict:
    gross = price * quantity

    disc_amt = Decimal("0")
    if discount_perc is not None:
        disc_amt = gross * discount_perc / Decimal("100")
    elif discount_amt is not None:
        disc_amt = discount_amt

    taxable = max(Decimal("0"), gross - disc_amt)

    if not tax_inclusive:
        tax_amt = taxable * gst_rate / Decimal("100")
    else:
        base = taxable / (Decimal("1") + gst_rate / Decimal("100"))
        tax_amt = taxable - base
        taxable = base

    cgst, sgst, igst = resolve_gst_split(tax_amt, is_interstate)
    row_total = taxable + tax_amt

    return {
        "discount_amount": quantize(disc_amt),
        "taxable_amount": quantize(taxable),
        "tax_amount": quantize(tax_amt),
        "cgst_amount": quantize(cgst),
        "sgst_amount": quantize(sgst),
        "igst_amount": quantize(igst),
        "row_total": quantize(row_total),
    }


def compute_grand_total(total_taxable: Decimal, total_tax: Decimal, round_off: bool) -> Decimal:
    grand_total = quantize(total_taxable + total_tax)
    if round_off:
        grand_total = grand_total.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return grand_total


def party_prefix(party_name: str) -> str:
    return f"Party: {party_name}"
