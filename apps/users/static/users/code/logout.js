const logoutButton = document.getElementById('logout-btn')

logoutButton.addEventListener('click', () => {
  // Show loading
  showLoading ()

  // Redirect to logout
  setTimeout(() => {
    window.location.href = '/logout'
  }, 100)
})