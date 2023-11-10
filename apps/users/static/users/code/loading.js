const loadingWrapper = document.querySelector('.loading-wrapper')

function showLoading () {
    // Show loading
    loadingWrapper.classList.remove('hidden')
    setTimeout(() => {
      loadingWrapper.classList.remove ("transparent")
    }, 100)
}