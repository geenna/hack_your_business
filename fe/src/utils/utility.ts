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