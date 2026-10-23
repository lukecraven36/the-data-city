// Convenience entry screen only. Public static files are not access-protected.
(() => {
  'use strict';
  const root = document.querySelector('#review-entry');
  if (!root) return;
  const config = JSON.parse(document.querySelector('#review-access-config').content.textContent);
  const form = document.querySelector('#review-entry-form');
  const email = document.querySelector('#review-email');
  const error = document.querySelector('#review-entry-error');
  const submit = document.querySelector('#review-enter');
  const signOut = document.querySelector('#review-sign-out');
  let checking = false;
  async function emailHash(value) {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
    return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
  }
  function unlock(hash, address, focus) {
    const interviewAllowed = (config.interviewEmailHashes || []).includes(hash);
    document.documentElement.classList.toggle('interview-reviewer', interviewAllowed);
    if (document.querySelector('.interview-story') && !interviewAllowed) {
      location.replace(document.querySelector('.sidebar .identity').href);
      return;
    }
    const profile = config.reviewProfiles?.[hash] || {};
    const identity = {...profile, email: address};
    window.dataCityReviewer = identity;
    document.querySelectorAll('.topbar .avatar').forEach(avatar => {
      avatar.textContent = ((profile.firstName?.[0] || '') + (profile.surname?.[0] || '')).toUpperCase();
    });
    window.dispatchEvent(new CustomEvent('review-identity-change', {detail: identity}));
    root.hidden = true;
    document.documentElement.classList.remove('review-required');
    if (focus) {
      const main = document.querySelector('#main');
      main.tabIndex = -1;
      main.focus();
    }
  }
  function lock() {
    try {
      sessionStorage.removeItem(config.storageKey);
      sessionStorage.removeItem(config.storageKey + ':email');
    } catch { /* Storage can be disabled. */ }
    window.dataCityReviewer = null;
    document.documentElement.classList.remove('interview-reviewer');
    document.querySelectorAll('dialog[open]').forEach(dialog => dialog.close());
    document.documentElement.classList.add('review-required');
    root.hidden = false;
    root.scrollTop = 0;
    email.value = '';
    error.textContent = '';
    email.removeAttribute('aria-invalid');
    window.scrollTo(0, 0);
    email.focus();
  }
  async function restoreSession() {
    try {
      const hash = sessionStorage.getItem(config.storageKey);
      const address = sessionStorage.getItem(config.storageKey + ':email');
      if (config.allowedEmailHashes.includes(hash) && address && await emailHash(address) === hash) unlock(hash, address, false);
    } catch { /* Remain on the entry screen when storage is unavailable. */ }
  }
  restoreSession();
  window.addEventListener('pageshow', event => {
    if (!event.persisted) return;
    document.documentElement.classList.add('review-required');
    document.documentElement.classList.remove('interview-reviewer');
    root.hidden = false;
    restoreSession();
  });
  submit.disabled = false;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (checking) return;
    const value = email.value.trim().toLowerCase();
    email.value = value;
    error.textContent = '';
    email.removeAttribute('aria-invalid');
    if (!value || !email.validity.valid) {
      error.textContent = 'Enter a valid email address.';
      email.setAttribute('aria-invalid', 'true');
      email.focus();
      return;
    }
    checking = true;
    submit.disabled = true;
    try {
      const hash = await emailHash(value);
      if (!config.allowedEmailHashes.includes(hash)) {
        error.textContent = 'This email is not on the review list. Please check the address or contact Luke.';
        email.setAttribute('aria-invalid', 'true');
        email.focus();
        return;
      }
      try {
        sessionStorage.setItem(config.storageKey, hash);
        sessionStorage.setItem(config.storageKey + ':email', value);
      } catch { /* Current page still works. */ }
      unlock(hash, value, true);
    } catch {
      error.textContent = 'The email check could not run. Open the HTTPS link in a current browser and try again.';
    } finally {
      checking = false;
      submit.disabled = false;
    }
  });
  signOut?.addEventListener('click', lock);
})();
