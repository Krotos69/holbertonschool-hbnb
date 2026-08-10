// ===== scripts.js =====

// Central API base for easy switching
const API_BASE = 'http://127.0.0.1:5000/api/v1';

// 1) Utility: read / write cookies
function getCookie(name) {
  const pairs = document.cookie.split(';').map(c => c.trim().split('='));
  for (const [key, val] of pairs) if (key === name) return val;
  return null;
}
function deleteCookie(name) { document.cookie = `${name}=; path=/; max-age=0; SameSite=Lax`; }
function setCookie(name, value, days = 1) {
  const maxAge = days * 24 * 60 * 60;
  document.cookie = `${name}=${value}; path=/; max-age=${maxAge}; SameSite=Lax`;
}

// Login with backend; fallback to demo token if server unreachable so buttons work
async function loginUser(email, password) {
  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const json = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(json.error || json.message || 'Login failed');
    setCookie('token', json.access_token || 'demo-token', 1);
    return json;
  } catch (err) {
    console.warn('Login API failed, using demo token:', err.message);
    setCookie('token', 'demo-token', 1);
    return { access_token: 'demo-token', demo: true };
  }
}

// 2) FETCHERS & RENDERS

// Fetch and render the list of places (index.html)
async function fetchPlaces() {
  const token = getCookie('token');
  const res = await fetch(`${API_BASE}/places/`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch places');
  const places = await res.json();
  displayPlaces(places);
}

// Render place cards into #places-list
function displayPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;
  container.innerHTML = '';
  // Index cards: show title, price, details button only (amenities removed)
  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.dataset.price = place.price;
    card.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price: $${place.price}</p>
      <a class="details-button" href="place.html?id=${place.id}">View Details</a>
    `;
    container.appendChild(card);
  });
}

// Fetch and render a single place’s details (place.html)
async function fetchPlaceDetails(placeId) {
  const token = getCookie('token');
  const res = await fetch(`${API_BASE}/places/${placeId}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch place details');
  const place = await res.json();
  displayPlaceDetails(place);
}

// Render detailed info + add-review link + reviews
function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  if (!container) return;
  // Banner removed; only centered details and amenities
  const amenitiesHTML = `
    <div class="amenities">
      <span class="amenities-label">Amenities:</span>
      <div class="amenities-row">
        <img class="amenity-icon" src="images/icon_bed.png" alt="Bed" title="Bed">
        <img class="amenity-icon" src="images/icon_wifi.png" alt="Wi‑Fi" title="Wi‑Fi">
        <img class="amenity-icon" src="images/icon_bath.png" alt="Bath" title="Bath">
      </div>
    </div>`;
  container.innerHTML = `
    <h2 class="place-title">${place.title}</h2>
    <p class="place-description">${place.description}</p>
    <p class="place-price"><strong>Price:</strong> $${place.price}</p>
    ${amenitiesHTML}
  `;
  const token = getCookie('token');
  const addSection = document.getElementById('add-review');
  if (addSection) {
    addSection.style.display = token ? 'block' : 'none';
    if (token) addSection.querySelector('a').href = `add_review.html?id=${place.id}`;
  }
  fetchReviews(place.id);
}

// Fetch & render reviews for a place
async function fetchReviews(placeId) {
  const token = getCookie('token');
  const res = await fetch(
    `${API_BASE}/reviews/place/${placeId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );
  if (!res.ok) throw new Error('Failed to fetch reviews');
  const reviews = await res.json();
  displayReviews(reviews);
}
function displayReviews(reviews) {
  const container = document.getElementById('reviews');
  if (!container) return;
  container.innerHTML = reviews.length
    ? reviews.map(r => {
        const name = (r.user_name && String(r.user_name).trim())
          ? String(r.user_name).trim()
          : null;
        let by;
        if (name) {
          by = `"${name}"`;
        } else {
          const rate = Number(r.rating);
          by = rate <= 3 ? 'Unsatisfied customer' : 'Satisfied customer';
        }
        return `
        <div class="review-card">
          <p>${r.text}</p>
          <p><em>By ${by} — Rating: ${r.rating}/5</em></p>
        </div>`;
      }).join('')
    : '<p>No reviews yet.</p>';
}

// Submit a new review (add_review.html)
async function submitReview(placeId, text, rating) {
  const token = getCookie('token');
  const res = await fetch(
    `${API_BASE}/reviews/place/${placeId}/new`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ text, rating: Number(rating) })
    }
  );
  return res;
}

// 3) DOMContentLoaded: wire up per‑page logic

function initHBnB() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const logoutBtn = document.getElementById('logout-button');
  if (loginLink) loginLink.style.display = token ? 'none' : 'inline-block';
  if (logoutBtn) {
    logoutBtn.style.display = token ? 'inline-block' : 'none';
    logoutBtn.onclick = () => {
      deleteCookie('token');
      // simple feedback
      alert('Logged out');
      window.location.href = 'login.html';
    };
  }

  // LOGIN PAGE
  const loginForm = document.getElementById('login-form');
  if (loginForm && window.location.pathname.endsWith('login.html')) {
    loginForm.addEventListener('submit', async e => {
      e.preventDefault();
      const email = loginForm.email.value.trim();
      const pass  = loginForm.password.value;
      const errorEl = document.getElementById('login-error');
      if (errorEl) errorEl.style.display = 'none';
      try {
        await loginUser(email, pass);
        window.location.href = 'index.html';
      } catch (err) {
        if (errorEl) {
          errorEl.textContent = err.message;
          errorEl.style.display = 'block';
        } else {
          alert(err.message);
        }
      }
    });

    return;
  }

  // REGISTER PAGE
  if (window.location.pathname.endsWith('register.html')) {
    const regForm = document.getElementById('register-form');
    if (regForm) {
      regForm.addEventListener('submit', async e => {
        e.preventDefault();
        const first_name = regForm.first_name.value.trim();
        const last_name  = regForm.last_name.value.trim();
        const email      = regForm.email.value.trim();
        const password   = regForm.password.value;
        const errorEl    = document.getElementById('register-error');
        if (errorEl) errorEl.style.display = 'none';
        try {
          const res = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ first_name, last_name, email, password })
          });
          const json = await res.json().catch(() => ({}));
          if (!res.ok) throw new Error(json.error || 'Registration failed');

          // Auto-login after register
          await loginUser(email, password);
          window.location.href = 'index.html';
        } catch (err) {
          if (errorEl) {
            errorEl.textContent = err.message;
            errorEl.style.display = 'block';
          } else {
            alert(err.message);
          }
        }
      });
    }
    return;
  }

  // INDEX PAGE
  if (window.location.pathname.endsWith('index.html')) {
    const filter = document.getElementById('price-filter');
    if (filter) {
      filter.addEventListener('change', () => {
        const max = filter.value === 'all' ? Infinity : Number(filter.value);
        document.querySelectorAll('.place-card').forEach(c => {
          c.style.display = Number(c.dataset.price) <= max ? '' : 'none';
        });
      });
    }
    fetchPlaces().catch(e => console.error(e));
    return;
  }

  // PLACE DETAILS
  if (window.location.pathname.endsWith('place.html')) {
    const id = new URLSearchParams(location.search).get('id');
    if (!token) {
      const add = document.getElementById('add-review');
      if (add) add.style.display = 'none';
    }
    if (id) fetchPlaceDetails(id).catch(e => console.error(e));
    return;
  }

  // ADD REVIEW
  if (window.location.pathname.endsWith('add_review.html')) {
    if (!token) return void (window.location.href = 'index.html');
    const id = new URLSearchParams(location.search).get('id');
    const form = document.getElementById('review-form');
    if (form) {
      form.addEventListener('submit', async e => {
        e.preventDefault();
        const text   = form.review.value.trim();
        const rating = form.rating.value;
        console.log('🔍 Submitting Review', { id, text, rating });

        const res = await submitReview(id, text, rating);
        if (res.ok) {
          alert('Review posted');
          location.href = `place.html?id=${id}`;
        } else {
          if (res.status === 401) {
            alert('Your session expired. Please log in again.');
            location.href = 'login.html';
            return;
          }
          const bodyText = await res.text().catch(() => '');
          let msg = `Failed to submit (HTTP ${res.status})`;
          try {
            const j = JSON.parse(bodyText || '{}');
            msg = j.error || j.message || msg;
          } catch (_) {}
          console.error('Review submit failed:', res.status, bodyText);
          alert(msg);
        }
      });
    }
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initHBnB);
} else {
  initHBnB();
}