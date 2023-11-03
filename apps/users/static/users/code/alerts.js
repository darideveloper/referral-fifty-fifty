
/**
 * Show alert (error or info)
 * @param {str} icon icon name ("error", "info")
 * @param {str} title alert title 
 * @param {str} text alert text
 */
function showAlert(icon, title, text) {
  Swal.fire({
    icon: icon,
    title: title,
    text: text,
  })
}

if (error != "") {
  const errorParts = error.split("|")
  showAlert("error", errorParts[0], errorParts[1])
}

if (info != "") {
  const infoParts = info.split("|")
  showAlert("info", infoParts[0], infoParts[1])

}