const btnCopy = document.querySelector ('#btn-copy')
const referralLink = document.querySelector ('#referral-link')

btnCopy.addEventListener ('click', () => {

  // get referral link href
  const href = referralLink.getAttribute ('href')

  // Copy to clipboard
  navigator.clipboard.writeText (href)

  // Show success message
  showAlert("ok", "Copied", "Now you can share your referral link")
})