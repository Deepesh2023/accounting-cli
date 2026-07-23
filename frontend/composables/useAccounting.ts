const COMPANY_STATE = 'Karnataka'

function isInterstate(partyState: string): boolean {
  return partyState !== '' && partyState !== COMPANY_STATE
}

function resolveGstSplit(taxAmt: number, interstate: boolean) {
  if (interstate) return { cgst: 0, sgst: 0, igst: taxAmt }
  const half = taxAmt / 2
  return { cgst: half, sgst: half, igst: 0 }
}

function quantize(v: number): number {
  return Math.round(v * 100) / 100
}

function computeRow(params: {
  price: number
  quantity: number
  gstRate: number
  discountPerc?: number
  discountAmt?: number
  interstate: boolean
  taxInclusive: boolean
}) {
  const gross = params.price * params.quantity
  let discAmt = 0
  if (params.discountPerc) discAmt = gross * params.discountPerc / 100
  else if (params.discountAmt) discAmt = params.discountAmt

  let taxable = Math.max(0, gross - discAmt)
  let taxAmt = 0

  if (!params.taxInclusive) {
    taxAmt = taxable * params.gstRate / 100
  } else {
    const base = taxable / (1 + params.gstRate / 100)
    taxAmt = taxable - base
    taxable = base
  }

  const split = resolveGstSplit(taxAmt, params.interstate)
  const rowTotal = taxable + taxAmt

  return {
    discountAmount: quantize(discAmt),
    taxableAmount: quantize(taxable),
    taxAmount: quantize(taxAmt),
    cgst: quantize(split.cgst),
    sgst: quantize(split.sgst),
    igst: quantize(split.igst),
    rowTotal: quantize(rowTotal),
  }
}

function computeGrandTotal(totalTaxable: number, totalTax: number, roundOff: boolean): number {
  let gt = quantize(totalTaxable + totalTax)
  if (roundOff) gt = Math.round(gt)
  return gt
}

function partyPrefix(name: string): string {
  return `Party: ${name}`
}

export function useAccounting() {
  return {
    isInterstate,
    resolveGstSplit,
    quantize,
    computeRow,
    computeGrandTotal,
    partyPrefix,
    COMPANY_STATE,
  }
}
