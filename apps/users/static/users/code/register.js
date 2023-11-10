const form = document.querySelector('form')
const countryInput = document.querySelector('.iti__selected-flag')
const phoneInput = document.querySelector('#phone')
const storesInputs = document.querySelectorAll('.refferral')

// Refferral link structure
const refferralStructure = {
  "amazon": ["tag"],
  "ebay": ["mkcid", "mkrid", "siteid", "campid", "customid", "toolid", "mkevt"],
  "walmart": [], // TODO: update structure
}

// Submit form (show loading and get country code)
form.addEventListener('submit', (event) => {

  // Wait before submit
  event.preventDefault()

  // Validate stores inputs
  const storesWithValue = Array.from(storesInputs).filter (store => store.value)
  
  // Display error if no stores
  if (storesWithValue.length == 0) {
    Swal.fire({
      icon: 'error',
      title: 'Missing stores',
      text: 'You must type at least one store referral codes to continue',
    })

    // Stop function
    return null
  }

  // Validate stores inputs structure
  for (const storeInput of storesWithValue) {
    
    // Get structure
    const storeName = storeInput.getAttribute ('name')
    const storeKeys = refferralStructure[storeName]

    // Validate keys
    const storeValue = storeInput.value
    for (const storeKey of storeKeys) {
      if (!storeValue.includes (storeKey)) {
        Swal.fire({
          icon: 'error',
          title: 'Invalid store code',
          text: `The ${storeName} code is invalid`,
        })

        storeInput.classList.add ("error")

        // Stop function
        return null
      }
    }
  }

  showLoading ()

  // Get title of country code
  const country = countryInput.getAttribute ('title')
  const countryParts = country.split (' ')
  const countryCode = countryParts[countryParts.length - 1].replace ('+', '')

  // Add country code to phone number
  phoneInput.value = countryCode + phoneInput.value  

  // Submit form
  setTimeout(() => {
    form.submit()
  }, 500)
})