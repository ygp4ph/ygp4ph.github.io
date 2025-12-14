const gallery = document.getElementById("gallery")
const modal = document.getElementById("modal")
const modalImage = document.getElementById("modalImage")
const closeBtn = document.querySelector(".close")

// Load gallery images from manifest or fallback
async function loadGallery() {
  try {
    const response = await fetch("gallery/manifest.json")
    if (!response.ok) {
      throw new Error("manifest.json not found")
    }
    const manifest = await response.json()
    displayGallery(manifest)
  } catch (error) {
    console.error("Error loading manifest:", error)
    gallery.innerHTML =
      '<p class="no-images">Pour ajouter des images, créez un fichier gallery/manifest.json avec la liste des noms de fichiers.</p>'
  }
}

// Display gallery grid with images
function displayGallery(images) {
  gallery.innerHTML = ""

  if (!images || images.length === 0) {
    gallery.innerHTML =
      '<p class="no-images">Aucune image dans la galerie pour le moment.</p>'
    return
  }

  const gridContainer = document.createElement("div")
  gridContainer.className = "gallery-grid gallery-fade-in"

  images.forEach((image, index) => {
    const item = document.createElement("div")
    item.className = "gallery-item"

    const img = document.createElement("img")
    img.src = `gallery/${image}`
    img.alt = `Galerie ${index + 1}`
    img.loading = "lazy"

    const overlay = document.createElement("div")
    overlay.className = "gallery-overlay"

    const btn = document.createElement("button")
    btn.className = "gallery-btn"
    btn.textContent = "Voir"

    overlay.appendChild(btn)
    item.appendChild(img)
    item.appendChild(overlay)

    // Open modal on click
    img.addEventListener("click", () => {
      modalImage.src = `gallery/${image}`
      modalImage.alt = `Galerie ${index + 1}`
      modal.style.display = "block"
      document.body.style.overflow = "hidden"
    })

    btn.addEventListener("click", (e) => {
      e.stopPropagation()
      modalImage.src = `gallery/${image}`
      modalImage.alt = `Galerie ${index + 1}`
      modal.style.display = "block"
      document.body.style.overflow = "hidden"
    })

    gridContainer.appendChild(item)
  })

  gallery.appendChild(gridContainer)
}

// Close modal
closeBtn.addEventListener("click", () => {
  modal.style.display = "none"
  document.body.style.overflow = "auto"
})

// Close modal on background click
modal.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.style.display = "none"
    document.body.style.overflow = "auto"
  }
})

// Close modal on Escape key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && modal.style.display === "block") {
    modal.style.display = "none"
    document.body.style.overflow = "auto"
  }
})

document.addEventListener('contextmenu', function (e) {
  // Si l'élément cliqué est une image (balise IMG)
  if (e.target.tagName === 'IMG') {
    e.preventDefault(); // Bloque le menu "Enregistrer sous..."
    return false;
  }
});
document.addEventListener('dragstart', function (e) {
  // Si l'élément qu'on essaie de glisser est une image
  if (e.target.tagName === 'IMG') {
    e.preventDefault(); // Annule l'action immédiatement
  }
});
// Initialize gallery on page load
loadGallery()
