// ===== DOM Elements =====
const form = document.getElementById('emailForm');
const emailInput = document.getElementById('emailInput');
const sendBtn = document.getElementById('sendBtn');
const btnText = document.getElementById('btnText');
const btnSpinner = document.getElementById('btnSpinner');
const btnIcon = document.getElementById('btnIcon');
const toastContainer = document.getElementById('toastContainer');
const historySection = document.getElementById('historySection');
const historyList = document.getElementById('historyList');
const hrNameInput = document.getElementById('hrNameInput');
const companyInput = document.getElementById('companyInput');

// Job description elements
const jdInput = document.getElementById('jdInput');
const jdWrapper = document.getElementById('jdWrapper');
const jdHint = document.getElementById('jdHint');
const toggleJd = document.getElementById('toggleJd');
const jdToggleText = document.getElementById('jdToggleText');

// Bulk mode elements
const singleEmailGroup = document.getElementById('singleEmailGroup');
const bulkEmailGroup = document.getElementById('bulkEmailGroup');
const bulkEmailsInput = document.getElementById('bulkEmailsInput');
const toggleBulkMode = document.getElementById('toggleBulkMode');
const toggleSingleMode = document.getElementById('toggleSingleMode');

// Resume elements
const fileUploadArea = document.getElementById('fileUploadArea');
const resumeInput = document.getElementById('resumeInput');
const fileUploadContent = document.getElementById('fileUploadContent');
const fileSelected = document.getElementById('fileSelected');
const fileName = document.getElementById('fileName');
const fileRemove = document.getElementById('fileRemove');

// Cover letter elements
const toggleCoverLetter = document.getElementById('toggleCoverLetter');
const toggleText = document.getElementById('toggleText');
const coverLetterWrapper = document.getElementById('coverLetterWrapper');
const coverLetterInput = document.getElementById('coverLetterInput');
const coverLetterDefault = document.getElementById('coverLetterDefault');
const resetCoverLetter = document.getElementById('resetCoverLetter');

// ===== State =====
const HISTORY_KEY = 'jobAppSentHistory';
let sentHistory = loadHistory();
let coverLetterOpen = false;
let bulkMode = false;

function loadHistory() {
    try {
        return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
    } catch (e) {
        return [];
    }
}

function saveHistory() {
    try {
        // Keep the list from growing unbounded
        localStorage.setItem(HISTORY_KEY, JSON.stringify(sentHistory.slice(0, 200)));
    } catch (e) {
        // localStorage may be unavailable (e.g. private browsing quota) — fail silently
    }
}

function hasAlreadySentTo(email) {
    return sentHistory.some(item => item.success && item.email.toLowerCase() === email.toLowerCase());
}

// ===== Email Validation =====
function isValidEmail(email) {
    return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
}

// ===== Toast Notifications =====
function showToast(message, type = 'success') {
    const icons = {
        success: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`,
        error: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`
    };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `${icons[type]}<span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('toast-exit');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// ===== Resume File Upload =====
fileUploadArea.addEventListener('click', () => resumeInput.click());

fileUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadArea.classList.add('drag-over');
});

fileUploadArea.addEventListener('dragleave', () => {
    fileUploadArea.classList.remove('drag-over');
});

fileUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadArea.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file) {
        resumeInput.files = e.dataTransfer.files;
        showSelectedFile(file.name);
    }
});

resumeInput.addEventListener('change', () => {
    if (resumeInput.files.length > 0) {
        showSelectedFile(resumeInput.files[0].name);
    }
});

function showSelectedFile(name) {
    fileUploadContent.style.display = 'none';
    fileSelected.style.display = 'flex';
    fileName.textContent = name;
}

function clearSelectedFile() {
    resumeInput.value = '';
    fileUploadContent.style.display = 'flex';
    fileSelected.style.display = 'none';
}

fileRemove.addEventListener('click', (e) => {
    e.stopPropagation();
    clearSelectedFile();
});

// ===== Bulk Mode Toggle =====
toggleBulkMode.addEventListener('click', () => {
    bulkMode = true;
    singleEmailGroup.style.display = 'none';
    bulkEmailGroup.style.display = 'block';
    emailInput.value = '';
    bulkEmailsInput.focus();
});

toggleSingleMode.addEventListener('click', () => {
    bulkMode = false;
    bulkEmailGroup.style.display = 'none';
    singleEmailGroup.style.display = 'block';
    bulkEmailsInput.value = '';
    emailInput.focus();
});

// ===== Job Description Toggle =====
let jdOpen = false;
toggleJd.addEventListener('click', () => {
    jdOpen = !jdOpen;
    jdWrapper.style.display = jdOpen ? 'block' : 'none';
    jdHint.style.display = jdOpen ? 'none' : 'flex';
    jdToggleText.textContent = jdOpen ? 'Collapse' : 'Add JD';
    if (jdOpen) jdInput.focus();
});

// ===== Cover Letter Toggle =====
toggleCoverLetter.addEventListener('click', () => {
    coverLetterOpen = !coverLetterOpen;
    coverLetterWrapper.style.display = coverLetterOpen ? 'block' : 'none';
    coverLetterDefault.style.display = coverLetterOpen ? 'none' : 'flex';
    toggleText.textContent = coverLetterOpen ? 'Collapse' : 'Customize';
});

resetCoverLetter.addEventListener('click', () => {
    coverLetterInput.value = window.DEFAULT_COVER_LETTER;
    showToast('Cover letter reset to default.', 'success');
});

// ===== History =====
function addToHistory(email, success, message = '') {
    sentHistory.unshift({ email, success, message, time: new Date().toISOString() });
    saveHistory();
    renderHistory();
}

function renderHistory() {
    if (sentHistory.length === 0) {
        historySection.style.display = 'none';
        return;
    }

    historySection.style.display = 'block';
    historyList.innerHTML = sentHistory.map((item, index) => `
    <li class="history-item">
      <span class="email" title="${item.message ? item.message.replace(/"/g, '&quot;') : ''}">${item.email}</span>
      <span class="history-actions">
        <span class="status ${item.success ? 'sent' : 'failed'}">
          ${item.success ? '✓ Sent' : '✗ Failed'}
        </span>
        ${!item.success ? `<button type="button" class="retry-btn" data-index="${index}" title="Refill this email to retry">Retry</button>` : ''}
      </span>
    </li>
  `).join('');
}

historyList.addEventListener('click', (e) => {
    const btn = e.target.closest('.retry-btn');
    if (!btn) return;
    const item = sentHistory[Number(btn.dataset.index)];
    if (!item) return;

    if (bulkMode) {
        toggleSingleMode.click();
    }
    emailInput.value = item.email;
    emailInput.focus();
    window.scrollTo({ top: form.offsetTop - 40, behavior: 'smooth' });
});

// Render any history restored from localStorage on page load
renderHistory();

// ===== Sending State =====
function setLoading(loading) {
    sendBtn.disabled = loading;
    emailInput.disabled = loading;
    btnText.textContent = loading ? 'Sending...' : 'Send Application';
    btnSpinner.style.display = loading ? 'block' : 'none';
    btnIcon.style.display = loading ? 'none' : 'block';
}

function buildSharedFormData() {
    const formData = new FormData();
    if (resumeInput.files.length > 0) {
        formData.append('resume', resumeInput.files[0]);
    }
    if (coverLetterOpen) {
        formData.append('cover_letter', coverLetterInput.value);
    }
    if (hrNameInput.value.trim()) {
        formData.append('hr_name', hrNameInput.value.trim());
    }
    if (companyInput.value.trim()) {
        formData.append('company', companyInput.value.trim());
    }
    if (jdOpen && jdInput.value.trim()) {
        formData.append('jd_text', jdInput.value.trim());
    }
    return formData;
}

async function submitSingle(email) {
    if (hasAlreadySentTo(email)) {
        const proceed = confirm(`You already sent an application to ${email} before. Send again anyway?`);
        if (!proceed) return;
    }

    setLoading(true);
    try {
        const formData = buildSharedFormData();
        formData.append('email', email);

        const response = await fetch('/send', { method: 'POST', body: formData });
        const data = await response.json();

        showToast(data.message, data.success ? 'success' : 'error');
        addToHistory(email, data.success, data.message);
        if (data.success) emailInput.value = '';
    } catch (err) {
        showToast('Network error. Please check if the server is running.', 'error');
        addToHistory(email, false, 'Network error');
    } finally {
        setLoading(false);
        emailInput.focus();
    }
}

async function submitBulk(emails) {
    const newRecipients = emails.filter(email => !hasAlreadySentTo(email));
    const alreadySentCount = emails.length - newRecipients.length;

    if (newRecipients.length === 0) {
        showToast('All of these recipients already have a successful send in your history.', 'error');
        return;
    }

    if (alreadySentCount > 0) {
        const proceed = confirm(`${alreadySentCount} of these emails were already sent successfully before. Continue with the remaining ${newRecipients.length}?`);
        if (!proceed) return;
    }

    setLoading(true);
    try {
        const formData = buildSharedFormData();
        formData.append('emails', newRecipients.join('\n'));

        const response = await fetch('/send-bulk', { method: 'POST', body: formData });
        const data = await response.json();

        if (Array.isArray(data.results)) {
            data.results.forEach(r => addToHistory(r.email, r.success, r.message));
        }
        showToast(data.message, data.success ? 'success' : 'error');
        if (data.success) bulkEmailsInput.value = '';
    } catch (err) {
        showToast('Network error. Please check if the server is running.', 'error');
    } finally {
        setLoading(false);
    }
}

// ===== Form Submit =====
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (bulkMode) {
        const emails = bulkEmailsInput.value
            .split(/[\n,]/)
            .map(x => x.trim())
            .filter(Boolean);

        if (emails.length === 0) {
            showToast('Please enter at least one email address.', 'error');
            bulkEmailsInput.focus();
            return;
        }

        const invalid = emails.filter(email => !isValidEmail(email));
        if (invalid.length > 0) {
            showToast(`Invalid email address: ${invalid[0]}`, 'error');
            bulkEmailsInput.focus();
            return;
        }

        await submitBulk(emails);
        return;
    }

    const email = emailInput.value.trim();

    if (!email) {
        showToast('Please enter an email address.', 'error');
        emailInput.focus();
        return;
    }

    if (!isValidEmail(email)) {
        showToast('Please enter a valid email address.', 'error');
        emailInput.focus();
        return;
    }

    await submitSingle(email);
});
