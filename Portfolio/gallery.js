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
  
  // Re-layout after each image loads for proper positioning
  imagesLoaded(gridContainer).on('progress', function() {
    msnry.layout();
  });
  
  // Initial check on load
  checkHash()
  
  // Listen for hash changes
  window.addEventListener('hashchange', checkHash)
}

// Close modal events
closeBtn.addEventListener("click", closeModal)

modal.addEventListener("click", (e) => {
  if (e.target === modal) {
    closeModal()
  }
})

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && modal.style.display === "block") {
    closeModal()
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

// Parallax Effect for Gallery
window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.body.scrollHeight - window.innerHeight;

    if (docHeight > 0) {
        const scrollPercent = scrollTop / docHeight;
        const bgPosY = scrollPercent * 100; // 0 to 100
        document.body.style.setProperty('--bg-pos-y', `${bgPosY}%`);
    }
});
// Initial call to set position
window.dispatchEvent(new Event('scroll'));
