export function getFilenameFromContentDisposition(
  contentDisposition?: string | null
): string | null {

  if (!contentDisposition) return null

  // RFC 5987 (filename*=UTF-8'')
  const utf8Match = contentDisposition.match(
    /filename\*\s*=\s*UTF-8''([^;]+)/i
  )
  if (utf8Match?.[1]) {
    try {
      return decodeURIComponent(utf8Match[1])
    } catch {
      return utf8Match[1]
    }
  }

  // Standard filename="file.ext" OR filename=file.ext
  const asciiMatch = contentDisposition.match(
    /filename\s*=\s*"?([^";]+)"?/i
  )

  return asciiMatch?.[1] ?? null
}

export function toDateOnlyISO(date: Date): string {
  return date.toISOString().slice(0, 10);
}

export function resolveUserRoleVariant(role: string): { color: string, icon: string } {
  const roleLowerCase = role.toLowerCase()

  if (roleLowerCase === 'cliente')
    return { color: 'success', icon: 'ri-user-line' }
  if (roleLowerCase === 'collaboratore')
    return { color: 'info', icon: 'ri-pie-chart-line' }
  if (roleLowerCase === 'admin')
    return { color: 'primary', icon: 'ri-vip-crown-line' }

  return { color: 'success', icon: 'ri-user-line' }
}

export function resolveUserStatusVariant(role: string): string {
  const roleLowerCase = role.toLowerCase()

  if (roleLowerCase === 'disattivo')
    return 'error'

  return 'primary'

}
