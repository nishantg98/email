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
const sentHistory = [];
let coverLetterOpen = false;

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
function addToHistory(email, success) {
    sentHistory.unshift({ email, success, time: new Date() });
    renderHistory();
}

function renderHistory() {
    if (sentHistory.length === 0) {
        historySection.style.display = 'none';
        return;
    }

    historySection.style.display = 'block';
    historyList.innerHTML = sentHistory.map(item => `
    <li class="history-item">
      <span class="email">${item.email}</span>
      <span class="status ${item.success ? 'sent' : 'failed'}">
        ${item.success ? '✓ Sent' : '✗ Failed'}
      </span>
    </li>
  `).join('');
}

// ===== Sending State =====
function setLoading(loading) {
    sendBtn.disabled = loading;
    emailInput.disabled = loading;
    btnText.textContent = loading ? 'Sending...' : 'Send Application';
    btnSpinner.style.display = loading ? 'block' : 'none';
    btnIcon.style.display = loading ? 'none' : 'block';
}

// ===== Form Submit =====
form.addEventListener('submit', async (e) => {
    e.preventDefault();
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

    setLoading(true);

    try {
        const formData = new FormData();
        formData.append('email', email);

        // Append resume if uploaded
        if (resumeInput.files.length > 0) {
            formData.append('resume', resumeInput.files[0]);
        }

        // Append cover letter if customized
        if (coverLetterOpen) {
            formData.append('cover_letter', coverLetterInput.value);
        }

        const response = await fetch('/send', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            showToast(data.message, 'success');
            addToHistory(email, true);
            emailInput.value = '';
        } else {
            showToast(data.message, 'error');
            addToHistory(email, false);
        }
    } catch (err) {
        showToast('Network error. Please check if the server is running.', 'error');
        addToHistory(email, false);
    } finally {
        setLoading(false);
        emailInput.focus();
    }
});
