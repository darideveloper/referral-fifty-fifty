const form = document.querySelector ('form')

form.addEventListener ('submit', (event) => {

  // Show loading
  event.preventDefault ()
  showLoading ()

  // Submit form
  setTimeout(() => {
    form.submit()
  }, 500)

})