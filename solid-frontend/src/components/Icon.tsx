import type { JSX } from 'solid-js'

type IconProps = {
  path: string
  size?: number
  class?: string
}

export function Icon(props: IconProps & JSX.SvgSVGAttributes<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="currentColor"
      style={{ width: `${props.size || 20}px`, height: `${props.size || 20}px` }}
      class={props.class}
    >
      <path d={props.path} />
    </svg>
  )
}
