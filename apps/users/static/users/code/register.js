const form = document.querySelector('form')
const loadingWrapper = document.querySelector('.loading-wrapper')

// Detect when the form is submitted
form.addEventListener('submit', (event) => {
  event.preventDefault()
  loadingWrapper.classList.remove('hidden')
  setTimeout(() => {
    loadingWrapper.classList.remove ("transparent")
  }, 100)
  setTimeout(() => {
    form.submit()
  }, 5000)
})