const gallery = document.getElementById("gallery")
const modal = document.getElementById("modal")
const modalImage = document.getElementById("modalImage")
const closeBtn = document.querySelector(".close")

// Deterministic alias generator for filenames
function getAlias(filename) {
    let hash = 0;
    for (let i = 0; i < filename.length; i++) {
        hash = ((hash << 5) - hash) + filename.charCodeAt(i);
        hash |= 0;
    }
    let seed = Math.abs(hash);
    const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
    let alias = "";
    for (let i = 0; i < 8; i++) {
        seed = (seed * 1664525 + 1013904223) % 4294967296;
        alias += chars[seed % chars.length];
    }
    return alias;
}

let aliasMap = {}; // alias -> filename
let imagesList = []; // Liste ordonnée des images
let currentImageIndex = -1; // Index de l'image actuellement affichée

// Load gallery images from manifest or fallback
async function loadGallery() {
  try {
    const response = await fetch("gallery/manifest.json")
    if (!response.ok) {
      throw new Error("manifest.json not found")
    }
    const manifest = await response.json()
    
    // Build alias map
    manifest.forEach(file => {
        aliasMap[getAlias(file)] = file;
    });

    displayGallery(manifest)
  } catch (error) {
    console.error("Error loading manifest:", error)
    gallery.innerHTML =
      '<p class="no-images">Pour ajouter des images, créez un fichier gallery/manifest.json avec la liste des noms de fichiers.</p>'
  }
}

// Open modal for a specific image
function openImage(filename) {
  if (!filename) return
  const alias = getAlias(filename);
  
  // Trouver l'index de l'image dans la liste
  currentImageIndex = imagesList.indexOf(filename);
  
  modalImage.src = `gallery/${filename}`
  modalImage.alt = "Image Galerie"
  modal.style.display = "block"
  document.body.style.overflow = "hidden"
  
  // Update hash with alias instead of filename
  const currentHash = window.location.hash.substring(1)
  if (currentHash !== alias) {
    window.location.hash = alias
  }
}

// Close modal and clear hash
function closeModal() {
  modal.style.display = "none"
  document.body.style.overflow = "auto"
  if (window.location.hash) {
      history.pushState("", document.title, window.location.pathname + window.location.search);
  }
}

// Check URL hash and open image if needed
function checkHash() {
  const hash = window.location.hash.substring(1)
  if (hash && aliasMap[hash]) {
    openImage(aliasMap[hash])
  } else {
    closeModal()
  }
}

// Display gallery grid with images
function displayGallery(images) {
  gallery.innerHTML = ""
  imagesList = images; // Stocker la liste pour la navigation

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

    // Open via hash change using alias
    img.addEventListener("click", () => {
      window.location.hash = getAlias(image)
    })

    btn.addEventListener("click", (e) => {
      e.stopPropagation()
      window.location.hash = getAlias(image)
    })

    gridContainer.appendChild(item)
  })

  gallery.appendChild(gridContainer)
  
  // Initialize Masonry with horizontal order (left to right reading)
  const msnry = new Masonry(gridContainer, {
    itemSelector: '.gallery-item',
    columnWidth: '.gallery-item',
    gutter: 20,
    percentPosition: true,
    horizontalOrder: true  // Read left to right (row order)
  });
  
  // Re-layout once when ALL images are loaded (instead of per-image)
  imagesLoaded(gridContainer).on('always', function() {
    msnry.layout();
  });
  
  // Initial check on load
  checkHash()
  
  // Listen for hash changes
  window.addEventListener('hashchange', checkHash)
}

// Navigation functions
function navigatePrev() {
  if (imagesList.length === 0 || currentImageIndex === -1) return;
  const newIndex = (currentImageIndex - 1 + imagesList.length) % imagesList.length;
  window.location.hash = getAlias(imagesList[newIndex]);
}

function navigateNext() {
  if (imagesList.length === 0 || currentImageIndex === -1) return;
  const newIndex = (currentImageIndex + 1) % imagesList.length;
  window.location.hash = getAlias(imagesList[newIndex]);
}

// Close modal events
closeBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  closeModal();
})

// Click on modal background (left/right zones) for navigation
modal.addEventListener("click", (e) => {
  // Si on clique sur l'image elle-même ou le bouton close, ne pas naviguer
  if (e.target === modalImage || e.target === closeBtn || e.target.closest('.close')) {
    return;
  }
  
  // Si le modal est affiché
  if (modal.style.display === "block") {
    const rect = modal.getBoundingClientRect();
    const clickX = e.clientX;
    const modalCenterX = rect.left + rect.width / 2;
    
    // Clic à gauche = image précédente, clic à droite = image suivante
    if (clickX < modalCenterX) {
      navigatePrev();
    } else {
      navigateNext();
    }
  }
})

// Navigation arrows buttons
document.addEventListener("click", (e) => {
  if (e.target.closest('.modal-nav-prev')) {
    e.stopPropagation();
    navigatePrev();
  } else if (e.target.closest('.modal-nav-next')) {
    e.stopPropagation();
    navigateNext();
  }
})

// Keyboard navigation
document.addEventListener("keydown", (e) => {
  if (modal.style.display === "block") {
    if (e.key === "Escape") {
      closeModal();
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      navigatePrev();
    } else if (e.key === "ArrowRight") {
      e.preventDefault();
      navigateNext();
    }
  }
})

document.addEventListener('contextmenu', function (e) {
  if (e.target.tagName === 'IMG') {
    e.preventDefault();
    return false;
  }
});

document.addEventListener('dragstart', function (e) {
  if (e.target.tagName === 'IMG') {
    e.preventDefault();
  }
});
// Initialize gallery on page load
loadGallery()

// Mobile Menu Toggle
const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
const navLinks = document.getElementById('nav-links');
if (mobileMenuToggle && navLinks) {
    mobileMenuToggle.addEventListener('click', () => {
        mobileMenuToggle.classList.toggle('active');
        navLinks.classList.toggle('active');
    });
    navLinks.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenuToggle.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });
}

// Optimized Parallax Effect for Gallery with requestAnimationFrame
let parallaxTicking = false;
function updateGalleryParallax() {
    const scrollTop = window.scrollY;
    const docHeight = document.body.scrollHeight - window.innerHeight;

    if (docHeight > 0) {
        const scrollPercent = scrollTop / docHeight;
        const bgPosY = scrollPercent * 100;
        document.body.style.setProperty('--bg-pos-y', `${bgPosY}%`);
    }
    parallaxTicking = false;
}

window.addEventListener('scroll', () => {
    if (!parallaxTicking) {
        requestAnimationFrame(updateGalleryParallax);
        parallaxTicking = true;
    }
}, { passive: true });

// Initial call to set position
updateGalleryParallax();
