import { Switch, Match } from 'solid-js'
import { createFileRoute } from '@tanstack/solid-router'
import { activeSection, type Section } from '../components/Sidebar'

export const Route = createFileRoute('/')({ component: Home })

function SectionHeading({ title }: { title: string }) {
  return (
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-4 border-bottom">
      <h1 class="h3">{title}</h1>
    </div>
  )
}

function Section(props: { section: Section; title: string; children: any }) {
  return (
    <Switch>
      <Match when={activeSection() === props.section}>
        <SectionHeading title={props.title} />
        {props.children}
      </Match>
    </Switch>
  )
}

function Home() {
  return (
    <>
      <Section section="sales" title="Sales">
        <p class="text-muted">Sales dashboard content coming soon.</p>
      </Section>

      <Section section="purchases" title="Purchases">
        <p class="text-muted">Purchases dashboard content coming soon.</p>
      </Section>

      <Section section="outstanding" title="Outstanding Report">
        <p class="text-muted">Outstanding report content coming soon.</p>
      </Section>

      <Section section="expenses" title="Expenses">
        <p class="text-muted">Expenses content coming soon.</p>
      </Section>

      <Section section="quotation" title="Quotation">
        <p class="text-muted">Quotation content coming soon.</p>
      </Section>

      <Section section="transactions" title="Transaction History">
        <p class="text-muted">Transaction history content coming soon.</p>
      </Section>

      <Section section="parties" title="Parties">
        <p class="text-muted">Parties content coming soon.</p>
      </Section>

      <Section section="stock" title="Stock Inventory">
        <p class="text-muted">Stock inventory content coming soon.</p>
      </Section>

      <Section section="financial-statements" title="Financial Statements">
        <p class="text-muted">Financial statements content coming soon.</p>
      </Section>

      <Section section="company" title="Company Profile">
        <p class="text-muted">Company profile content coming soon.</p>
      </Section>
    </>
  )
}
