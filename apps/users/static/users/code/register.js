const form = document.querySelector('form')
const loadingWrapper = document.querySelector('.loading-wrapper')
const countryInput = document.querySelector('.iti__selected-flag')
const phoneInput = document.querySelector('#phone')
const storesInputs = document.querySelectorAll('.refferral')

// Submit form (show loading and get country code)
form.addEventListener('submit', (event) => {

  // Wait before submit
  event.preventDefault()

  // Validate stores
  const storesValues = Array.from(storesInputs).filter (store => store.value)
  
  // Display error if no stores
  if (storesValues.length == 0) {
    Swal.fire({
      icon: 'error',
      title: 'Missing stores',
      text: 'You must type at least one store referral codes to continue',
    })

    // Stop function
    return null
  }

  // Show loading
  loadingWrapper.classList.remove('hidden')
  setTimeout(() => {
    loadingWrapper.classList.remove ("transparent")
  }, 100)

  // Get title of country code
  const country = countryInput.getAttribute ('title')
  const countryParts = country.split (' ')
  const countryCode = countryParts[countryParts.length - 1].replace ('+', '')

  // Add country code to phone number
  phoneInput.value = countryCode + phoneInput.value  

  // Submit form
  setTimeout(() => {
    form.submit()
  }, 100)
})