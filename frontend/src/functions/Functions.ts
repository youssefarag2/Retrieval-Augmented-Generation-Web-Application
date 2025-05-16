export function getFromAssets(src: string) {
    // Remember to change path before deployment
    const paths = {
        deploymentPath: '',
        localhostPath: '../../public/assets/',
    }

    return new URL(paths.localhostPath + src, import.meta.url).href
}

export function capitalize(text: string) {
    if (!text) return ''
    return text.charAt(0).toUpperCase() + text.slice(1)
}

export function detectLanguage(text: string): 'ar' | 'en' {
    return /[\u0600-\u06FF]/.test(text) ? 'ar' : 'en'
}
