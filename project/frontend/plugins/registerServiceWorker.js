if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(err =>
        console.error('SW kayıt hata:', err)
    )
}